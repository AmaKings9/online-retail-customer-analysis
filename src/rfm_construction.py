import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

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

# ----------------------------------------------
# Preprocess RFM (log transformation + scaling)
# ----------------------------------------------
def preprocess_rfm(df_rfm):
    df = df_rfm.copy()

    # Log transformation
    df['Frequency_log'] = np.log1p(df['Frequency'])
    df['Monetary_log'] = np.log1p(df['Monetary'])

    # Select features for scaling
    features = df[['Recency', 'Frequency_log', 'Monetary_log']]

    # Scaling
    scaler = StandardScaler()
    scaled_values = scaler.fit_transform(features)

    df_scaled = pd.DataFrame(
        scaled_values,
        columns=['Recency', 'Frequency', 'Monetary'],
        index=df.index
    )

    return df_scaled

def main(path):
    print(f"Path: {path}")

    df_clean = load_data(path)
    print("The clean dataset has been loaded \n")
    
    df_rfm = build_rfm_table(df_clean)
    print("The RFM metrics have been calculated and stored \n")

    df_rfm_scaled = preprocess_rfm(df_rfm)
    print("RFM preprocessing (log + scaling) completed \n")

    return df_rfm, df_rfm_scaled

if __name__ == "__main__":
    clean_path = "../data_clean/clean_online_retail.csv"
    rfm_path = "../data_raw/raw_rfm_metrics.csv"
    rfm_scaled_path = "../data_clean/rfm_scaled.csv"

    df_rfm, df_rfm_scaled = main(clean_path)

    df_rfm.to_csv(rfm_path, index=False)
    df_rfm_scaled.to_csv(rfm_scaled_path, index=False)