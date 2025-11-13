# Sample Data

This directory contains sample transactions for testing the fraud detection system.

## Files

- **sample_transactions.json**: Collection of test transactions covering various fraud scenarios

## Fraud Scenarios Covered

1. **Normal Transactions**: Regular everyday purchases
2. **Credit Card Fraud**: Large amounts, unusual locations, new devices
3. **Money Laundering**: Structuring, offshore transfers
4. **Card Testing**: Small test transactions followed by large purchases
5. **Account Takeover**: New device, changed patterns

## Using Sample Data

```python
import json

with open('data/samples/sample_transactions.json', 'r') as f:
    transactions = json.load(f)

# Test with API
for txn in transactions:
    response = requests.post('http://localhost:8000/api/analyze/transaction', json=txn)
    print(f"{txn['transaction_id']}: {response.json()['is_fraudulent']}")
```

## Expected Results

Each sample transaction includes an `expected_result` field indicating what the fraud detection system should identify.
