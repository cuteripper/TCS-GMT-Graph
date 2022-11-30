# Original (for group)

# -- Import libraries --
from cmath import e
import pandas as pd
import csv

import requests
from bs4 import BeautifulSoup
import urllib.parse


# Read CSV file into dataframe
df = pd.read_excel("Property_and_functionalities_List.xlsx", header=0)
print(len(df))

# Drop duplicate chemical names
# df = df.drop_duplicates(subset='Chemical Name', keep="last")
# print(len(df))
df = df.iloc[:1600]

# Set file header
# header = ['id, Chemical Name', 'Macthed Chemical', 'CAS', 'Synonyms', 'Molecular Formula', 'Molecular Weight', 'Density', 'Water Solubility']
header = ['id', 'Chemical Name', 'LogP (Partition coefficient)', 'LogS (water solubility of the ingredient)',
          'Molecular weight', 'Density', 'Chemical formula', 'Structure', 'Synonyms', 'Functionalities']

# Write to file
with open('chembk_1129_new_1.csv', 'w', encoding='UTF8', newline="") as f:
    try:
        writer = csv.writer(f)
        writer.writerow(header)

        count_e = 0
        for index, row in df.iterrows():
            synonyms = ""
            cas = ""
            formula = ""
            weight = ""
            density = ""
            water_solubility = ""

            chemical_name = row['Chemical Name'].title().replace("/", " ")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0',
            }
            url = "www.chembk.com/en/chem/" + chemical_name

            response = requests.get("https://" + urllib.parse.quote(url), headers=headers)

            soup = BeautifulSoup(response.text, 'html5lib')
            tables = soup.find_all('table')

            try:
                ## summary
                rows = tables[0].find_all('tr')
                for row in rows:
                    tds = row.find_all('td')
                    if tds[0].text == 'Synonyms':
                        synonyms = [a.text for a in tds[1].find_all('a')]
                        
                    # Grab CAS
                    if tds[0].text == "CAS":
                        cas = tds[1].text

                ## infos
                rows = tables[1].find_all('tr')
                for row in rows:
                    tds = row.find_all('td')
                    if tds[0].text == 'Molecular Formula':
                        formula = tds[1].text

                        
                    if tds[0].text == 'Molar Mass':
                        weight = tds[1].text
                        
                    # Grab Density
                    if tds[0].text == "Density":
                        density = tds[1].text

                    # Grab Water Solubility
                    if tds[0].text == "Water Solubility":
                        water_solubility = tds[1].text
                
                print(chemical_name, "Completed")
                writer.writerow([index, chemical_name, "", water_solubility,
                                weight, density, formula, "", synonyms, ""])
            except Exception as e:
                writer.writerow(
                    [index, chemical_name, "", "", "", "", "", "", ""])
                count_e += 1
                print("error" + str(count_e) + ": " +
                      chemical_name + " - " + str(e))
                continue

    except Exception as e:
        print(e)
