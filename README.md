# Razorpay MCP Server

A Model Context Protocol (MCP) server implementation for Razorpay payment integration that enables Claude AI to interact directly with Razorpay's payment services.

![Razorpay MCP Integration](https://razorpay.com/docs/assets/images/logo.svg)

## Overview

This project creates a bridge between AI assistants (like Claude) and Razorpay's payment platform using the Model Context Protocol (MCP). It allows AI to perform various payment operations directly, without requiring manual API integration:

- Process payments and refunds
- Create and track orders
- Manage customer profiles
- Generate payment links
- Handle subscription billing
- Process settlements and disbursements
- And more...

The implementation follows the official MCP specification and uses the Razorpay API to provide a seamless connection between AI assistants and payment processing capabilities.

## Features

- **Comprehensive Razorpay Integration**: 
  - **Payments**: Fetch and list payments, create and manage refunds
  - **Orders**: Create, fetch, and list orders
  - **Customers**: Create and manage customer profiles
  - **Payment Links**: Generate shareable payment links
  - **Subscriptions**: Create and manage recurring billing
  - **Settlements**: Process settlements and generate reports
- **Dual-mode Operation**: 
  - HTTP server with web interface for API access
  - Direct stdio connection for Claude Desktop integration
- **Official MCP SDK Support**: Implements the Model Context Protocol to spec
- **Developer-friendly**: Clear documentation, configuration examples, and setup guides
- **Production Ready**: Error handling, proper logging, and security considerations

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

### Payment and Refund Tools
- **razorpay_payments_get**: Fetch payment details by payment ID
- **razorpay_payments_list**: List payments with optional filtering
- **razorpay_refunds_create**: Create a new refund
- **razorpay_refunds_get**: Get refund details by refund ID

### Order Tools
- **razorpay_orders_create**: Create a new order
- **razorpay_orders_get**: Get order details by order ID
- **razorpay_orders_list**: List orders with optional filtering

### Customer Tools
- **razorpay_customers_create**: Create a new customer
- **razorpay_customers_get**: Get customer details by customer ID

### Payment Link Tools
- **razorpay_payment_links_create**: Create a new payment link
- **razorpay_payment_links_get**: Get payment link details by payment link ID

### Settlement Tools
- **razorpay_settlements_get**: Get settlement details by settlement ID
- **razorpay_settlements_list**: List settlements with optional filtering
- **razorpay_settlements_create_ondemand**: Create an on-demand settlement
- **razorpay_settlements_report**: Get settlement reports with filtering

### Subscription Tools
- **razorpay_subscriptions_get**: Get subscription details by subscription ID
- **razorpay_subscriptions_list**: List subscriptions with optional filtering
- **razorpay_subscriptions_create**: Create a new subscription for a customer
- **razorpay_subscriptions_cancel**: Cancel an active subscription
- **razorpay_subscriptions_pause**: Pause an active subscription
- **razorpay_subscriptions_resume**: Resume a paused subscription

## Resources and Prompts

The server also provides helpful resources and prompt templates to guide Claude in constructing proper Razorpay API requests.

### Resources

- **razorpay_order_sample**: Example order payload
- **razorpay_customer_sample**: Example customer payload
- **razorpay_payment_link_sample**: Example payment link payload
- **razorpay_subscription_sample**: Example subscription payload
- **razorpay_settlement_sample**: Example on-demand settlement payload

### Prompts

- **razorpay_create_order**: Template for creating orders
- **razorpay_create_customer**: Template for creating customers
- **razorpay_create_payment_link**: Template for creating payment links
- **razorpay_check_payment_status**: Template for checking payment status
- **razorpay_create_subscription**: Template for creating subscriptions
- **razorpay_manage_subscription**: Template for managing existing subscriptions
- **razorpay_create_settlement**: Template for creating on-demand settlements
- **razorpay_check_settlement**: Template for checking settlement details

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

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Razorpay account with API keys

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/razorpay-mcp-server.git
cd razorpay-mcp-server
```

### Step 2: Set Up Python Environment (Optional but Recommended)

Create and activate a virtual environment:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

Install all required packages:

```bash
pip install flask gunicorn razorpay mcp jsonschema
```

The dependencies include:
- **Flask**: Web framework for the HTTP server
- **Gunicorn**: WSGI HTTP server for production deployment
- **Razorpay**: Official Razorpay Python SDK
- **MCP**: Model Context Protocol Python SDK
- **jsonschema**: For JSON schema validation

### Step 4: Configure Environment Variables

Set up your Razorpay API credentials:

```bash
# On Windows (Command Prompt):
set RAZORPAY_KEY_ID=your_key_id
set RAZORPAY_KEY_SECRET=your_key_secret

# On Windows (PowerShell):
$env:RAZORPAY_KEY_ID = "your_key_id"
$env:RAZORPAY_KEY_SECRET = "your_key_secret"

# On macOS/Linux:
export RAZORPAY_KEY_ID=your_key_id
export RAZORPAY_KEY_SECRET=your_key_secret
```

Alternatively, create a `.env` file in the project root:
```
RAZORPAY_KEY_ID=your_key_id
RAZORPAY_KEY_SECRET=your_key_secret
```

### Step 5: Run the Server

#### Option A: HTTP Server with Web Interface

Start the HTTP server:

```bash
# Development mode
python main.py

# Production mode with Gunicorn
gunicorn --bind 0.0.0.0:5000 main:app
```

The server will be available at: http://localhost:5000

#### Option B: Direct MCP Server for Claude Desktop

Run the direct MCP server for use with Claude Desktop:

```bash
python razorpay_mcp_server.py
```

This will start the MCP server using the stdio transport, which can be connected to Claude Desktop.

### Step 6: Connecting with Claude Desktop

1. Install [Claude Desktop](https://claude.ai/desktop)
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

Alternatively, you can use the provided `claude_desktop_config.json` file and import it into Claude Desktop.

## Available Functionality

### Razorpay Tools

The MCP server provides the following Razorpay integration tools:

#### Payment Operations

| Tool Name | Description | Parameters |
|-----------|-------------|------------|
| `razorpay_payments_get` | Fetch payment details | `payment_id` (string) |
| `razorpay_payments_list` | List payments with filtering | Various filter options |
| `razorpay_refunds_create` | Create a refund | `payment_id` (string), `amount` (int), etc. |
| `razorpay_refunds_get` | Get refund details | `refund_id` (string) |

#### Order Operations

| Tool Name | Description | Parameters |
|-----------|-------------|------------|
| `razorpay_orders_create` | Create a new order | `amount` (int), `currency` (string), etc. |
| `razorpay_orders_get` | Get order details | `order_id` (string) |
| `razorpay_orders_list` | List orders with filtering | Various filter options |

#### Customer Operations

| Tool Name | Description | Parameters |
|-----------|-------------|------------|
| `razorpay_customers_create` | Create a new customer | `name` (string), `email` (string), etc. |
| `razorpay_customers_get` | Get customer details | `customer_id` (string) |

#### Payment Link Operations

| Tool Name | Description | Parameters |
|-----------|-------------|------------|
| `razorpay_payment_links_create` | Create a payment link | `amount` (int), `description` (string), etc. |
| `razorpay_payment_links_get` | Get payment link details | `payment_link_id` (string) |

#### Settlement Operations

| Tool Name | Description | Parameters |
|-----------|-------------|------------|
| `razorpay_settlements_get` | Get settlement details | `settlement_id` (string) |
| `razorpay_settlements_list` | List settlements with filtering | Various filter options |
| `razorpay_settlements_create_ondemand` | Create an on-demand settlement | `amount` (int), `settle_full_balance` (bool), etc. |
| `razorpay_settlements_report` | Get settlement reports | `year` (int), `month` (int), `day` (int), etc. |

#### Subscription Operations

| Tool Name | Description | Parameters |
|-----------|-------------|------------|
| `razorpay_subscriptions_get` | Get subscription details | `subscription_id` (string) |
| `razorpay_subscriptions_list` | List subscriptions | Various filter options |
| `razorpay_subscriptions_create` | Create a new subscription | `plan_id` (string), `customer_id` (string), etc. |
| `razorpay_subscriptions_cancel` | Cancel a subscription | `subscription_id` (string), `cancel_at_cycle_end` (bool) |
| `razorpay_subscriptions_pause` | Pause a subscription | `subscription_id` (string), `pause_at` (string) |
| `razorpay_subscriptions_resume` | Resume a subscription | `subscription_id` (string), `resume_at` (string) |

### HTTP API Endpoints

When using the HTTP server (Option A), the following endpoints are available:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page with server info and start button |
| `/mcp/health` | GET | Health check endpoint |
| `/mcp/tools` | GET | List available tools |
| `/mcp/metadata` | GET | Get server metadata |
| `/mcp/request` | POST | Execute a specific tool |
| `/mcp` | POST | Standard MCP protocol endpoint |
| `/start-mcp` | GET | Start the stdio MCP server |

## License

This project is licensed under the MIT License - see the LICENSE file for details.