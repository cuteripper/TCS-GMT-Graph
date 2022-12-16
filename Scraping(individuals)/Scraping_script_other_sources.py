#!/usr/bin/env python
# coding: utf-8

# # ChEBI

# ###Code to load the data:

# In[ ]:



synonyms = pd.read_csv('names_3star.tsv',sep='\t')
compounds = pd.read_csv('compounds_3star.tsv',sep='\t')


# In[ ]:


synonyms.shape


# In[ ]:


synonyms.columns


# In[ ]:


synonyms.head()


# In[ ]:


synonyms = synonyms.drop_duplicates(subset=['NAME'])


# In[ ]:


synonyms.shape


# In[ ]:


compounds.shape


# In[ ]:


compounds.columns


# In[ ]:


compounds.head()


# In[ ]:


compounds = compounds.drop_duplicates(subset=['NAME'])


# In[ ]:


compounds.shape


# ###Remove NAN

# In[ ]:


compounds = compounds.dropna(subset=['NAME'])


# In[ ]:


import pandas as pd


# ##Load cosing_clean

# In[ ]:


cosing = pd.read_excel("./cosing_clean.xlsx")
cosing.head()


# In[ ]:


cosing_name = cosing['Chemical Name'].copy()


# In[ ]:


cosing_name = cosing_name.apply(lambda x: x.lower())
cosing_name = cosing_name.to_frame()


# #### Sample match:

# In[ ]:


compounds[compounds['NAME'].str.fullmatch('acetaldehyde')]


# In[ ]:


def findName(str, compounds, synonyms):
  """Determine whether this ingredient can be found in ChEBI data.

    Args:
        str (string): The chemical name of this ingredient in cosing clean data
        compounds (dataframe): A dataframs containing the chemicals listed in ChEBI website.
        synonyms (dataframs): A dataframe containing the synonyms of chemicals listed in ChEBI website.

    Returns:
        res: A boolean value reporting whether a match has been found.
  """
  if compounds['NAME'].str.fullmatch(str).sum() > 0:
    return True
  elif synonyms['NAME'].str.fullmatch(str).sum() > 0:
    return True
  else:
    return False


# ###Report percentage of coverage:

# In[ ]:


cosing_name['Chemical Name'].apply(lambda x: findName(x, compounds, synonyms)).mean()


# In[ ]:


cosing_name['matched'] = cosing_name['Chemical Name'].apply(lambda x: findName(x, compounds, synonyms))


# In[ ]:


cosing_name.head()


# In[ ]:


cosing_name_matched = cosing_name[cosing_name['matched'] == True].copy()
cosing_name_matched.head()


# In[ ]:


def findID(str, compounds, synonyms):
  """Determine whether this ingredient can be found in ChEBI data.

    Args:
        str (string): The chemical name of this ingredient in cosing clean data
        compounds (dataframe): A dataframs containing the chemicals listed in ChEBI website.
        synonyms (dataframs): A dataframe containing the synonyms of chemicals listed in ChEBI website.

    Returns:
        res: A boolean value reporting whether a match has been found.
  """
  if compounds['NAME'].str.fullmatch(str).sum() > 0:
    return int(compounds[compounds['NAME'].str.fullmatch(str) == True]['ID'].values)
  else:
    return int(synonyms[synonyms['NAME'].str.fullmatch(str) == True]['COMPOUND_ID'].values)


# In[ ]:


cosing_name_matched['ID'] = cosing_name_matched['Chemical Name'].apply(lambda x: findID(x, compounds, synonyms))


# In[ ]:


cosing_name_matched.head()


# In[ ]:


relation = pd.read_csv('relation_3star.tsv',sep='\t')
relation.head()


# #### Sample functionality (for 'acetaldehyde')

# In[ ]:


sample_relation = relation[relation['FINAL_ID']  == 15343]
sample_relation


# In[ ]:


sample_relation.join(compounds[['ID', 'NAME']].set_index('ID'), how = 'left', on = 'INIT_ID')


# # CPDatRelease

# Each unique chemical record associated with a data document has been assigned a chemical
# record ID, associated with a reported chemical name and Chemical Abstract Service Registration
# Number (CAS), if available. Each of these individual chemical records are eventually officially
# curated using automated workflows within EPA’s Distributed Structure-Searchable Toxicity
# (DSSTox) database (Williams et al., 2017), where they are assigned a preferred name, CAS, and
# a DSSTox Chemical Substance ID (DTXSID).

# ##Code to load the data:

# In[ ]:


import pandas as pd


# In[ ]:


chem_dict = pd.read_csv('chemical_dictionary_20201216.csv')


# In[ ]:


chem_dict.head()


# ###Remove NAN

# In[ ]:


chem_dict = chem_dict.dropna(subset=['preferred_name', 'curation_level'])


# In[ ]:


chem_dict['preferred_name'] = chem_dict['preferred_name'].apply(lambda x: str(x).lower())


# ###Sample match

# In[ ]:


chem_dict[chem_dict['preferred_name'].str.fullmatch('acetaldehyde')]


# **Preferred name is not unique in our case, we should drop duplicate to speed up**

# In[ ]:


chem_dict_uni = chem_dict.drop_duplicates(subset=['preferred_name'])


# In[ ]:


chem_dict_uni.shape


# ##Function for matching

# In[ ]:


def findNameCPD(str, chem_dict):
  """Determine whether this ingredient can be found in CPDat data.

    Args:
        str (string): The chemical name of this ingredient in cosing clean data
        compounds (dataframe): A dataframs containing the chemicals listed in CPDat website.
        synonyms (dataframs): A dataframe containing the synonyms of chemicals listed in CPDat website.

    Returns:
        res: A boolean value reporting whether a match has been found.
  """
  if chem_dict['preferred_name'].str.fullmatch(str).sum() > 0:
    return True
  else:
    return False


# **Report percentage of coverage:**

# In[ ]:


cosing_name_CPD = cosing['Chemical Name'].copy()


# In[ ]:


cosing_name_CPD = cosing_name_CPD.apply(lambda x: x.lower())
cosing_name_CPD = cosing_name_CPD.to_frame()


# In[ ]:


cosing_name_CPD['Chemical Name'].apply(lambda x: findNameCPD(x, chem_dict_uni)).mean()


# In[ ]:


cosing_name_CPD['matched'] = cosing_name_CPD['Chemical Name'].apply(lambda x: findNameCPD(x, chem_dict_uni))


# In[ ]:


cosing_name_CPD.head()


# In[ ]:


cosing_name_CPD_matched = cosing_name_CPD[cosing_name_CPD['matched'] == True].copy()
cosing_name_CPD_matched.head()


# In[ ]:


def findID_CPD(str, chem_dict):
  """Determine whether this ingredient can be found in ChEBI data.

    Args:
        str (string): The chemical name of this ingredient in cosing clean data
        compounds (dataframe): A dataframs containing the chemicals listed in ChEBI website.
        synonyms (dataframs): A dataframe containing the synonyms of chemicals listed in ChEBI website.

    Returns:
        res: A boolean value reporting whether a match has been found.
  """
  
  return chem_dict[chem_dict['preferred_name']==str]['DTXSID'].iloc[0]


# In[ ]:


cosing_name_CPD_matched['ID'] = cosing_name_CPD_matched['Chemical Name'].apply(lambda x: findID_CPD(x, chem_dict_uni))


# In[ ]:


cosing_name_CPD_matched.head()


# ## Find functionality (for 'acetaldehyde')

# **Load functional use data.**

# In[ ]:


func_dict = pd.read_csv('functional_use_dictionary_20201216.csv')
func_dict.head()


# ###Test sample

# In[ ]:


sample_match = chem_dict[chem_dict['DTXSID']=='DTXSID5039224']
sample_match


# In[ ]:


sample_match_func = sample_match.join(func_dict[['chemical_id', 'report_funcuse']].set_index('chemical_id'), 
                                      how = 'inner', on = 'chemical_id')


# In[ ]:


sample_func = sample_match_func.drop_duplicates(subset=['report_funcuse'])


# In[ ]:


sample_func


# ## functionality  and synonyms
# 
# 
# 

# In[ ]:


res = pd.read_excel('search_result.xlsx', sheet_name=1)


# In[ ]:


res.head()


# In[ ]:


def findFunc(id):
  sample_match = chem_dict[chem_dict['DTXSID']== id]
  sample_match_func = sample_match.join(func_dict[['chemical_id', 'report_funcuse']].set_index('chemical_id'), 
                                      how = 'inner', on = 'chemical_id')
  sample_func = sample_match_func.drop_duplicates(subset=['report_funcuse'])
  prop = ''
  for i in sample_func['report_funcuse']:
    prop = prop + str(i) + ','
  prop = prop[:-1]
  return prop


# In[ ]:


def findSynonyms(id):
  sample_synonyms = chem_dict[chem_dict['DTXSID']== id]
  sample_synms = sample_synonyms.drop_duplicates(subset=['raw_chem_name'])
  synms = ''
  for i in sample_synms['raw_chem_name']:
    synms = synms + str(i) + ','
  synms = synms[:-1]
  return synms


# In[ ]:


res['Functionalities'] = res['DTXSID'].apply(lambda x: findFunc(x))
res.head()


# In[ ]:


res['Synonyms'] = res['DTXSID'].apply(lambda x: findSynonyms(x))
res.head()


# ## Find properties (for 'acetaldehyde')

# In[ ]:


get_ipython().system('pip install selenium')


# In[ ]:


get_ipython().system('apt-get update ')
get_ipython().system('apt install chromium-chromedriver')

from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)


# In[ ]:


import requests
from bs4 import BeautifulSoup
import time


# In[ ]:


def findDensityAndSolubility(id):
  
  den = 'Not found'
  sol = 'Not found'
  if isinstance(id, str):
      url = 'https://comptox.epa.gov/dashboard/chemical/properties/' + id
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
  


# In[ ]:


res['Density'], res['solubility'] = zip(*res['DTXSID'].apply(lambda x: findDensityAndSolubility(x)))
res.head()


# In[ ]:


res.to_excel('res.xlsx')


# ### Sample property case

# In[ ]:


DTXID = 'DTXSID5039224'
url = 'https://comptox.epa.gov/dashboard/chemical/properties/' + DTXID


# In[ ]:


driver.get(url) 
html = driver.page_source


# In[ ]:


soup = BeautifulSoup(html, "html.parser")


# In[ ]:


content = [s.text.strip() for s in soup.find_all(class_ = "ag-cell-value")]
content.index('Density')


# In[ ]:


vapor_pressure = soup.find_all(class_ = "ag-cell-value")[81].text.split()[0]
water_solubility = soup.find_all(class_ = "ag-cell-value")[89].text.split()[0]


# In[ ]:


soup.find_all(class_ = "ag-cell-value")[81]


# In[ ]:


soup.find_all(class_ = "ag-cell-value")[89].text.strip()


# In[ ]:


soup.find_all(class_ = "ag-cell-value")[88]


# In[ ]:


cosing_name_CPD_matched


# In[ ]:


cosing_name_CPD_matched.head(10)


# In[ ]:


excel = pd.read_excel("Property_and_functionalities1.xlsx")
excel.head()


# In[ ]:


excel['Chemical Name'] = excel['Chemical Name'].apply(lambda x: x.lower())


# In[ ]:


other = pd.read_csv('other.csv')
other


# In[ ]:


cosing_name_CPD_matched = cosing_name_CPD_matched.join(other.set_index('DTXSID'), 
                                                       how = 'left', on = 'ID')
cosing_name_CPD_matched


# In[ ]:


out = excel.join(cosing_name_CPD_matched.set_index('Chemical Name'), 
                 how = 'left', on = 'Chemical Name')
out


# In[ ]:


# out.to_csv('res.csv')
out.to_csv('./ScrapingResults/Properties_Other_Source.csv')


# In[ ]:




