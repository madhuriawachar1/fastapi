
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
    return {'message': 'Hello, World'}

# 4. Route with a single parameter, returns the parameter within a message
#    Located at: http://127.0.0.1:8000/AnyNameHere
@app.get('/{name}')
def get_name(name: str):
    return {'Welcome To Krish Youtube Channel': f'{name}'}

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

    return sorted_transactions
@app.post('/predict')
def predict_banknote(data:Transaction):
    transaction_dict = data.model_dump()
    encryptedHexCardNo = transaction_dict['encryptedHexCardNo']
    merchantCategoryCode = transaction_dict['merchantCategoryCode']
    transactionAmount = transaction_dict['transactionAmount']
    latitude = transaction_dict['latitude']
    longitude = transaction_dict['longitude']
    cardBalance = transaction_dict['cardBalance']
    dateTimeTransaction=transaction_dict['dateTimeTransaction']
    new_format = '%Y-%m-%d %H:%M:%S'
    
    threshold_amount = 0.70 * cardBalance
    '''
    #RULE-001
    # Calculate 70% of the card balance
    
    dd=pd.read_csv('modified_dfv3-1_filtered.csv')
    past_transactions=get_past_transactions(dd, encryptedHexCardNo)
    # Filter past transactions within the last 12 hours
    time_limit = new_date_str - timedelta(hours=12)

# Now filter the transactions
    recent_transactions = [
        txn for txn in past_transactions
        if datetime.strptime(txn['dateTimeTransaction'], '%Y-%m-%d %H:%M:%S') > time_limit
    ]
    
    # Sum the amounts of these transactions
    total_amount = sum(txn['transactionAmount'] for txn in recent_transactions) + transactionAmount
'''
    # Check the rule condition: Total amount >= 70% of balance and balance >= 3,00,000
    if  transactionAmount>= threshold_amount :
        return {
        'prediction': "rule 001"
    }
    return {
        'prediction': "hello"
    }

# 5. Run the API with uvicorn
#    Will run on http://127.0.0.1:8000
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
    
#uvicorn app:app --reload