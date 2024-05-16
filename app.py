
from datetime import datetime, timedelta
# 1. Library imports
import uvicorn
from fastapi import FastAPI
from Transactions import Transaction
import numpy as np
import pickle
import pandas as pd
# 2. Create the app object
app = FastAPI()
import pandas as pd

from sklearn.ensemble import IsolationForest

# Feature Engineering for Rule 003
def feature_engineering_transaction_pattern(transactions):
    # Extract relevant features
    transactions['dateTimeTransaction'] = pd.to_datetime(transactions['dateTimeTransaction'])
    transactions['hour'] = transactions['dateTimeTransaction'].dt.hour
    transactions['day_of_week'] = transactions['dateTimeTransaction'].dt.dayofweek
    transactions['transactionAmount'] = transactions['transactionAmount']
    # Add more features as needed
    
    return transactions[['transactionAmount', 'hour', 'day_of_week']]  # Select relevant features

# Feature Engineering for Rule 004
def feature_engineering_merchant_category_code(transactions):
    # Group transactions by merchant category code
    grouped_transactions = transactions.groupby('merchantCategoryCode')
    
    # Calculate statistics for each merchant category code (e.g., average transaction amount)
    statistics = grouped_transactions['transactionAmount'].mean()  # Adjust for other statistics as needed
    
    return statistics

# Rule 003: Transaction Pattern Coherence
def detect_anomalies_transaction_pattern(transactions):
    # Feature Engineering
    features = feature_engineering_transaction_pattern(transactions)
    
    # Model Training
    model = IsolationForest(contamination=0.1)  # Adjust contamination based on expected anomaly rate
    model.fit(features)
    
    # Anomaly Detection
    predictions = model.predict(features)
    anomalies = predictions == -1
    
    return anomalies

# Rule 004: Coherence with Merchant Category Code
def detect_anomalies_merchant_category_code(transactions):
    # Feature Engineering
    statistics = feature_engineering_merchant_category_code(transactions)
    
    # Anomaly Detection
    anomalies = []  # List to store detected anomalies
    for index, row in transactions.iterrows():
        # Compare transaction amount with average for its merchant category code
        avg_transaction_amount = statistics.get(row['merchantCategoryCode'], 0)  # Default to 0 if no statistics found
        if row['transactionAmount'] > 2 * avg_transaction_amount:
            anomalies.append(True)
        else:
            anomalies.append(False)
    
    return anomalies


# 3. Index route, opens automatically on http://127.0.0.1:8000
@app.get('/')
def index():
    return {'message': 'Welcome to Real-Time Fraud Detection API by Madhuri'}

# 4. Route with a single parameter, returns the parameter within a message
#    Located at: http://127.0.0.1:8000/AnyNameHere
'''@app.get('/{name}')
def get_name(name: str):
    return {'Welcome To Krish Youtube Channel': f'{name}'}
'''
# 3. Expose the prediction functionality, make a prediction from the passed
#    JSON data and return the predicted Bank Note with the confidence
def load_transactions(filename):
    return pd.read_csv(filename)

# RULE:001Get past transactions for a specific encryptedHexCardNo
def get_past_transactions(data, card_no):
    # Filter the data for the specific card number
    filtered_data = data[data['encryptedHexCardNo'] == card_no]

    # Convert dateTimeTransaction to datetime type for sorting
    filtered_data['dateTimeTransaction'] = pd.to_datetime(filtered_data['dateTimeTransaction'])

    # Sort the transactions by dateTimeTransaction
    sorted_transactions = filtered_data.sort_values('dateTimeTransaction')
    print(sorted_transactions)
    print(sorted_transactions.columns)
    print(sorted_transactions['dateTimeTransaction'])
    print(type(sorted_transactions))
    return sorted_transactions

#RULE:002
from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees).
    """
    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    haversine_distance = 2 * asin(sqrt(a)) * 6371  # Radius of earth in kilometers. Use 3956 for miles
    return haversine_distance

@app.post('/predict')
def predict_transaction(data:Transaction):
    transaction_dict = data.model_dump()
    print(type(transaction_dict))
    encryptedHexCardNo = transaction_dict['encryptedHexCardNo']
    merchantCategoryCode = transaction_dict['merchantCategoryCode']
    transactionAmount = transaction_dict['transactionAmount']
    latitude = transaction_dict['latitude']
    longitude = transaction_dict['longitude']
    cardBalance = transaction_dict['cardBalance']
    dateTimeTransaction=transaction_dict['dateTimeTransaction']
    dateyr=dateTimeTransaction[4:8]
    
    format2=dateyr+"-"+dateTimeTransaction[2:4]+"-"+dateTimeTransaction[0:2]+" "+dateTimeTransaction[8:10]+":"+dateTimeTransaction[10:12]+":"+'00'
    
    date_obj = datetime.strptime(format2, '%Y-%m-%d %H:%M:%S')
   
    
    
    
    #RULE-001
    # Calculate 70% of the card balance
    threshold_amount = 0.70 * cardBalance
    dd=pd.read_csv('modified_dfv3-1_filtered.csv')
    past_transactions=get_past_transactions(dd, encryptedHexCardNo)
    print(past_transactions)
    print(past_transactions.columns)
        
    
    # Filter past transactions within the last 12 hours
    time_limit = pd.Timestamp(date_obj - timedelta(hours=12))
    #print(type(time_limit))
    #Name: dateTimeTransaction, dtype: datetime64[ns]
# Now filter the transactions
    recent_transactions = past_transactions[past_transactions['dateTimeTransaction'] > time_limit]


    rule_violated = []
    #RULE!-001
    total_amount = recent_transactions['transactionAmount'].sum() + transactionAmount
    if total_amount >= threshold_amount and cardBalance >= 300000:
        rule_violated.append("RULE-001")
       

    
    #RULE:002
    unique_locations = []
    for index, txn in recent_transactions.iterrows():
        current_location = (txn['latitude'], txn['longitude'])
        if all(haversine(loc[1], loc[0], current_location[1], current_location[0]) > 200 for loc in unique_locations):
            unique_locations.append(current_location)
    total_amount = recent_transactions['transactionAmount'].sum()
    if total_amount > 100000 and len(unique_locations) > 5:
        rule_violated.append("RULE-002")
      
    # Apply Rule 003
    transactions_df = pd.DataFrame.from_dict(transaction_dict)

    anomalies_transaction_pattern = detect_anomalies_transaction_pattern(transactions_df)
    
    # Apply Rule 004
    anomalies_merchant_category_code = detect_anomalies_merchant_category_code(transactions_df)
    
    # Construct response based on detected anomalies
    rule_violated = []
    if any(anomalies_transaction_pattern):
        rule_violated.append("RULE-003")
    if any(anomalies_merchant_category_code):
        rule_violated.append("RULE-004")    
    #RULE:003    
        
    # Response construction
    if rule_violated:
        response = {
            "status": "ALERT",
            "ruleViolated": rule_violated,
            "timestamp": str(int(datetime.now().timestamp()))
        }
    else:
        response = {
            "status": "OK",
            "ruleViolated": [],
            "timestamp": str(int(datetime.now().timestamp()))
        }
    return response

    
# 5. Run the API with uvicorn
#    Will run on http://127.0.0.1:8000
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
    
#uvicorn app:app --reload