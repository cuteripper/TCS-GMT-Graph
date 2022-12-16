# Import packages
import pandas as pd
import numpy as np


# Read data into dataframe and algin formats

# ChemBK
df_chembk = pd.read_csv("ScrapingResults/Properties_ChemBK_new.csv", header = 0)
df_chembk['Chemical Name'] = df_chembk['Chemical Name'].str.upper()

# Wikipedia
df_wiki = pd.read_excel("ScrapingResults/Properties_Wiki.xlsx", header = 0)
df_wiki = df_wiki.rename(columns={'Unnamed: 0': 'id'})
df_wiki = df_wiki[['id', 'Chemical Name', 'log P', 'Solubility in water', 'Molar mass', 'Density', 'Chemical formula', 'Structure']]
df_wiki['Synonyms'] = np.NAN
df_wiki['Functionalities'] = np.NAN
df_wiki = df_wiki.rename(columns={'Unnamed: 0': 'id', 'Molecular Weight': 'Molecular weight', 'log P':'LogP (Partition coefficient)', 
        'Solubility in water':'LogS (water solubility of the ingredient)'})

# Other sources (Tompox)
df_other = pd.read_excel("ScrapingResults/Properties_Other_Source.xlsx", header = 0)
df_other = df_other.rename(columns={'Unnamed: 0': 'id'})
df_other['LogP (Partition coefficient)'] = np.NAN
df_other = df_other[['id', 'INPUT', 'LogP (Partition coefficient)','solubility', 'AVERAGE_MASS', 'Density', 'MOLECULAR_FORMULA', 'SMILES', 
            'Synonyms', 'Functionalities']]
df_other = df_other.rename(columns = {'INPUT': 'Chemical Name', 'solubility': 'LogS (water solubility of the ingredient)', 'AVERAGE_MASS':'Molecular weight', 
        'MOLECULAR_FORMULA': 'Chemical formula', 'SMILES':'Structure'})
df_other = df_other.drop_duplicates("Chemical Name")

# PubChem 
df_pubchem = pd.read_csv("ScrapingResults/Pubchem_properties.csv", header = 0)
df_pubchem = df_pubchem.drop(df_pubchem.columns[4:], axis=1)
df_pubchem = df_pubchem.rename(columns={'Unnamed: 0': 'id', 'Name': 'Chemical Name','Molecular Weight': 'Molecular weight', 'XLogP3':'LogP (Partition coefficient)'})
df_pubchem = df_pubchem.reindex(columns = df_pubchem.columns.tolist() + ['LogS (water solubility of the ingredient)', 'Density', 'Chemical formula', 'Structure', 'Synonyms', 'Functionalities'])
df_pubchem = df_pubchem[['id', 'Chemical Name', 'LogP (Partition coefficient)', 'LogS (water solubility of the ingredient)', 
        'Molecular weight', 'Density', 'Chemical formula', 'Structure', 'Synonyms', 'Functionalities']]

# Examine dataframes
print(df_chembk.head())
print(df_chembk.shape)  # shape(3256, 10)

print(df_wiki.head())
print(df_wiki.shape)    # shape(3256, 10)

print(df_other.head())
print(df_other.shape)   # shape(3256, 10)

print(df_pubchem.head())
print(df_pubchem.shape)  # shape(93, 10)

# Merging datasets
df_chembk = df_chembk.set_index('Chemical Name')
df_wiki = df_wiki.set_index('Chemical Name')
df_other = df_other.set_index('Chemical Name')

# Fill NAs with other data sources
df_chembk_wiki = df_chembk.fillna(df_wiki)
df_merged = df_chembk_wiki.fillna(df_other)

# Examine remaining NAs
df_chembk_wiki.isna().sum()
df_merged.isna().sum()

# Output result
df_merged.reset_index().set_index('id').to_csv("ScrapingResults/Properties_merged.csv")