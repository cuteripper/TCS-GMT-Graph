"""
Scraping script for obtaining information from ChemBK.
Source link: https://www.chembk.com/en

@author: Becky Yu
"""

# -- Import libraries --
from cmath import e
import pandas as pd
import csv

import requests
from bs4 import BeautifulSoup
import urllib.parse

'''
Function to scrape ChemBK's webpage using BeautifulSoup
'''
def scrapChemBK(header, df, outputFileName):
    # Write to file
    with open(outputFileName, 'w', encoding='UTF8', newline="") as f:
        try:
            writer = csv.writer(f)
            writer.writerow(header)

            count_e = 0  # error count
            for index, row in df.iterrows():
                synonyms = ""
                formula = ""
                weight = ""
                density = ""
                water_solubility = ""

                chemical_name = row['Chemical Name'].title().replace("/", " ")
                
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0',
                }
                url = "www.chembk.com/en/chem/" + chemical_name


                # Send request and parse the tables in response
                response = requests.get("https://" + urllib.parse.quote(url), headers=headers)

                soup = BeautifulSoup(response.text, 'html5lib')
                tables = soup.find_all('table')

                try:
                    ## summary table
                    rows = tables[0].find_all('tr')
                    for row in rows:
                        tds = row.find_all('td')

                        # Extract Synonyms into an array
                        if tds[0].text == 'Synonyms':
                            synonyms = [a.text for a in tds[1].find_all('a')]
                            

                    ## infos table
                    rows = tables[1].find_all('tr')
                    for row in rows:
                        tds = row.find_all('td')
                        
                        # Extract formula
                        if tds[0].text == 'Molecular Formula':
                            formula = tds[1].text

                        # Extract molecular weight
                        if tds[0].text == 'Molar Mass':
                            weight = tds[1].text
                            
                        # Extract Density
                        if tds[0].text == "Density":
                            density = tds[1].text

                        # Extract Water Solubility
                        if tds[0].text == "Water Solubility":
                            water_solubility = tds[1].text
                    
                    print(chemical_name, "Completed")

                    # Write result to csv file
                    writer.writerow([index, chemical_name, "", water_solubility,
                                    weight, density, formula, "", synonyms, ""])

                except Exception as e:
                    
                    # Write only the index and chemical name if no results found / if errors occured.
                    writer.writerow(
                        [index, chemical_name, "", "", "", "", "", "", ""])
                    count_e += 1
                    print("error" + str(count_e) + ": " +
                        chemical_name + " - " + str(e))
                    continue

        except Exception as e:
            print(e)



if __name__ == '__main__':
    
    # Read clean chemical list into dataframe
    df = pd.read_excel("cleansingPipeline/clean_chemical_list.xlsx", header = 0)
    print(len(df))

    # Drop duplicate chemical names if needed
    # df = df.drop_duplicates(subset='Chemical Name', keep="last")
    # print(len(df))
    # df = df.iloc[:1600]

    # Set file header
    header = ['id', 'Chemical Name', 'LogP (Partition coefficient)', 'LogS (water solubility of the ingredient)',
            'Molecular weight', 'Density', 'Chemical formula', 'Structure', 'Synonyms', 'Functionalities']

    scrapChemBK(header = header, df = df, outputFileName = 'ScrapingResults/Properties_Chembk_new.csv')