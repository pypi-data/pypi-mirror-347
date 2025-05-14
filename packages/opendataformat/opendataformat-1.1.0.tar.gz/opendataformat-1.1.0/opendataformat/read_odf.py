# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 12:24:04 2024

@author: xhan
"""

# ODF2pd

import pandas as pd
import zipfile
import xml.etree.ElementTree as ET
import os
from tempfile import gettempdir
from urllib.request import urlretrieve
from urllib.parse import urlparse
import json
import warnings

      


def read_odf(filepath, languages = "all", usecols = None, skiprows=None, nrows=None, na_values = None):
    """
    Read an Open Data Format (ODF) file into a Pandas DataFrame.

    This function reads data from an ODF zipfile (containing data.csv and metadata.xml) and converts it into a pandas DataFrame.
    It supports language selection, optional filtering of columns, skipping rows, and replacing specific values
    with NaN.

    Parameters
    ----------
    filepath : str
        The file path to the ODF file to be read.
    languages : str or list of str, default "all"
        Specifies the language(s) to extract from the file. Use "all" to read all available languages, or pass a single language code (e.g., "en").
    usecols : list of int or str, optional
        Specifies the columns to be read from the file. If None, all columns are read. Column selection can be by index or name.
    skiprows : int or list of int, optional
        Line numbers to skip (0-indexed) at the start of the file. Can be used to skip metadata or headers.
    nrows : int, optional
        The number of rows to read from the file. If None, all rows are read.
    na_values : scalar, str, list-like, or dict, optional
        Additional values to consider as NaN. If dict, applies per column.

    Returns
    -------
    DataFrame
        A pandas DataFrame containing the data and metadata from the ODF file.

    Notes
    -----
    - The `languages` parameter allows for selecting specific localized data if the ODF file supports it.
    - Metadata is stored in the `attrs` attribute of pandas objects- You can call the attributes with df.attrs or df['variable_name'].attrs.

    Examples
    --------
    Read an ODF file and load all columns:
    >>> import opendataformat as odf
    >>> df = odf.read_odf("example_dataset.odf.zip")

    Read an ODF zipfile, selecting specific language:

    >>> df = odf.read_odf("example_dataset.odf.zip", languages="en")

    """
    
    # Check if file exists or is a URL
    def is_url(path):
        parsed = urlparse(path)
        # A URL typically has a scheme (e.g., "http", "https") and a network location (netloc)
        return bool(parsed.scheme) and bool(parsed.netloc)

    if not os.path.exists(filepath) and not is_url(filepath):
        raise FileNotFoundError(f"The file {filepath} was not found.")
    
    # Download file to tempdir if filepath is URL
    if is_url(filepath):
        # Get the system's temporary directory
        temp_dir = gettempdir()
        
        fname = filepath.split("/")[-1]
        # Define the full path where the file will be saved
        download_file_path = os.path.join(temp_dir, fname)
        
        # Download the file using urllib
        try:
            urlretrieve(filepath, download_file_path)
        except Exception:
            raise Exception("Downloading file from URL failed.")
        
        filepath = download_file_path
        
        if not os.path.exists(filepath):
            FileNotFoundError(f"The file {filepath} was not found.")
    
    #check if input is a zipped file of an unzipped folder
    if '.zip' not in filepath:
        file_not_zipped = True
    else:
        file_not_zipped = False

    #read version file
    if file_not_zipped == False:
        with zipfile.ZipFile(filepath, 'r') as zip_ref:    
            # read the version file if existing        
            if 'odf-version.json' in zip_ref.namelist():
                with zip_ref.open('odf-version.json') as json_file:
                    version_file = json.load(json_file)  # Read and parse JSON
                if 'version' not in version_file  or 'files' not in version_file or 'data' not in version_file.get('files', {}) or 'metadata' not in version_file.get('files', {}):
                    warnings.warn(f"Version file in {filepath} is corrupt and (partly) ignored.", UserWarning)
                odf_version = version_file.get('version', '1.1.0')
                vers_files = version_file.get('files', {'data': 'data.csv', 'metadata': 'metadata.xml'})
                datafile = vers_files.get('data', 'data.csv')
                metadatafile = vers_files.get('metadata', 'metadata.xml')
            else:
                odf_version='1.0.0'
                datafile = 'data.csv'
                metadatafile = 'metadata.xml'
    else:
        # read the version file if existing        
        if os.path.isfile(os.path.join(filepath, 'odf-version.json')):
            with open(os.path.join(filepath, 'odf-version.json'), "r") as f:
                vers_file = json.load(f)  # Load JSON content
                odf_version = vers_file['version']
                datafile = vers_file['files']['data']
                metadatafile = vers_file['files']['metadata']
        else:
            odf_version='1.0.0'
            datafile = 'data.csv'
            metadatafile = 'metadata.xml'

    

    #if input is a unzipped folder, check if data and metadatafile are available
    if not filepath.endswith(".zip") and (not os.path.exists(filepath + "/" + datafile) or not os.path.exists(filepath + "/" + metadatafile)):
        raise FileNotFoundError(f"A file {filepath + '.zip'} was not found and in the folder {filepath} expected {metadatafile} and {datafile}.")
    

    if file_not_zipped == False:
        
        # Open zip data and xml file in it   
        with zipfile.ZipFile(filepath, 'r') as zip_ref:    

            #check if data and metadata file are in the zip file
            if datafile not in zip_ref.namelist():
                    raise Exception(f"Expected {datafile} in {filepath}")
            if metadatafile not in zip_ref.namelist():
                    raise Exception(f"Expected {metadatafile} in {filepath}")
            
            try:
                root=ET.fromstring(zip_ref.read(metadatafile))
            except Exception as e:
                raise Exception(f"{type(e).__name__} in reading metadata.xml in {filepath}. Check the xml file in the data file")
            
            # Iterate through the tags in xml and remove prefix of each tag
            for i in root.iter():
                i.tag=i.tag.split('}')[-1]
                #print(i.tag)
            #read the csv file
            with zip_ref.open(datafile) as csv_file:            
                if (skiprows != None):
                    if (type(skiprows) == int):
                        skiprows = list(range(skiprows))
                    skiprows = [x + 1 for x in skiprows]
                df = pd.read_csv(csv_file, encoding='UTF-8', usecols = usecols, skiprows=skiprows, nrows=nrows, na_values = na_values)
                
                # Convert integer values with NAN from float to integer
                for col in df.columns:
                    if df[col].dtype == 'float64':
                        # Check if all values are integers (ignoring NaNs)
                        if df[col].dropna().apply(lambda x: x % 1 == 0).all():
                            df[col] = df[col].astype('Int64')  # Convert to nullable integer
                
                if usecols != None and all(isinstance(item, str) for item in usecols):
                    df = df[usecols]

                
                
            # Make dataset dictionary
            dataset_dic=make_dataset_dic(root)
                
            # Make variables dictionary
            variables_dic=make_variables_dic(root, variables =  list(df.columns))
                
            #remove languages that are not needed
            if languages != "all":
                if type(languages) == str:
                    languages = [languages]
                keys_wrong_language = []
                for key in dataset_dic.keys():
                    if 'label_' in key or 'description_' in key:
                        if key.split("_")[1] not in languages:
                            keys_wrong_language.append(key)
                for key in keys_wrong_language:
                    dataset_dic.pop(key)
                for varname in variables_dic.keys():
                    var_dic = variables_dic[varname]
                    keys_wrong_language = []
                    for key in var_dic.keys():
                        if 'label_' in key or 'labels_' in key or 'description_' in key:
                            if key.split("_")[1] not in languages:
                                keys_wrong_language.append(key)
                    for key in keys_wrong_language:    
                        var_dic.pop(key)
                    variables_dic[varname] = var_dic

            df.attrs=dataset_dic
            for var_name, attributes in variables_dic.items():
                if var_name in df.columns:
                    df[var_name].attrs=attributes
                    
    elif file_not_zipped == True:
        

        metadata_path = os.path.join(filepath, metadatafile)
        data_csv_path = os.path.join(filepath, datafile)

        # Ensure files exist
        if not os.path.exists(metadata_path) or not os.path.exists(data_csv_path):
            raise ValueError("Expected metadata.xml and data.csv in {filepath}")

        # Parse metadata.xml directly
        try:
            tree = ET.parse(metadata_path)
        except Exception as e:
            raise Exception(f"{type(e).__name__} in reading metadata.xml in {filepath}. Check the xml file in the data file")

        root = tree.getroot()

        # Process XML tags
        for i in root.iter():
            i.tag = i.tag.split('}')[-1]


        # Load data.csv from folder and save dictionaries to DataFrame

        if (skiprows != None):
            if (type(skiprows) == int):
                skiprows = list(range(skiprows))
            skiprows = [x + 1 for x in skiprows]
        df = pd.read_csv(data_csv_path, encoding='UTF-8', usecols = usecols, skiprows=skiprows, nrows=nrows, na_values = na_values)
        
        # Convert integer values with NAN from float to integer
        for col in df.columns:
            if df[col].dtype == 'float64':
                # Check if all values are integers (ignoring NaNs)
                if df[col].dropna().apply(lambda x: x % 1 == 0).all():
                    df[col] = df[col].astype('Int64')  # Convert to nullable integer
                    
        if usecols != None and all(isinstance(item, str) for item in usecols):
            df = df[usecols]

        
        # Make dataset dictionary
        dataset_dic=make_dataset_dic(root)
        
        # Make variables dictionary
        variables_dic=make_variables_dic(root, variables =  list(df.columns))
        
        #remove languages that are not needed
        if languages != "all":
            if type(languages) == str:
                languages = [languages]
            keys_wrong_language = []
            for key in dataset_dic.keys():
                if 'label_' in key or 'description_' in key:
                    if key.split("_")[1] not in languages:
                        keys_wrong_language.append(key)
            for key in keys_wrong_language:
                dataset_dic.pop(key)
            for varname in variables_dic.keys():
                var_dic = variables_dic[varname]
                keys_wrong_language = []
                for key in var_dic.keys():
                    if 'label_' in key or 'labels_' in key or 'description_' in key:
                        if key.split("_")[1] not in languages:
                            keys_wrong_language.append(key)
                for key in keys_wrong_language:    
                    var_dic.pop(key)
                variables_dic[varname] = var_dic
                    
        df.attrs = dataset_dic
        for var_name, attributes in variables_dic.items():
            if var_name in df.columns:
                df[var_name].attrs=attributes
    return df
        


def make_dataset_dic(root):        
    dictionary = {}  # Initialize the dictionary to store label entries
    #study and dataset name
    dictionary['study'] = root.findtext(".//stdyDscr/citation/titlStmt/titl")
    dictionary['dataset'] = root.findtext(".//fileDscr/fileTxt/fileName")
    # labels
    titl_stmt = root.find('.//fileDscr/fileTxt/fileCitation/titlStmt')
    if titl_stmt is not None:
        # Loop through each child element in titlStmt
        for elem in titl_stmt:
            # Check if there is a language attribute
            lang = elem.get('{http://www.w3.org/XML/1998/namespace}lang')
            if lang:
                # Store text with 'label_<language>' key if lang attribute exists
                dictionary[f'label_{lang}'] = elem.text
            else:
                # Store text with 'label' key if no lang attribute exists
                dictionary['label'] = elem.text
    # Process descriptions in fileCont
    for file_cont in root.findall('.//fileDscr/fileTxt/fileCont'):
        lang = file_cont.get('{http://www.w3.org/XML/1998/namespace}lang')
        if lang:
            dictionary[f'description_{lang}'] = file_cont.text
        else:
            dictionary['description'] = file_cont.text
    #URL
    ExtLink = root.findall('.//fileDscr/notes/ExtLink')
    if len(ExtLink) == 1:
        dictionary['url'] = ExtLink[0].get('URI')

    return dictionary

def make_variables_dic(root, variables):        
    dictionaries={}
    
    for var in root.findall('.//dataDscr/var'):
        varname = var.attrib.get('name')
        if varname not in variables:
            continue
        # dictionary
        dictionary = {}
        # variable
        dictionary['variable'] = var.attrib.get('name')
        
        
        # Process `labl` elements
        for labl_elem in var.findall('labl'):
            # Check if there is a language attribute
            lang = labl_elem.get('{http://www.w3.org/XML/1998/namespace}lang')
            if lang:
                # Store text with 'label_<language>' key if lang attribute exists
                dictionary[f'label_{lang}'] = labl_elem.text
            else:
                # Store text with 'label' key if no lang attribute exists
                dictionary['label'] = labl_elem.text
        
        # Process `txt` elements
        for txt_elem in var.findall('txt'):
            # Check if there is a language attribute
            lang = txt_elem.get('{http://www.w3.org/XML/1998/namespace}lang')
            if lang:
                # Store text with 'description_<language>' key if lang attribute exists
                dictionary[f'description_{lang}'] = txt_elem.text
            else:
                # Store text with 'description' key if no lang attribute exists
                dictionary['description'] = txt_elem.text
        
        # Process `catgry` elements to accumulate labels by language
        for catgry_elem in var.findall('catgry'):
            # Get the category value
            catValu_elem = catgry_elem.find('catValu')
            if catValu_elem is not None:
                cat_value = catValu_elem.text
            else:
                continue  # Skip if there's no category value
    
            # Loop through `labl` elements within `catgry`
            for labl_elem in catgry_elem.findall('labl'):
                lang = labl_elem.get('{http://www.w3.org/XML/1998/namespace}lang', 'default')
                # Construct the key for labels by language (e.g., 'labels_en', 'labels_de')
                labels_key = f'labels_{lang}' if lang != 'default' else 'labels'
                
                # Initialize the dictionary for this language if not already present
                if labels_key not in dictionary:
                    dictionary[labels_key] = {}
                
                # Add the category value and corresponding label to the dictionary for the language
                dictionary[labels_key][cat_value] = labl_elem.text
        
        # Process `varFormat` for type
        varFormat_elem = var.find('varFormat')
        if varFormat_elem is not None:
            dictionary['type'] = varFormat_elem.get('type')
        
        # Process `ExtLink` for external URL
        extLink_elem = var.find('.//notes/ExtLink')
        if extLink_elem is not None:
            dictionary['url'] = extLink_elem.get('URI')
        
        dictionaries[varname] = dictionary
        
    return dictionaries
