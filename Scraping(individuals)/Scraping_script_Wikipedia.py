# -*- coding: utf-8 -*-
"""
@author: Anam Iqbal
"""

import requests
import pandas as pd

import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

'''
Function to get wikipedia link from google.
'''
def get_wiki_link_from_google(chem_name):
    keyword = chem_name
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')

    driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
    driver.get('https://www.google.com/')

    search_query = driver.find_element('name','q')
    search_query.send_keys(keyword + ' wikipedia')
    search_query.send_keys(Keys.RETURN)

    google_search_list = driver.find_element('id','search').text.split("\n")

    wiki_link = ""
    for i,line in enumerate(google_search_list):
        if 'Wikipedia' in line:
            wiki_link = google_search_list[i+1]
            break
    final_wiki_link = wiki_link.replace(" › ","/")
    return final_wiki_link

'''
Function to get one property from wikipedia from a given chemical name.
'''
def get_property(chemical):
    try:
        refined_chem_name = chemical.split()[0].capitalize() + "_".join([x for x in chemical.split()[1:]])
        try:
            df_pandas = pd.read_html("https://en.wikipedia.org/wiki/" + refined_chem_name, attrs = {'class': 'infobox ib-chembox'},  flavor='bs4', thousands ='.')
        except:
            link = get_wiki_link_from_google(chemical)
            df_pandas = pd.read_html(link, attrs = {'class': 'infobox ib-chembox'},  flavor='bs4', thousands ='.')
            
        all_df = pd.DataFrame(df_pandas[0])
        property_index = all_df[all_df[0] == 'Properties'].index[0]
        property_df = all_df.loc[property_index:]
        property_dict = dict(zip(property_df[0],property_df[1]))
        property_dict['Chemical Name'] = chemical
    except:
        property_dict = {'Chemical Name':chemical}
        
    return property_dict

'''
Function to get all properties from wikipedia from an input df with column 'Chemical Name'
'''
def get_properties(ingredients_df):
    all_chem_property_dicts = []
    for chemical in ingredients_df['Chemical Name']:
        property_dict = get_property(chemical)
        all_chem_property_dicts.append(property_dict)
    final_df = pd.DataFrame(all_chem_property_dicts)
    return final_df

'''
Function to get functionality from wikipedia from a given chemical name.
'''
def get_functionality(chemical,func_df):
    try:
        refined_chem_name = chemical.split()[0].capitalize() + "_".join([x for x in chemical.split()[1:]])
        response = requests.get(url="https://en.wikipedia.org/wiki/" + refined_chem_name)
        if response.status_code!=200:
            link = get_wiki_link_from_google(chemical)
            response = requests.get(url=link)
        soup = BeautifulSoup(response.content, 'html.parser')
        span = soup.find('span', {'id': 'Uses'})
        results = span.parent.find_next_siblings('p')
        
        result_subheadings_text = span.parent.find_next_siblings('p')
        all_uses_text = [x.text for x in results+result_subheadings_text]
        uses_text = " ".join(all_uses_text)
        all_funcs = []
        for func in func_df['Functionality']:
            if func in uses_text.lower():
                all_funcs.append(func)
        return all_funcs
    except:
        return []
    

'''
Function to get all functionalities from wikipedia from an input df with column 'Chemical Name'
'''
def get_functionalities(ingredients_df,functionality_file_name):
    all_chem_func_dict = {}
    func_df = pd.read_csv(functionality_file_name)
    for chemical in ingredients_df['Chemical Name']:
        all_chem_func_dict[chemical] = get_functionality(chemical,func_df)
    final_func_df = pd.DataFrame(all_chem_func_dict)
    return final_func_df


if __name__ == '__main__':

    functionality_file_name = './Wikipedia_All_functionalities.csv'
    ingredients_df = pd.read_excel("./cleansingPipeline/clean_chemical_list.xlsx")
    
    properties_df = get_properties(ingredients_df.iloc[0:3])

    functionalites_df = get_functionalities(ingredients_df.iloc,functionality_file_name)

    # Output the result
    properties_df.to_excel("./ScrapingResults/Properties_Wiki.xlsx")
    # functionalites_df.to_csv("All_wiki_functionalities.csv")
