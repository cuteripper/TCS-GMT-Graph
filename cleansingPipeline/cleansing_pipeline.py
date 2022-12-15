import pandas as pd
import numpy as np


def data_overview(df):
     """get null and duplicate values and print the count
      Args:
          df (DataFrame): Cosing dataframe
    """
    print(df.head())
    print(df.isna().sum())
    print("Duplicate Count")
    for col_name in df.columns:
        if not col_name.startswith("Func"):
            print(col_name, ":", df[col_name].duplicated(keep=False).sum())
    print(df[df.alias.isna() == False].alias)    
    

def remove_duplicate_smiles(df):
     """remove ingredients with duplicate smiles
      Args:
          df (DataFrame): Cosing dataframe without duplicate and null values
      Returns:
          res: Cosing clean dataframe without duplicate smiles instances.
    """
    df["alias"] = np.nan
    print(df.isna().sum())
    print(df.shape)
    smiles_table = {}
    for i in range(len(df)):
        cur_row = df.iloc[i]
        smile = cur_row["Smiles"]
        if smile not in smiles_table:
            smiles_table[smile] = i
        else:
            funcs = (col for col in df.columns if col.startswith("Func"))
            first_row = df.iloc[smiles_table[smile]]
            first_row_nan_funcs = (func for func in funcs if pd.isnull(first_row[func]))
            cur_row_notnan_funcs = (func for func in funcs if not pd.isnull(cur_row[func]))
            for func in cur_row_notnan_funcs:
                try:
                    first_row[next(first_row_nan_funcs)] = cur_row[func]
                    df.iloc[smiles_table[smile]] = first_row
                except StopIteration:
                    break
            aliases = "" if pd.isnull(first_row["alias"]) else (first_row["alias"] + "/")
            first_row["alias"] = aliases + cur_row["Chemical Name"]
            df.iloc[smiles_table[smile]] = first_row
    print(df.isna().sum())
    df = df[df["Smiles"].duplicated() == False]
    print(df.shape)
    return df


def do_cleansing(df):
    """cleansing dataframe and saving unique chemical names to provide it to scrappers
      Args:
          df (DataFrame): Cosing clean dataframe
      Returns:
          res: Cosing clean dataframe without duplicate smiles instances.
    """
    df.index = df.index.astype(int)
    df.drop_duplicates(inplace=True)
    df = remove_duplicate_smiles(df)
    df.drop('Smiles',axis=1, inplace=True)
    with pd.ExcelWriter("Ingred_v2.xlsx") as writer:
        Chem_Name_1['Chemical Name'].to_excel(writer, sheet_name='Unique chemical name', index=False)
        Chem_Name_2['Chemical Name'].to_excel(writer, sheet_name='Unique Canonical_smiles', index=False)
    return df


if __name__ == "__main__":
    df = pd.read_excel("cosing_clean.xlsx", index_col=0)
    df = do_cleansing(df)
    data_overview(df)
