# TCS-GMT-Graph
## Data Cleaning

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

### Wikipedia
Wikipedia can be a great source to extract properties from the table on its page, and funcitonalities from sections like 'Uses'.
- Source Link: https://www.wikipedia.org
### Overall Flow:
1. Get clean chemical name and try compiling a direct wikipedia link.
2. If link not found, go to the search bar using selenium and search for the name.
3. Go to the top result in the search.
4. Extract properties and functionalities.



# Contents of the Repository:
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
6. Wikipedia_AllFunctionalities.csv - The keyword file used to search for functionality in the Wikipedia text.
7. combiner.py - The file which combines outputs from multiple sources into one source.
8. cosing_clean.csv and cosing_clean.xlsx- The files which contain the cleaned chemical names.
