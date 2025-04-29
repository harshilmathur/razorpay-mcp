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

# API endpoints
base_url = 'https://api.razorpay.com/v1'
settlements_url = f'{base_url}/settlements'

# Try to list settlements
print(f"Sending GET request to URL: {settlements_url}")
print("With headers:", json.dumps(headers, indent=2).replace(auth_token, "***AUTH_TOKEN***"))

try:
    response = requests.get(settlements_url, headers=headers)
    print(f"\nResponse status code: {response.status_code}")
    
    if response.status_code == 200:
        print("\nSuccess! Settlements retrieved successfully.")
        data = response.json()
        print(f"Count: {data.get('count', 'N/A')}")
        print(f"Items: {json.dumps(data.get('items', []), indent=2)}")
    else:
        print(f"Response headers: {dict(response.headers)}")
        print(f"Response body: {response.text}")
    
except Exception as e:
    print(f"\nException occurred: {str(e)}")