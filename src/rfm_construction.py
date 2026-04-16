import pandas as pd

def load_data(path):
    return pd.read_csv(path)

# ----------------------------------------------
# Create recency, frequency and monetary metrics and stores them in a new df
# ----------------------------------------------
def build_rfm_table(df):
    df = df.copy()
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

    snapshot_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)

    rfm = df.groupby('Customer ID').agg({
        'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
        'Invoice': 'count',
        'TotalPrice': 'sum'
    })

    rfm.columns = ['Recency', 'Frequency', 'Monetary']

    return rfm

def main(path):
    print(f"Path: {path}")

    df_clean = load_data(path)
    print("The clean dataset has been loaded \n")
    
    df_rfm = build_rfm_table(df_clean)
    print("The RFM metrics have been calculated and stored \n")

    return df_rfm

if __name__ == "__main__":
    clean_path = "../data_clean/clean_online_retail.csv"
    rfm_path = "../data_raw/raw_rfm_metrics.csv"
    df_rfm = main(clean_path)
    df_rfm.to_csv(rfm_path, index=False)