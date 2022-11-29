# Import packages

from cmath import e
import pandas as pd
import csv

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Read CSV file into dataframe
df = pd.read_csv("cosing_clean.csv", header=0)
print(len(df))


# Set file header
header = ['id', 'Chemical Name', 'LogP (Partition coefficient)', 'LogS (water solubility of the ingredient)', 'Molecular weight', 'Density', 'Chemical formula', 'Structure', 'Synonyms', 'Functionalities']

# Setup Selenium web driver
def setupDriver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.chembk.com/en")
    return driver


# Enter searchbox
def search(index, driver):
    # The first one searched from home page, the rest searched from result page
    if index == 0:
        searchBox = driver.find_element(By.ID, "chem")
    else:
        driver.find_element(By.ID, "chem").clear()
        searchBox = driver.find_element(By.ID, "chem")

    searchBox.send_keys(chemical_name)
    searchBox.send_keys(Keys.ENTER)


# Mark properties as empty when no results found
def writeEmpty(writer, index, chemical_name):
    writer.writerow([index, chemical_name, "", "", "", "", "", "", "", ""])


# Extract information from Supplier Page
def extractSupplierPage(tds, driver, writer):
    for row in driver.find_elements(By.TAG_NAME, 'tr'):
        tds = row.find_elements(By.TAG_NAME, 'td')

        # Get formula
        if tds[0].text == "Chemical Formula":
            formula = tds[1].text

        # Get molecular weight
        if tds[0].text == "Molecular Weight":
            weight = tds[1].text
            break
        
    writer.writerow([index, chemical_name, "", water_solubility, weight, density, formula, "", synonyms, ""])
        
    driver.get("https://www.chembk.com/en")

# Main
if __name__ == '__main__':
    with open('chembk_1020_all.csv', 'w', encoding = 'UTF8', newline="") as f:
        try:
            writer = csv.writer(f)
            writer.writerow(header)

            # Setup Selenium web driver
            driver = setupDriver()

            count_e = 0
            for index, row in df.iterrows():
                try:
                    found = False

                    # Use chemical name as search keyword
                    # Remove slash in the string which cannot be put into search box
                    chemical_name = row['Chemical Name'].title().replace("/", " ")

                    # Initialization
                    macthed_name = ""
                    synonyms = ""
                    formula = ""
                    weight = ""
                    density = ""
                    water_solubility = ""

                    # Search
                    search(index, driver)

                    # -- Choose which page to move on -- 

                    trs = driver.find_elements(By.TAG_NAME, 'tr')
                    tds = driver.find_elements(By.TAG_NAME, 'td')

                    # If no table -> No Results found
                    if len(trs) == 0 or len(tds) == 0:   
                        writeEmpty(writer, index, chemical_name)
                        print(chemical_name + " : no results found.")
                        continue

                    # If exact name match found
                    if len(driver.find_elements(By.XPATH, '//a[@href="/en/chem/'+chemical_name+'"]')) == 1:
                        matched_name = chemical_name
                        nextPage = driver.find_element(By.XPATH, '//a[@href="/en/chem/'+chemical_name+'"]')
                        found = True
                        print(chemical_name + " : exact name found.")

                    # If no exact match, having multiple results:
                    #    1. See if the search name matches one of the Synonyms
                    if found == False:
                        tbodys = driver.find_elements(By.TAG_NAME, 'tbody')
                        trs = tbodys[0].find_elements(By.TAG_NAME, 'tr')
                        for tr in trs:
                            cols = tr.find_elements(By.TAG_NAME, 'td')
                            if len(cols) >= 5:   # make sure it is data, not some random row with tds
                                if chemical_name in cols[3].text:
                                    nextPage = cols[2].find_element(By.TAG_NAME, 'a')
                                    matched_name = cols[2].text
                                    found = True
                                    print(chemical_name + " : have matched synonym.")
                                    break

                    #    2. In the rest options, pick the first one with Molecular Formula shown
                    if found == False:
                        trs = driver.find_elements(By.TAG_NAME, 'tr')
                        for tr in trs:
                            cols = tr.find_elements(By.TAG_NAME, 'td')
                            if len(cols) >= 5:   # make sure it is data, not some random row with tds
                                if cols[4].text != "":
                                    nextPage = cols[2].find_element(By.TAG_NAME, 'a')
                                    matched_name = cols[2].text
                                    found = True
                                    print(chemical_name + " : pick the first one with molecular.")
                                    break

                    #    3. If no options showing Molecular Formula, pick the first one containing the chemical name as its substring of the results
                    if found == False:
                        if driver.find_elements(By.XPATH, '//a[contains(@href, "%s")]' % chemical_name):
                            options = driver.find_elements(By.XPATH, '//a[contains(@href, "%s")]' % chemical_name)
                            if len(options) > 1:
                                matched_name = options[1].text
                                nextPage = options[1]   # Skip option 0
                                found = True
                                print(chemical_name + " : pick the first one containing the chemical name.")
                                break

                    #  4. Pick the first one if no conditions matched.
                    if found == False:
                        tbodys = driver.find_elements(By.TAG_NAME, 'tbody')
                        if len(tbodys) != 0:
                            for tbody in tbodys:
                                trs = tbody.find_elements(By.TAG_NAME, 'tr')
                                if len(trs) != 0:                    
                                    tds = trs[0].find_elements(By.TAG_NAME, 'td')
                                    nextPage = tds[2].find_element(By.TAG_NAME, 'a')
                                    matched_name = tds[2].text
                                    print(chemical_name + " : pick the first one.")
                                    break

                    # If chemical found
                    nextPage.click()

                    # If the page found is a supplier page
                    if len(driver.find_elements(By.TAG_NAME, 'h4')) > 0:
                        if driver.find_elements(By.TAG_NAME, 'h4')[0].text == "Request for quotation":
                            extractSupplierPage(tds, driver, writer)
                            continue

                    # Extract info from header paragraph
                    formula = driver.find_elements(By.TAG_NAME, 'h4')[2].text.split(":")[1].strip()
                    weight =  driver.find_elements(By.TAG_NAME, 'h4')[3].text.split(":")[1].strip()

                    # Extract info from table
                    for row in driver.find_elements(By.TAG_NAME, 'tr'):
                        tds = row.find_elements(By.TAG_NAME, 'td')

                        # Grab Synonyms
                        if tds[0].text == "Synonyms":
                            syns = tds[1].find_elements(By.TAG_NAME, 'a')
                            for syn in syns:
                                if len(syn.text.split(",")) > 1:
                                    synonyms += syn.text + ","
                                else:
                                    synonyms += syn.text

                        # Grab Density
                        if tds[0].text == "Density":
                            density = tds[1].text

                        # Grab Water Solubility
                        if tds[0].text == "Water Solubility":
                            water_solubility = tds[1].text
                            break   # exit earlier if all the properties have found

                    writer.writerow([index, chemical_name, "", water_solubility, weight, density, formula, "", synonyms, ""])
                except Exception as e:
                    writer.writerow([index, chemical_name, "", "", "", "", "", "", ""])
                    count_e += 1
                    print("error" + str(count_e) + ": " + chemical_name + " - " + str(e))
                    continue
        except Exception as e:
            print(e)