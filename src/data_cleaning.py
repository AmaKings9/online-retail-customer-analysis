import pandas as pd

def load_data(path):
    return pd.read_csv(path)

def remove_missing_values(df):
    return df.dropna(subset=['Customer ID'])

def filter_valid_transactions(df):
    return df[(df['Quantity'] > 0) & (df['Price'] > 0)]

def remove_duplicates(df):
    cols = ['Invoice', 'StockCode', 'Quantity', 'InvoiceDate', 'Price', 'Customer ID', 'Country']
    return df.drop_duplicates(subset=cols)

def data_type_conversion(df):
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df['Customer ID'] = df['Customer ID'].astype('Int64')
    return df

def create_features(df):
    df['TotalPrice'] = df['Quantity'] * df['Price']
    return df

def main(path):
    print(f"Path: {path}")

    df_orig = load_data(path)
    print("The dataset has been loaded \n")
    print(f"Initial number of rows: {len(df_orig)} \n")

    df_v1 = remove_missing_values(df_orig)
    print(f"{len(df_orig) - len(df_v1)} missing values have been removed \n")

    df_v2 = filter_valid_transactions(df_v1)
    print(f"{len(df_v1) - len(df_v2)} invalid rows have been filtered \n")

    df_v3 = remove_duplicates(df_v2)
    print(f"{len(df_v2) - len(df_v3)} duplicated rows have been removed \n")

    df_v4 = data_type_conversion(df_v3)
    print("InvoiceDate column has been converted from string to datetime \n")
    print("Customer ID column has been converted from float to int \n")

    df_v5 = create_features(df_v4)
    print("The TotalPrice column has been created \n")

    print(f"Number of rows after cleaning: {len(df_v5)} \n")
    print(f"Total number of deleted rows: {len(df_orig) - len(df_v5)} \n")

    return df_v5

if __name__ == "__main__":
    raw_path = "../data_raw/online_retail_II.csv"
    clean_path = "../data_clean/clean_online_retail.csv"
    df_clean = main(raw_path)
    df_clean.to_csv(clean_path, index=False)