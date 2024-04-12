import pandas as pd
import numpy as np

# Load the dataset
df = pd.read_csv('dfv3-1.csv')

# Rename selected columns as specified
df.rename(columns={
    'cc_num': 'encryptedHexCardNo',
    'trans_date_trans_time': 'dateTimeTransaction',
    'merchant': 'merchantCategoryCode',
    'amt': 'transactionAmount',
    'lat': 'latitude',
    'long': 'longitude'
}, inplace=True)

# Add 'cardBalance' column where each 'cardBalance' is at least 70% greater than 'transactionAmount'
df['cardBalance'] = df['transactionAmount'] / (1 - 0.70)
# Optionally add a random extra amount to make balances more realistic
df['cardBalance'] += np.random.uniform(1000, 50000, len(df))
df['cardBalance'] = df['cardBalance'].round(2)

# Select only the required columns to save in the new dataset
columns_needed = [
    'encryptedHexCardNo',
    'dateTimeTransaction',
    'merchantCategoryCode',
    'transactionAmount',
    'latitude',
    'longitude',
    'cardBalance',
    'is_fraud'
]
df = df[columns_needed]

# Save the modified DataFrame back to a CSV file
df.to_csv('modified_dfv3-1_filtered.csv', index=False)

print("Modifications applied and saved to 'modified_dfv3-1_filtered.csv'.")
