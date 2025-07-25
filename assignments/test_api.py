import requests

# Test LEND API
url = 'http://127.0.0.1:5000/lend'
payload = {
    "customer_id": "cust001",
    "loan_amount": 10000,
    "loan_period": 2,
    "rate_of_interest": 5
}

response = requests.post(url, json=payload)
print("LEND API Response:", response.json())

# Store loan_id from response
loan_id = response.json()['loan_id']

# Test PAYMENT API
payment_url = 'http://127.0.0.1:5000/payment'
payment_payload = {
    "loan_id": loan_id,
    "amount": 500,
    "type": "emi"
}
payment_response = requests.post(payment_url, json=payment_payload)
print("PAYMENT API Response:", payment_response.json())

# Test LEDGER API
ledger_url = f'http://127.0.0.1:5000/ledger/{loan_id}'
ledger_response = requests.get(ledger_url)
print("LEDGER API Response:", ledger_response.json())

# Test OVERVIEW API
overview_url = 'http://127.0.0.1:5000/overview/cust001'
overview_response = requests.get(overview_url)
print("OVERVIEW API Response:", overview_response.json())
