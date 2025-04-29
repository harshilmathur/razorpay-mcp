import os
import requests
import json
import base64

# Get Razorpay credentials
key_id = os.environ.get('RAZORPAY_KEY_ID')
key_secret = os.environ.get('RAZORPAY_KEY_SECRET')

if not key_id or not key_secret:
    print("Error: Razorpay credentials not found in environment variables")
    exit(1)

# Prepare authentication
auth_token = base64.b64encode(f"{key_id}:{key_secret}".encode()).decode('ascii')
headers = {
    'Authorization': f'Basic {auth_token}',
    'Content-Type': 'application/json'
}

# API endpoint for plans
base_url = 'https://api.razorpay.com/v1'
plans_url = f'{base_url}/plans'

# Test plan data
plan_data = {
    'period': 'monthly',
    'interval': 1,
    'item': {
        'name': 'Test Premium Plan',
        'amount': 99900,
        'currency': 'INR',
        'description': 'Test Premium Monthly Subscription'
    },
    'notes': {
        'test': 'true',
        'purpose': 'testing'
    }
}

# Create plan
print(f"Sending POST request to URL: {plans_url}")
print("With headers:", json.dumps(headers, indent=2).replace(auth_token, "***AUTH_TOKEN***"))
print("And data:", json.dumps(plan_data, indent=2))

try:
    response = requests.post(plans_url, headers=headers, json=plan_data)
    print(f"\nResponse status code: {response.status_code}")
    print(f"Response headers: {response.headers}")
    print(f"Response body: {response.text}")
    
    if response.status_code == 200:
        print("\nSuccess! Plan created successfully.")
    
except Exception as e:
    print(f"\nException occurred: {str(e)}")

# List plans
print("\n--------\nListing Plans\n--------")
print(f"Sending GET request to URL: {plans_url}")

try:
    response = requests.get(plans_url, headers=headers)
    print(f"\nResponse status code: {response.status_code}")
    print(f"Response headers: {response.headers}")
    print(f"Response body: {response.text}")
    
    if response.status_code == 200:
        print("\nSuccess! Plans retrieved successfully.")
    
except Exception as e:
    print(f"\nException occurred: {str(e)}")