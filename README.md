# TCS-GMT-Graph

## Contents of the Repository:
1. Scraping(individuals) - The folder which contains separate scripts for each scraping source and generates output files for a given 'cosing_clean' file.
     - CompTox.py - This script contains the scraping code for scraping results from the CompTox database.
     - Pubchem Scraping.ipynb - This script contains the scraping code for Pubchem.
     - Scraping_script_ChemBK.py - This script contains scraping code for ChemBK.
     - Scraping_script_Wikipedia.py - This script contains scraping code for Wikipedia.
     - Scraping_script_other_sources.py - This script contains scraping code for other sources.
     - 
3. ScrapingResults - This folder contains all the output files from each source.
4. cleansingPipeline - This folder contains code to clean the input cosing data.
5. ScrapingPipeline.ipynb - This script is the overall master file which calls other scripts to extract properties and functionalities.
6. KnowledgeGraph.ipynb - This script contains functions to construct knowledge graphs based on properties and certain thresholds.
6. Wikipedia_AllFunctionalities.csv - The keyword file used to search for functionality in the Wikipedia text.
7. combiner.py - The file which combines outputs from multiple sources into one source.
8. cosing_clean.csv and cosing_clean.xlsx- The files which contain the cleaned chemical names.

## Data Cleaning
Process
1.Initially 3617 records in the file\
2.Smiles and Canonical_Smiles are 1 to 1 mapping, remove smiles\
3.Remove 241 duplicated rows\
4.Duplicated Canonical_Smiles: merge synonyms (414 rows)\
5.Duplicated Chemical Names with different smiles: leave it there\
6.Cleaned dataset: 2962 rows, 18 columns for web scraping

## Data Scraping
### CompTox
The CompTox Chemicals Dashboard provides public access to chemical data. It is a widely used resource for chemistry, toxicity, and exposure information for hundreds of thousands of chemicals.
- Source Link: [CompTox Dashboard](https://comptox.epa.gov/dashboard/)
- Data download: [CompTox data files](https://epa.figshare.com/articles/dataset/The_Chemical_and_Products_Database_CPDat_MySQL_Data_File/5352997)
#### Main steps:
1. Get unique identifier
   - Use chemical_dictionary_20201216.csv to find DTXSID (unique identifier) for each chemical from cosing data
3. Find functionalities
   - Use DTXSID to find corresponding functionalities in functional_use_dictionary_20201216.csv
5. Find properties
   - Download and install [web driver](https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/) to render from dynamic web page.
   - Use DTXSID to find corresponding properties in each url.
   - Urls are fomulated as: "https://comptox.epa.gov/dashboard/chemical/properties/" + DTXSID

### Pubchem
The Pubchem website provides properties, chemical uses, and a bunch of other information about chemical compounds and substances.
- Source link: https://pubchem.ncbi.nlm.nih.gov
#### Overall flow:
1. We get the substance id through the Pubchem API.
2. Construct a custom link to download the JSON.
3. We download the JSON itself from this link and store it locally.
4. We parse this JSON to extract properties and functionalities.

### ChemBK
ChemBK website provdies information such as molecular weight, density, chemical formula, and synonyms of certain chemicals.
We used BeautifulSoup to send request to the website and extract the properties by parsing the response.
- Source link: [ChemBK website](https://www.chembk.com/en)

#### Overall flow:
1. Read the clean chemical list file "clean_chemical_list.xlsx", which generated after the data cleaning process (eg. removing duplicates)
2. Send request to ChemBK by defining the URL using BeautifulSoup and parse the HTML table with information we need.
3. Save the extracted data to "ScrapingResults/Properties_ChemBK_new.csv"

### Wikipedia
Wikipedia can be a great source to extract properties from the table on its page, and funcitonalities from sections like 'Uses'.
- Source Link: https://www.wikipedia.org

### Overall Flow:
1. Get clean chemical name and try compiling a direct wikipedia link.
2. If link not found, go to the search bar using selenium and search for the name.
3. Go to the top result in the search.
4. Extract properties and functionalities.

## Data Integration
1. There should be four output propertiy files in the ScrapingResults folder after running the scraping scripts of each source.
2. Run the combiner.py file, which will combine the results into "Perperties_merged.csv" in the ScrapingResults folder.
