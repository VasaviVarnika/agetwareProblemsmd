from flask import Flask, request, jsonify
import uuid
import json
import os

app = Flask(__name__)
DATA_FILE = 'loan_data.json'

# Load or initialize data
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
else:
    data = {"loans": {}}

def save_data():
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def home():
    return "Welcome to Bank Loan System API. Use /lend, /payment, /ledger/<id>, /overview/<customer_id>"


@app.route('/lend', methods=['POST'])
def lend():
    req = request.json
    customer_id = req['customer_id']
    P = req['loan_amount']
    N = req['loan_period']
    R = req['rate_of_interest']

    interest = (P * N * R) / 100
    total_amount = P + interest
    emi = round(total_amount / (N * 12), 2)

    loan_id = str(uuid.uuid4())
    loan = {
        "customer_id": customer_id,
        "principal": P,
        "interest": interest,
        "total_amount": total_amount,
        "emi": emi,
        "emi_left": int(N * 12),
        "amount_paid": 0,
        "transactions": []
    }
    data["loans"][loan_id] = loan
    save_data()
    return jsonify({"loan_id": loan_id, "total_amount": total_amount, "monthly_emi": emi})

@app.route('/payment', methods=['POST'])
def payment():
    req = request.json
    loan_id = req['loan_id']
    amount = req['amount']
    payment_type = req['type']  # 'emi' or 'lump'

    if loan_id not in data["loans"]:
        return jsonify({"error": "Loan ID not found"}), 404

    loan = data["loans"][loan_id]
    loan["transactions"].append({"type": payment_type, "amount": amount})

    if payment_type == 'emi':
        loan["amount_paid"] += amount
        loan["emi_left"] = max(0, loan["emi_left"] - 1)
    elif payment_type == 'lump':
        loan["amount_paid"] += amount
        remaining_amount = loan["total_amount"] - loan["amount_paid"]
        loan["emi_left"] = max(0, int(remaining_amount / loan["emi"])) if loan["emi"] > 0 else 0
    else:
        return jsonify({"error": "Invalid payment type"}), 400

    save_data()
    return jsonify({"message": "Payment recorded", "emi_left": loan["emi_left"], "amount_paid": loan["amount_paid"]})

@app.route('/ledger/<loan_id>', methods=['GET'])
def ledger(loan_id):
    if loan_id not in data["loans"]:
        return jsonify({"error": "Loan ID not found"}), 404

    loan = data["loans"][loan_id]
    balance = max(0, loan["total_amount"] - loan["amount_paid"])
    return jsonify({
        "transactions": loan["transactions"],
        "balance": balance,
        "monthly_emi": loan["emi"],
        "emi_left": loan["emi_left"]
    })

@app.route('/overview/<customer_id>', methods=['GET'])
def overview(customer_id):
    customer_loans = [loan for loan in data["loans"].values() if loan["customer_id"] == customer_id]
    result = []
    for loan in customer_loans:
        balance = max(0, loan["total_amount"] - loan["amount_paid"])
        result.append({
            "principal": loan["principal"],
            "total_amount": loan["total_amount"],
            "emi": loan["emi"],
            "interest": loan["interest"],
            "amount_paid": loan["amount_paid"],
            "emi_left": loan["emi_left"],
            "balance": balance
        })
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
