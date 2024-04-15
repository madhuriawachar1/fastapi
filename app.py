
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

# Get past transactions for a specific encryptedHexCardNo
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
@app.post('/predict')
def predict_transaction(data:Transaction):
    transaction_dict = data.model_dump()
    encryptedHexCardNo = transaction_dict['encryptedHexCardNo']
    merchantCategoryCode = transaction_dict['merchantCategoryCode']
    transactionAmount = transaction_dict['transactionAmount']
    latitude = transaction_dict['latitude']
    longitude = transaction_dict['longitude']
    cardBalance = transaction_dict['cardBalance']
    dateTimeTransaction=transaction_dict['dateTimeTransaction']
    dateyr=dateTimeTransaction[4:8]
    
    format2=dateyr+"-"+dateTimeTransaction[2:4]+"-"+dateTimeTransaction[0:2]+" "+dateTimeTransaction[8:10]+":"+dateTimeTransaction[10:12]+":"+'00'
   # date_int1=int(dateTimeTransaction)
    #convert into suitable format
    # Convert string to datetime
    
    date_obj = datetime.strptime(format2, '%Y-%m-%d %H:%M:%S')
   
    
    
    
    #RULE-001
    # Calculate 70% of the card balance
    threshold_amount = 0.70 * cardBalance
    dd=pd.read_csv('modified_dfv3-1_filtered.csv')
    past_transactions=get_past_transactions(dd, encryptedHexCardNo)
       
    
    # Filter past transactions within the last 12 hours
    time_limit = pd.Timestamp(date_obj - timedelta(hours=12))
    print(type(time_limit))
    #Name: dateTimeTransaction, dtype: datetime64[ns]
# Now filter the transactions
    recent_transactions = past_transactions[past_transactions['dateTimeTransaction'] > time_limit]

    # Sum the amounts of these transactions
    total_amount = recent_transactions['transactionAmount'].sum() + transactionAmount

    # Check the rule condition: Total amount >= 70% of balance and balance >= 3,00,000
    if total_amount >= threshold_amount and cardBalance >= 300000:
        response = {
        "status": "ALERT",
        "ruleViolated": ["RULE-001"],  # Add other rule codes if other rules are checked and violated
        "timestamp": str(int(datetime.now().timestamp()))  # Unix timestamp as a string
    }
    else:
        response = {
        "status": "OK",
        #"ruleViolated": ["rule2"],  # No rules violated
        "timestamp": str(int(datetime.now().timestamp()))  # Unix timestamp as a string
    }
    return response

# 5. Run the API with uvicorn
#    Will run on http://127.0.0.1:8000
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
    
#uvicorn app:app --reload