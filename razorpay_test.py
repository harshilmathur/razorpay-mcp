#!/usr/bin/env python3
import razorpay
import inspect

# Create a test client with dummy credentials
client = razorpay.Client(auth=('test', 'test'))

# Print information about settlement methods
print("=== SETTLEMENT METHODS ===")
for name, method in inspect.getmembers(client.settlement, predicate=inspect.ismethod):
    if not name.startswith('_'):  # Skip private methods
        try:
            signature = str(inspect.signature(method))
            print(f"{name}{signature}")
        except:
            print(f"{name}()")

# Print information about subscription methods
print("\n=== SUBSCRIPTION METHODS ===")
for name, method in inspect.getmembers(client.subscription, predicate=inspect.ismethod):
    if not name.startswith('_'):  # Skip private methods
        try:
            signature = str(inspect.signature(method))
            print(f"{name}{signature}")
        except:
            print(f"{name}()")