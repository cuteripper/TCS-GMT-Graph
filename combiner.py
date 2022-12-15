# Import packages
import pandas as pd
import numpy as np


# Read data into dataframe
# Data Cleaning
df_chembk = pd.read_csv("ScrapingResults/Properties_ChemBK_new.csv", header = 0)
df_chembk['Chemical Name'] = df_chembk['Chemical Name'].str.upper()
df_wiki = pd.read_excel("ScrapingResults/Properties_Wiki_new.xlsx", header = 0)
df_wiki['Functionalities'] = np.NAN
df_wiki = df_wiki.rename(columns={'Unnamed: 0': 'id'})
df_other = pd.read_excel("ScrapingResults/Properties_Other_Source_new.xlsx", header = 0)
df_other = df_other.rename(columns={'Id': 'id'})
df_other = df_other.drop_duplicates("Chemical Name")

# Examine df
print(df_chembk.head())
print(df_chembk.shape)

print(df_wiki.head())
print(df_wiki.shape)

print(df_other.head())
print(df_other.shape)

# Merging datasets
df_chembk = df_chembk.set_index('Chemical Name')
df_wiki = df_wiki.set_index('Chemical Name')
df_other = df_other.set_index('Chemical Name')

df_other.head()

# Fill NAs with other data sources
df_chembk_wiki = df_chembk.fillna(df_wiki)
df_merged = df_chembk_wiki.fillna(df_other)

# Examine remaining NAs
df_chembk_wiki.isna().sum()
df_merged.isna().sum()

# Output result
df_merged.reset_index().set_index('id').to_csv("ScrapingResults/Properties_merged.csv")