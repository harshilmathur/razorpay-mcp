#!/usr/bin/env python3
"""
Razorpay MCP Server - Official SDK implementation

A clean, efficient Model Context Protocol server that integrates Razorpay's payment
processing capabilities with Claude AI. Uses the official MCP SDK with proper formatting
for all identifiers.
"""
import os
import sys
import json
import logging
from typing import Any, Dict

from razorpay_client import RazorpayClient

# Import FastMCP components
from mcp.server.fastmcp import FastMCP
from mcp.types import Resource, Prompt

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s', stream=sys.stderr)
logger = logging.getLogger("razorpay-mcp-server")

# Initialize Razorpay client
razorpay_client = RazorpayClient()

# Define async handlers for each tool
async def get_payment(arguments):
    payment_id = arguments.get("payment_id")
    logger.info(f"Executing get_payment with payment_id: {payment_id}")
    return razorpay_client.get_payment({"id": payment_id})

async def list_payments(arguments):
    logger.info(f"Executing list_payments with arguments: {arguments}")
    return razorpay_client.list_payments(arguments)

async def create_order(arguments):
    logger.info(f"Executing create_order with arguments: {arguments}")
    return razorpay_client.create_order(arguments)

async def get_order(arguments):
    order_id = arguments.get("order_id")
    logger.info(f"Executing get_order with order_id: {order_id}")
    return razorpay_client.get_order({"id": order_id})

async def list_orders(arguments):
    logger.info(f"Executing list_orders with arguments: {arguments}")
    return razorpay_client.list_orders(arguments)

async def create_customer(arguments):
    logger.info(f"Executing create_customer with arguments: {arguments}")
    return razorpay_client.create_customer(arguments)

async def get_customer(arguments):
    customer_id = arguments.get("customer_id")
    logger.info(f"Executing get_customer with customer_id: {customer_id}")
    return razorpay_client.get_customer({"id": customer_id})

async def create_payment_link(arguments):
    logger.info(f"Executing create_payment_link with arguments: {arguments}")
    link_params = arguments.copy()
    if "customer" in link_params:
        # Format customer info for the client
        customer = link_params.pop("customer", {})
        if "name" in customer:
            link_params["customer_name"] = customer["name"]
        if "email" in customer:
            link_params["customer_email"] = customer["email"]
        if "contact" in customer:
            link_params["customer_contact"] = customer["contact"]
    
    if "notify" in link_params:
        # Format notification preferences
        notify = link_params.pop("notify", {})
        if "sms" in notify:
            link_params["notify_sms"] = notify["sms"]
        if "email" in notify:
            link_params["notify_email"] = notify["email"]
            
    return razorpay_client.create_payment_link(link_params)

async def get_payment_link(arguments):
    payment_link_id = arguments.get("payment_link_id")
    logger.info(f"Executing get_payment_link with payment_link_id: {payment_link_id}")
    return razorpay_client.get_payment_link({"id": payment_link_id})

async def create_refund(arguments):
    logger.info(f"Executing create_refund with arguments: {arguments}")
    return razorpay_client.create_refund(arguments)

async def get_refund(arguments):
    refund_id = arguments.get("refund_id")
    logger.info(f"Executing get_refund with refund_id: {refund_id}")
    return razorpay_client.get_refund({"id": refund_id})

# Settlement handlers
async def get_settlement(arguments):
    settlement_id = arguments.get("settlement_id")
    logger.info(f"Executing get_settlement with settlement_id: {settlement_id}")
    return razorpay_client.get_settlement({"id": settlement_id})

async def list_settlements(arguments):
    logger.info(f"Executing list_settlements with arguments: {arguments}")
    return razorpay_client.list_settlements(arguments)

async def create_ondemand_settlement(arguments):
    logger.info(f"Executing create_ondemand_settlement with arguments: {arguments}")
    return razorpay_client.create_ondemand_settlement(arguments)

async def get_settlement_report(arguments):
    logger.info(f"Executing get_settlement_report with arguments: {arguments}")
    return razorpay_client.get_settlement_report(arguments)

# Subscription handlers
async def get_subscription(arguments):
    subscription_id = arguments.get("subscription_id")
    logger.info(f"Executing get_subscription with subscription_id: {subscription_id}")
    return razorpay_client.get_subscription({"id": subscription_id})

async def list_subscriptions(arguments):
    logger.info(f"Executing list_subscriptions with arguments: {arguments}")
    return razorpay_client.list_subscriptions(arguments)

async def create_subscription(arguments):
    logger.info(f"Executing create_subscription with arguments: {arguments}")
    return razorpay_client.create_subscription(arguments)

async def cancel_subscription(arguments):
    subscription_id = arguments.get("subscription_id")
    cancel_at_cycle_end = arguments.get("cancel_at_cycle_end", False)
    logger.info(f"Executing cancel_subscription with subscription_id: {subscription_id}")
    return razorpay_client.cancel_subscription({
        "id": subscription_id,
        "cancel_at_cycle_end": cancel_at_cycle_end
    })

async def pause_subscription(arguments):
    subscription_id = arguments.get("subscription_id")
    pause_at = arguments.get("pause_at", "now")
    logger.info(f"Executing pause_subscription with subscription_id: {subscription_id}")
    return razorpay_client.pause_subscription({
        "id": subscription_id,
        "pause_at": pause_at
    })

async def resume_subscription(arguments):
    subscription_id = arguments.get("subscription_id")
    resume_at = arguments.get("resume_at", None)
    logger.info(f"Executing resume_subscription with subscription_id: {subscription_id}")
    
    params = {"id": subscription_id}
    if resume_at:
        params["resume_at"] = resume_at
        
    return razorpay_client.resume_subscription(params)

def decorate_tool(fn, name, description):
    """Add metadata to tool function for documentation purposes"""
    fn.__name__ = name
    fn.__doc__ = description
    return fn

def create_mcp_server():
    """Create and configure the FastMCP server with Razorpay tools."""
    # Create the FastMCP server
    server = FastMCP(
        name="razorpay-mcp-server-python",
        version="1.0.0",
        description="Razorpay integration for the Model Context Protocol"
    )
    
    # Add tools using the correct add_tool method
    # The signature is: add_tool(fn, name=None, description=None)
    
    server.add_tool(
        fn=get_payment,
        name="razorpay_payments_get",
        description="Get payment details by payment ID"
    )
    
    server.add_tool(
        fn=list_payments,
        name="razorpay_payments_list",
        description="List payments with optional filtering"
    )
    
    server.add_tool(
        fn=create_order,
        name="razorpay_orders_create",
        description="Create a new order"
    )
    
    server.add_tool(
        fn=get_order,
        name="razorpay_orders_get",
        description="Get order details by order ID"
    )
    
    server.add_tool(
        fn=list_orders,
        name="razorpay_orders_list",
        description="List orders with optional filtering"
    )
    
    server.add_tool(
        fn=create_customer,
        name="razorpay_customers_create",
        description="Create a new customer"
    )
    
    server.add_tool(
        fn=get_customer,
        name="razorpay_customers_get",
        description="Get customer details by customer ID"
    )
    
    server.add_tool(
        fn=create_payment_link,
        name="razorpay_payment_links_create",
        description="Create a new payment link"
    )
    
    server.add_tool(
        fn=get_payment_link,
        name="razorpay_payment_links_get",
        description="Get payment link details by payment link ID"
    )
    
    server.add_tool(
        fn=create_refund,
        name="razorpay_refunds_create",
        description="Create a new refund"
    )
    
    server.add_tool(
        fn=get_refund,
        name="razorpay_refunds_get",
        description="Get refund details by refund ID"
    )
    
    # Add resources - need uri field
    server.add_resource(
        Resource(
            id="razorpay_order_sample",
            name="Razorpay Order Example",
            description="Example Razorpay order payload",
            content=json.dumps({
                "amount": 50000,
                "currency": "INR",
                "receipt": "order_receipt_1",
                "notes": {
                    "purpose": "Sample order for testing"
                }
            }),
            format="json",
            uri="mcp-resources://razorpay/order-sample"  # Required by your SDK
        )
    )
    
    server.add_resource(
        Resource(
            id="razorpay_customer_sample",
            name="Razorpay Customer Example",
            description="Example Razorpay customer payload",
            content=json.dumps({
                "name": "John Doe",
                "email": "john.doe@example.com",
                "contact": "+919999999999",
                "notes": {
                    "source": "API demonstration"
                }
            }),
            format="json",
            uri="mcp-resources://razorpay/customer-sample"  # Required by your SDK
        )
    )
    
    server.add_resource(
        Resource(
            id="razorpay_payment_link_sample",
            name="Razorpay Payment Link Example",
            description="Example Razorpay payment link payload",
            content=json.dumps({
                "amount": 100000,
                "currency": "INR",
                "description": "Payment for service XYZ",
                "customer": {
                    "name": "Jane Doe",
                    "email": "jane.doe@example.com",
                    "contact": "+919999999988"
                },
                "notify": {
                    "sms": False,
                    "email": False
                },
                "reminder_enable": False
            }),
            format="json",
            uri="mcp-resources://razorpay/payment-link-sample"  # Required by your SDK
        )
    )
    
    # Add prompts using Prompt class
    server.add_prompt(
        Prompt(
            id="razorpay_create_order",
            name="Create Razorpay Order",
            description="Create a new order in Razorpay",
            content="Create a new Razorpay order with the following details:\n- Amount: {{amount}} in {{currency}}\n- Receipt: {{receipt}}\n- Notes: {{notes}}\n\nPlease provide the order ID and other details once created."
        )
    )
    
    server.add_prompt(
        Prompt(
            id="razorpay_create_customer",
            name="Create Razorpay Customer",
            description="Create a new customer in Razorpay",
            content="Create a new Razorpay customer with the following details:\n- Name: {{name}}\n- Email: {{email}}\n- Contact: {{contact}}\n\nPlease provide the customer ID once created."
        )
    )
    
    server.add_prompt(
        Prompt(
            id="razorpay_create_payment_link",
            name="Create Razorpay Payment Link",
            description="Create a payment link for a customer",
            content="Create a new Razorpay payment link with the following details:\n- Amount: {{amount}} in {{currency}}\n- Description: {{description}}\n- Customer Name: {{customer_name}}\n- Customer Email: {{customer_email}}\n- Customer Contact: {{customer_contact}}\n\nPlease provide the payment link URL once created."
        )
    )
    
    server.add_prompt(
        Prompt(
            id="razorpay_check_payment_status",
            name="Check Payment Status",
            description="Check status of an existing Razorpay payment",
            content="Check the status of Razorpay payment with ID {{payment_id}} and summarize the results, including the amount, currency, status, and creation date."
        )
    )
    
    # Return the configured server
    return server

def main():
    """Start the MCP server with Razorpay integration."""
    server = create_mcp_server()
    logger.info("Starting Razorpay MCP Server using FastMCP...")
    server.run(transport="stdio")

if __name__ == "__main__":
    main()