# -*- coding: utf-8 -*-
"""
Capstone Project: TCS (Graph)
Task: Scraping
Source: https://comptox.epa.gov/dashboard/
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

def loadCosingData(path):
    """load the data from cosing_clean.

      Args:
          path (string): The path of cosing data

      Returns:
          res: A data frame of cosing chemical name.
    """
    cosing = pd.read_excel(path)
    cosing_name = cosing['Chemical Name'].copy()
    cosing_name = cosing_name.apply(lambda x: x.lower())
    return cosing_name.to_frame()
    
def loadChemData(path):
    """load the data from comptox and do cleaning (remove na and convert to lower case).

      Args:
          path (string): The path of chemical dictionary data

      Returns:
          res: A cleaned data frame.
    """
    chem_dict = pd.read_csv(path)
    chem_dict = chem_dict.dropna(subset=['preferred_name', 'curation_level'])
    chem_dict_uni = chem_dict.drop_duplicates(subset=['preferred_name'])
    chem_dict_uni['preferred_name'] = chem_dict_uni['preferred_name'].apply(lambda x: str(x).lower())
    return chem_dict, chem_dict_uni


def findID_CompTox(str, chem_dict):
  """Find the corresponding DTXSID for each chemical that has a match.

    Args:
        str (string): The chemical name of this ingredient in cosing clean data
        chem_dict (dataframe): A dataframe containing the chemicals listed in CompTox website.

    Returns:
        res: A string value reporting the corresponding DTXSID.
  """
  if chem_dict['preferred_name'].str.fullmatch(str).sum() > 0:
      return chem_dict[chem_dict['preferred_name']==str]['DTXSID'].iloc[0]
  else:
      return ''

def findFunc(id, func_dict):
    """Find the corresponding functional uses for each chemical that has a match.

      Args:
          id (string): The DTXSID of this ingredient in cosing clean data
          func_dict (dataframe): A dataframe containing the chemicals listed in CompTox website.

      Returns:
          res: A string value reporting the corresponding functional uses, concatnated with comma.
    """
    if id == '':
        return ''
    sample_match = chem_dict[chem_dict['DTXSID']== id]
    sample_match_func = sample_match.join(func_dict[['chemical_id', 'report_funcuse']].set_index('chemical_id'), 
                                          how = 'inner', on = 'chemical_id')
    sample_func = sample_match_func.drop_duplicates(subset=['report_funcuse'])
    prop = ''
    for i in sample_func['report_funcuse']:
        prop = prop + str(i) + ','
    prop = prop[:-1]
    return prop

def findSynonyms(id, chem_dict):
    """Find the corresponding synonyms for each chemical that has a match.

      Args:
          id (string): The DTXSID of this ingredient in cosing clean data
          chem_dict (dataframe): A dataframe containing the chemicals listed in CompTox website.

      Returns:
          res: A string value reporting the corresponding synonyms, concatnated with comma.
    """
    sample_synonyms = chem_dict[chem_dict['DTXSID']== id]
    sample_synms = sample_synonyms.drop_duplicates(subset=['raw_chem_name'])
    synms = ''
    for i in sample_synms['raw_chem_name']:
        synms = synms + str(i) + ','
    synms = synms[:-1]
    return synms

def findDensityAndSolubility(id):
  
  den = 'Not found'
  sol = 'Not found'
  if isinstance(id, str):
      url = 'https://comptox.epa.gov/dashboard/chemical/properties/' + id
      driver = webdriver.Chrome(ChromeDriverManager().install())
      driver.get(url) 
      html = driver.page_source

      soup = BeautifulSoup(html, "html.parser") 
      content = [s.text.strip() for s in soup.find_all(class_ = "ag-cell-value")]
  else:
      return '', ''

  if 'Density' in content:
      den = content[content.index('Density') + 4]
  if 'Water Solubility' in content:
      sol = content[content.index('Water Solubility') + 4]
  
  return den, sol

if __name__ == '__main__':
     
    cosing = loadCosingData("cosing_clean.xlsx")
    chem_dict, chem_dict_uni = loadChemData('chemical_dictionary_20201216.csv')
    func_dict = pd.read_csv('functional_use_dictionary_20201216.csv')
    cosing['ID'] = cosing['Chemical Name'].apply(lambda x: findID_CompTox(x, chem_dict_uni))
    cosing['Functionalities'] = cosing['ID'].apply(lambda x: findFunc(x, func_dict))
    cosing['Synonyms'] = cosing['ID'].apply(lambda x: findSynonyms(x, chem_dict))
    cosing['Density'], cosing['Solubility'] = zip(*cosing['ID'].apply(lambda x: findDensityAndSolubility(x)))
    print(cosing.head())