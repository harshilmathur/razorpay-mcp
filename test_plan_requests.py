import requests
import json

# MCP endpoint URL
mcp_url = "http://localhost:5000/mcp"

# Test metadata request
def test_metadata():
    payload = {
        "type": "metadata"
    }
    
    print("Testing metadata request...")
    response = requests.post(mcp_url, json=payload)
    
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        print("Metadata response:")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error: {response.text}")
    
    print("\n" + "-"*40 + "\n")

# Test plans_list tool request
def test_plans_list():
    payload = {
        "type": "tool",
        "name": "plans_list",
        "parameters": {
            "count": 10
        }
    }
    
    print("Testing plans_list tool...")
    response = requests.post(mcp_url, json=payload)
    
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        print("Plans list response:")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error: {response.text}")
    
    print("\n" + "-"*40 + "\n")

# Test plan_create tool request
def test_plan_create():
    payload = {
        "type": "tool",
        "name": "plan_create",
        "parameters": {
            "period": "monthly",
            "interval": 1,
            "item": {
                "name": "Test Plan via MCP",
                "amount": 79900,
                "currency": "INR",
                "description": "Test Monthly Plan via MCP Server"
            },
            "notes": {
                "test": "true",
                "created_via": "mcp_server"
            }
        }
    }
    
    print("Testing plan_create tool...")
    response = requests.post(mcp_url, json=payload)
    
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        print("Plan create response:")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error: {response.text}")
    
    print("\n" + "-"*40 + "\n")

# Test subscriptions_list tool request
def test_subscriptions_list():
    payload = {
        "type": "tool",
        "name": "subscriptions_list",
        "parameters": {
            "count": 10
        }
    }
    
    print("Testing subscriptions_list tool...")
    response = requests.post(mcp_url, json=payload)
    
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        print("Subscriptions list response:")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error: {response.text}")
    
    print("\n" + "-"*40 + "\n")

if __name__ == "__main__":
    # Run the tests
    test_metadata()
    test_plans_list()
    test_plan_create()
    test_subscriptions_list()