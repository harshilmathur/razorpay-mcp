import os
import razorpay
import json

# Initialize Razorpay client
key_id = os.environ.get('RAZORPAY_KEY_ID')
key_secret = os.environ.get('RAZORPAY_KEY_SECRET')

if not key_id or not key_secret:
    print("Error: Razorpay credentials not found in environment variables")
    exit(1)

client = razorpay.Client(auth=(key_id, key_secret))

# Test creating a plan
try:
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
    
    print("Attempting to create plan with data:")
    print(json.dumps(plan_data, indent=2))
    
    response = client.plan.create(plan_data)
    print("\nSuccess! Plan created:")
    print(json.dumps(response, indent=2))
    
except Exception as e:
    print(f"\nError creating plan: {str(e)}")
    
    # Try to print detailed error info
    if hasattr(e, 'error'):
        print(f"Error details: {e.error}")
    
# Test listing plans
try:
    print("\nAttempting to list all plans...")
    plans = client.plan.all()
    
    print("Success! Plans retrieved:")
    print(json.dumps(plans, indent=2))
    
except Exception as e:
    print(f"\nError listing plans: {str(e)}")
    
    # Try to print detailed error info
    if hasattr(e, 'error'):
        print(f"Error details: {e.error}")