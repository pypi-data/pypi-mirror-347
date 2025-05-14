# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 12:25:16 2024

@author: thartl
"""

import pandas as pd
import os
import tempfile
import xml.etree.ElementTree as ET
import shutil
import zipfile
import xml.dom.minidom
import csv
import numpy as np
import json


def write_odf(x, filepath, languages = "all", odf_version = "1.1.0"):
    """
    Write a pandas DataFrame or Series to an Open Data Format (ODF) file.

    This function saves the provided pandas dataframe (`x`) to an ODF file, including
    metadata stored in its `attrs` attribute. Metadata can optionally be filtered by
    language.

    Parameters
    ----------
    x : pandas.DataFrame or pandas.Series
        The pandas object to be saved to the ODF file. It should have metadata stored in the `attrs` attribute for inclusion in the output file metadata.xml.
    filepath : str
        The file path (including filename) where the ODF file will be saved. Ensure the path ends with `.odf.zip` (or .zip for ODF version 1.0.0) to specify the correct file format.
    languages : str or list of str, default "all"
        Specifies which language(s) of metadata to include in the ODF file.
        Options include:
        - "all": Include metadata for all available languages.
        - A single language code (e.g., "en").
        - A list of language codes (e.g., ["en", "de"]).
        Edge cases like empty strings or `None` in the language list are handled gracefully.

    Returns
    -------
    None
        The function writes the file to the specified `path` and does not return a value.

    Raises
    ------
    TypeError
        If `x` is not a pandas DataFrame or Series.
    ValueError
        If `languages` contains invalid values.

    Notes
    -----
    - Metadata from the attributes (`attrs`) of `x` is included in the file.
    - Multilingual metadata, if present, is processed according to the `languages` parameter.

    Examples
    --------
    Write a DataFrame to an ODF file, including all metadata:
    >>> import opendataformat as odf
    >>> df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    >>> df.attrs = {"label_en": "English Label", "label_de": "German Label", "description_en": "Example dataset"}
    >>> odf.write_odf(df, "output.odf.zip")

    Write a DataFrame to an ODF file, filtering metadata by language:

    >>> odf.write_odf(df, "output.zip", languages="en")

    Write a DataFrame to an ODF file, including metadata for multiple languages:

    >>> odf.write_odf(df, "output.zip", languages="all")
    """
    # Raise error if input is not a pandas dataframe
    if (not isinstance(x, pd.DataFrame)):
        raise TypeError("Input not a pandas.core.frame.DataFrame")
    filepath = os.path.realpath(filepath)
    
    # add extension if missing (.zip in case of odf_version = 1.0.0 and .odf.zip for later version)
    if not filepath.endswith(".zip"):
        if odf_version == "1.0.0" or filepath.endswith(".odf"):
            filepath = filepath + ".zip"
        else:
            filepath = filepath + ".odf.zip"

    # convert anlanguages to a list or if languages = ["all"] unlist it
    if languages != "all" and not isinstance(languages, list):
        languages = [languages]
    # if languages = ["all"] unlist it
    if isinstance(languages, list) and len(languages) == 1:
        if languages[0] == "all":
            languages = languages[0]
    # if None or '' in languages add metadatafields without language tag       
    if isinstance(languages, list) and (None in languages or '' in languages):
        languages += ["label", "labels", "description"]

    # Get the path of the system's temporary directory
    temp_dir = tempfile.gettempdir()

    # Create the full path for the temporary directory for odf output components
    temp_subdir = os.path.join(temp_dir, '/odf_temp')

    # Remove the directory if it already exists
    if os.path.exists(temp_subdir):
        shutil.rmtree(temp_subdir)

    # Create the directory
    os.makedirs(temp_subdir, exist_ok=True)
    
    #function to reformat floats to conserve all digits 
    # in non-scientific notation
    def custom_formatter(x):
        if isinstance(x, float):
            if np.isnan(x):  # Check if the value is NaN
                return np.nan  # Preserve NaN as-is
            return np.format_float_positional(x, trim='-')
        return x
    
    x_reformatted = x.map(custom_formatter)
    
    # re-add the attributes
    for col in list(x.columns):
        x_reformatted[col].attrs = x[col].attrs
    x = x_reformatted

    vers_major = int(odf_version.split('.')[0])
    vers_minor = int(odf_version.split('.')[1])
    vers_patch = int(odf_version.split('.')[2])
    # write odf-version.json file if version is 1.1.0 or higher
    if (vers_major == 1 and vers_minor >=1) or vers_major >= 2:
        # define version file as dictionary
        version_file = {
            "fileType": "opendataformat",
            "version": odf_version,
            "files": {
            "data": "data.csv",
            "metadata": "metadata.xml"
            }
        }
        # Write version file
        with open(temp_subdir + '/odf-version.json', "w") as f:
            json.dump(version_file, f, indent=2)  # Pretty formatting with indent

    # write raw data as csv to the output folder
    x.to_csv(temp_subdir + "/data.csv", 
             index = False,
             encoding = 'utf-8',
             quotechar='"',
             quoting=csv.QUOTE_MINIMAL,
             float_format='%.15f')

    
    # Create the root element
    root = ET.Element("codeBook", {
        "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "xmlns": "ddi:codebook:2_5",
        "xsi:schemaLocation": "ddi:codebook:2_5 http://www.ddialliance.org/Specification/DDI-Codebook/2.5/XMLSchema/codebook.xsd",
        "version": "2.5"
    })
    
    # Add study description section
    stdyDscr = ET.SubElement(root, "stdyDscr")
    citation = ET.SubElement(stdyDscr, "citation")
    titlStmt = ET.SubElement(citation, "titlStmt")
    ET.SubElement(titlStmt, "titl").text = x.attrs.get('study', "")
    
    # Add file description section
    fileDscr = ET.SubElement(root, "fileDscr")
    fileTxt = ET.SubElement(fileDscr, "fileTxt")
    ET.SubElement(fileTxt, "fileName").text = x.attrs.get('dataset', "")
    
    fileCitation = ET.SubElement(fileTxt, "fileCitation")
    titlStmtFile = ET.SubElement(fileCitation, "titlStmt")
    
    # Get labels
    labels = {}
    for k,v in x.attrs.items():
        if (k == "label" or k.startswith("label_")):
            labels[k] = v
    # keep only relevant languages if languages != 'all'
    if isinstance(languages, list):
        labels = {key: value for key, value in labels.items() if key.split('_')[-1] in languages}
        
    first_label = True
    for key,value in labels.items():   
        if (len(key.split("_"))==1):
            lang = "NA"
            if first_label == True:
                ET.SubElement(titlStmtFile, "titl").text = value
                first_label = False
            else:
                ET.SubElement(titlStmtFile, "parTitl").text = value
        else:
            lang = key.split("_")[1]
            if first_label == True:
                ET.SubElement(titlStmtFile, "titl", {"xml:lang": lang}).text = value
                first_label = False
            else:
                ET.SubElement(titlStmtFile, "parTitl", {"xml:lang": lang}).text = value
    
    # Get descriptions
    descriptions = {}
    for k,v in x.attrs.items():
        if (k == "description" or k.startswith("description_")):
            descriptions[k] = v
    # keep only relevant languages if languages != 'all'
    if isinstance(languages, list):
        descriptions = {key: value for key, value in descriptions.items() if key.split('_')[-1] in languages}
    
    
    
    for key, value in descriptions.items():   
        if (len(key.split("_"))==1):
            lang = "NA"
            ET.SubElement(fileTxt, "fileCont").text = value

        else:
            lang = key.split("_")[1]
            ET.SubElement(fileTxt, "fileCont", {"xml:lang": lang}).text = value

    
    # Add external link to the dataset
    notes = ET.SubElement(fileDscr, "notes")
    ET.SubElement(notes, "ExtLink", {"URI": x.attrs.get('url', "")})


    # Add data description with variable Metadata
    dataDscr = ET.SubElement(root, "dataDscr")
    for col in list(x.columns):
        var = ET.SubElement(dataDscr, "var", {"name": col})
        if x[col].attrs == x.attrs:
            continue
        metadata_dict = x[col].attrs
        # Get labels
        labels = {}
        for k,v in metadata_dict.items():
            if (k == "label" or k.startswith("label_")):
                labels[k] = v
        # keep only relevant languages if languages != 'all'
        if isinstance(languages, list):
            labels = {key: value for key, value in labels.items() if key.split('_')[-1] in languages}
                
        for key,value in labels.items():   
            if (len(key.split("_"))==1):
                lang = "NA"
                ET.SubElement(var, "labl").text = value
            else:
                lang = key.split("_")[1]
                ET.SubElement(var, "labl", {"xml:lang": lang}).text = value
                    
                    

        # Add English and German descriptions for the variable
        descriptions = {}
        for k,v in metadata_dict.items():
            if (k == "description" or k.startswith("description_")):
                descriptions[k] = v
        # keep only relevant languages if languages != 'all'
        if isinstance(languages, list):
            descriptions = {key: value for key, value in descriptions.items() if key.split('_')[-1] in languages}
            
        # Add file content descriptions in multiple languages
        for key, value in descriptions.items():   
            if (len(key.split("_"))==1):
                lang = "NA"
                ET.SubElement(var, "txt").text = value
            else:
                lang = key.split("_")[1]
                ET.SubElement(var, "txt", {"xml:lang": lang}).text = value
        
        
        valuelabels = {}
        for k,v in metadata_dict.items():
            if (k == "labels" or k.startswith("labels_")):
                valuelabels[k] = v
        # keep only relevant languages if languages != 'all'
        if isinstance(languages, list):
            valuelabels = {key: value for key, value in valuelabels.items() if key.split('_')[-1] in languages}
            
        labelled_values = []
        for key1, val1 in valuelabels.items():
            for key2 in val1.keys():
                if key2 not in labelled_values:
                    labelled_values.append(key2)

        
        for val in labelled_values:   
            catgry = ET.SubElement(var, "catgry")
            ET.SubElement(catgry, "catValu").text = val
            for key, value in valuelabels.items():
                if (len(key.split("_"))==1):
                    lang = "NA"
                    ET.SubElement(catgry, "labl").text = value[val]
                else:
                    lang = key.split("_")[1]
                    ET.SubElement(catgry, "labl", {"xml:lang": lang}).text = value[val]


        # Add variable format
        ET.SubElement(var, "varFormat", {"type": x[col].attrs.get('type', "")})
        
        # Add external link to the variable
        var_notes = ET.SubElement(var, "notes")
        ET.SubElement(var_notes, "ExtLink", {"URI": x[col].attrs.get('url', "")})
    
    
    
    # Add indentations and line breaks
    # Convert the ElementTree to a string
    xml_str = ET.tostring(root, encoding='UTF-8')

    # Use minidom to pretty-print the XML
    dom = xml.dom.minidom.parseString(xml_str)
    pretty_xml = dom.toprettyxml(indent="  ")
    
    # write xml to a file
    with open(temp_subdir + "/metadata.xml", "w", encoding = "UTF-8") as f:
        f.write(pretty_xml)
    

    # Create a zip file and add files to it
    with zipfile.ZipFile(filepath, 'w') as zipf:
        zipf.write(os.path.join(temp_subdir, 'metadata.xml'), arcname='metadata.xml')
        zipf.write(os.path.join(temp_subdir, 'data.csv'), arcname='data.csv')
        if (vers_major == 1 and vers_minor >=1) or vers_major >= 2:
            zipf.write(os.path.join(temp_subdir, 'odf-version.json'), arcname='odf-version.json')


    print(f"File sucessfully written to {filepath}.")
    
    
    

