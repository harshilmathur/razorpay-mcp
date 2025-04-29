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

# Try to list plans
print(f"Sending GET request to URL: {plans_url}")
print("With headers:", json.dumps(headers, indent=2).replace(auth_token, "***AUTH_TOKEN***"))

try:
    response = requests.get(plans_url, headers=headers)
    print(f"\nResponse status code: {response.status_code}")
    
    if response.status_code == 200:
        print("\nSuccess! Plans retrieved successfully.")
        data = response.json()
        print(f"Count: {data.get('count', 'N/A')}")
        print(f"Items: {json.dumps(data.get('items', []), indent=2)}")
    else:
        print(f"Response headers: {dict(response.headers)}")
        print(f"Response body: {response.text}")
    
except Exception as e:
    print(f"\nException occurred: {str(e)}")

# Try creating a plan
print("\n--------\nTesting Create Plan\n--------")
create_plan_data = {
    "period": "monthly",
    "interval": 1,
    "item": {
        "name": "Test Plan via Python",
        "amount": 99900,
        "currency": "INR",
        "description": "Test Monthly Subscription Plan"
    },
    "notes": {
        "test": "true",
        "purpose": "testing"
    }
}

print(f"Sending POST request to URL: {plans_url}")
print("With data:", json.dumps(create_plan_data, indent=2))

try:
    response = requests.post(plans_url, headers=headers, json=create_plan_data)
    print(f"\nResponse status code: {response.status_code}")
    
    if response.status_code == 200:
        print("\nSuccess! Plan created successfully.")
        data = response.json()
        print(f"Created plan: {json.dumps(data, indent=2)}")
    else:
        print(f"Response headers: {dict(response.headers)}")
        print(f"Response body: {response.text}")
    
except Exception as e:
    print(f"\nException occurred: {str(e)}")