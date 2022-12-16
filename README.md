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

## Wikipedia
