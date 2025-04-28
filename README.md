# Razorpay MCP Server

A Model Context Protocol (MCP) server implementation for Razorpay payment integration.

## Overview

This project provides a server that implements the Model Context Protocol (MCP) for interfacing with the Razorpay API. It allows AI assistants like Claude to directly interact with Razorpay's payment platform to perform various operations including managing payments, orders, customers, and payment links.

## Features

- Comprehensive Razorpay API integration
- Full MCP protocol support with the official MCP SDK 
- REST API endpoints for direct HTTP access
- Claude Desktop integration via stdio protocol
- Web interface for easy server management

## Implementation Details

This project provides two main ways to use the Razorpay MCP server:

### 1. HTTP-based MCP Server (main.py)

A Flask-based HTTP server that provides MCP capabilities over HTTP endpoints with a web interface for starting the raw MCP server.

**Usage:**
```bash
python main.py
# or
gunicorn --bind 0.0.0.0:5000 main:app
```

### 2. Direct MCP Server (razorpay_mcp_server.py)

Uses the official MCP Python SDK to provide a compliant implementation over stdio for direct Claude Desktop integration.

**Usage:**
```bash
python razorpay_mcp_server.py
```

## Configuration

### API Keys

The server requires Razorpay API keys to function. Set the following environment variables:

```bash
export RAZORPAY_KEY_ID=your_key_id
export RAZORPAY_KEY_SECRET=your_key_secret
```

You can also create a `.env` file based on the `.env.example` template.

### Claude Desktop Configuration

To use this MCP server with Claude Desktop:

1. Install Claude Desktop
2. Go to Settings > Desktop
3. Click "Add Service"
4. Enter the following details:
   - Name: Razorpay MCP
   - Command: `python razorpay_mcp_server.py`
   - Working Directory: (Your project directory)
5. Set the environment variables:
   - RAZORPAY_KEY_ID=your_key_id
   - RAZORPAY_KEY_SECRET=your_key_secret
6. Click "Save" and then "Connect"

## Available Tools

The MCP server provides the following Razorpay API tools:

- **payment_fetch**: Fetch payment details by payment ID
- **list_payments**: List payments with optional filtering
- **order_create**: Create a new order
- **order_fetch**: Get order details by order ID
- **list_orders**: List orders with optional filtering
- **customer_create**: Create a new customer
- **customer_fetch**: Get customer details by customer ID
- **payment_link_create**: Create a new payment link
- **payment_link_fetch**: Get payment link details by payment link ID
- **refund_create**: Create a new refund
- **refund_fetch**: Get refund details by refund ID

## Resources and Prompts

The server also provides helpful resources and prompt templates to guide Claude in constructing proper Razorpay API requests.

### Resources

- **razorpay_order_sample**: Example order payload
- **razorpay_customer_sample**: Example customer payload
- **razorpay_payment_link_sample**: Example payment link payload

### Prompts

- **razorpay_create_order**: Template for creating orders
- **razorpay_create_customer**: Template for creating customers
- **razorpay_create_payment_link**: Template for creating payment links
- **razorpay_check_payment_status**: Template for checking payment status

## API Endpoints (HTTP Server)

When using the HTTP server (main.py), the following endpoints are available:

- **GET /mcp/health**: Health check endpoint
- **GET /mcp/tools**: List available tools
- **POST /mcp/request**: Execute a tool
- **GET /mcp/metadata**: Get server metadata
- **POST /mcp**: Standard MCP protocol endpoint

## Requirements

- Python 3.7+
- Flask and Gunicorn for the HTTP server
- Razorpay Python SDK
- MCP Python SDK for the MCP server implementation

## Installation

1. Install the required packages:
   ```bash
   pip install flask gunicorn razorpay mcp jsonschema
   ```

2. Set up your environment variables (Razorpay API keys):
   ```bash
   export RAZORPAY_KEY_ID=your_key_id
   export RAZORPAY_KEY_SECRET=your_key_secret
   ```

3. Run the server:
   ```bash
   python main.py
   ```

## License

This project is licensed under the MIT License - see the LICENSE file for details.