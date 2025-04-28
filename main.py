import os
import sys
import logging
import json
import traceback
import subprocess
import threading
import time
from typing import Dict, Any, Optional, List
from flask import Flask, jsonify, request, render_template_string, redirect, url_for, session, flash

# Import the MCP server implementation
from razorpay_mcp_server import create_mcp_server

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key")

# Initialize Razorpay client
from razorpay_client import RazorpayClient
razorpay_client = RazorpayClient()

# Define MCP tools
RAZORPAY_TOOLS = [
    {
        "name": "payment_fetch",
        "description": "Fetch payment details",
        "parameters": {
            "payment_id": {
                "type": "string",
                "description": "Payment ID"
            }
        }
    },
    {
        "name": "order_create",
        "description": "Create a new order",
        "parameters": {
            "amount": {
                "type": "integer",
                "description": "Order amount in smallest currency unit"
            },
            "currency": {
                "type": "string",
                "description": "Currency code (default: INR)"
            },
            "receipt": {
                "type": "string",
                "description": "Receipt number"
            },
            "notes": {
                "type": "object",
                "description": "Additional notes"
            }
        }
    },
    {
        "name": "order_fetch",
        "description": "Fetch order details",
        "parameters": {
            "order_id": {
                "type": "string",
                "description": "Order ID"
            }
        }
    },
    {
        "name": "payment_link_create",
        "description": "Create a new payment link",
        "parameters": {
            "amount": {
                "type": "integer",
                "description": "Payment amount in smallest currency unit"
            },
            "currency": {
                "type": "string",
                "description": "Currency code"
            },
            "description": {
                "type": "string",
                "description": "Payment description"
            },
            "customer_name": {
                "type": "string",
                "description": "Customer name"
            },
            "customer_email": {
                "type": "string",
                "description": "Customer email"
            },
            "customer_contact": {
                "type": "string",
                "description": "Customer contact number"
            },
            "notes": {
                "type": "object",
                "description": "Additional notes"
            }
        }
    },
    {
        "name": "payment_link_fetch",
        "description": "Fetch payment link details",
        "parameters": {
            "payment_link_id": {
                "type": "string",
                "description": "Payment Link ID"
            }
        }
    },
    {
        "name": "customer_create",
        "description": "Create a new customer",
        "parameters": {
            "name": {
                "type": "string",
                "description": "Customer name"
            },
            "email": {
                "type": "string",
                "description": "Customer email"
            },
            "contact": {
                "type": "string",
                "description": "Customer contact number"
            },
            "notes": {
                "type": "object",
                "description": "Additional notes"
            }
        }
    },
    {
        "name": "customer_fetch",
        "description": "Fetch customer details",
        "parameters": {
            "customer_id": {
                "type": "string",
                "description": "Customer ID"
            }
        }
    }
]

# Tool execution function
def execute_tool(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Execute the specified tool with the given arguments"""
    logger.info(f"Executing tool: {tool_name} with arguments: {arguments}")
    
    # Map tool_name to handler function
    if tool_name == "payment_fetch" or tool_name == "payment.fetch":
        return razorpay_client.get_payment({"id": arguments.get("payment_id")})
    
    elif tool_name == "order_create" or tool_name == "order.create":
        params = {
            "amount": arguments.get("amount"),
            "currency": arguments.get("currency", "INR")
        }
        if "receipt" in arguments and arguments["receipt"]:
            params["receipt"] = arguments["receipt"]
        if "notes" in arguments and arguments["notes"]:
            params["notes"] = arguments["notes"]
        
        return razorpay_client.create_order(params)
    
    elif tool_name == "order_fetch" or tool_name == "order.fetch":
        return razorpay_client.get_order({"id": arguments.get("order_id")})
    
    elif tool_name == "payment_link_create" or tool_name == "payment_link.create":
        params = {
            "amount": arguments.get("amount"),
            "currency": arguments.get("currency"),
            "description": arguments.get("description")
        }
        
        if "customer_name" in arguments and arguments["customer_name"]:
            params["customer_name"] = arguments["customer_name"]
        if "customer_email" in arguments and arguments["customer_email"]:
            params["customer_email"] = arguments["customer_email"]
        if "customer_contact" in arguments and arguments["customer_contact"]:
            params["customer_contact"] = arguments["customer_contact"]
        if "notes" in arguments and arguments["notes"]:
            params["notes"] = arguments["notes"]
        
        return razorpay_client.create_payment_link(params)
    
    elif tool_name == "payment_link_fetch" or tool_name == "payment_link.fetch":
        return razorpay_client.get_payment_link({"id": arguments.get("payment_link_id")})
    
    elif tool_name == "customer_create" or tool_name == "customer.create":
        params = {
            "name": arguments.get("name"),
            "email": arguments.get("email")
        }
        
        if "contact" in arguments and arguments["contact"]:
            params["contact"] = arguments["contact"]
        if "notes" in arguments and arguments["notes"]:
            params["notes"] = arguments["notes"]
        
        return razorpay_client.create_customer(params)
    
    elif tool_name == "customer_fetch" or tool_name == "customer.fetch":
        return razorpay_client.get_customer({"id": arguments.get("customer_id")})
    
    else:
        raise ValueError(f"Unknown tool: {tool_name}")

# MCP standard routes
@app.route("/mcp/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "ok"}), 200

@app.route("/mcp/tools", methods=["GET"])
def list_tools():
    """List available tools"""
    return jsonify({"tools": RAZORPAY_TOOLS}), 200

@app.route("/mcp/request", methods=["POST"])
def handle_request():
    """Handle MCP request"""
    try:
        data = request.json
        logger.debug(f"Received MCP request: {data}")
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        tool_name = data.get("tool_name")
        arguments = data.get("arguments", {})
        
        if not tool_name:
            return jsonify({"error": "No tool_name provided"}), 400
            
        logger.info(f"Calling tool: {tool_name} with arguments: {arguments}")
        
        result = execute_tool(tool_name, arguments)
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error handling MCP request: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

@app.route("/mcp/metadata", methods=["GET"])
def get_metadata():
    """Return metadata about the MCP implementation"""
    metadata = {
        "name": "Razorpay MCP Server",
        "version": "1.0.0",
        "description": "Model Context Protocol server for Razorpay integration",
        "tools": RAZORPAY_TOOLS
    }
    return jsonify(metadata), 200

# Basic route for API information
@app.route("/")
def index():
    """API information"""
    html_content = '''
    <!DOCTYPE html>
    <html data-bs-theme="dark">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Razorpay MCP Server</title>
        <link href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container py-4">
            <div class="p-5 mb-4 bg-body-tertiary rounded-3">
                <div class="container-fluid py-5">
                    <h1 class="display-5 fw-bold">Razorpay MCP Server</h1>
                    <p class="col-md-8 fs-4">A Model Context Protocol server for Razorpay payment integration.</p>
                    <p>Version: 1.0.0</p>
                    <a href="/start-mcp" class="btn btn-primary btn-lg">Start MCP Server</a>
                </div>
            </div>
            
            <div class="row">
                <div class="col-md-6">
                    <div class="h-100 p-5 bg-body-tertiary border rounded-3">
                        <h2>API Endpoints</h2>
                        <ul class="list-group mb-3">
                            <li class="list-group-item d-flex justify-content-between align-items-center">
                                HTTP API
                                <span class="badge bg-primary rounded-pill">/mcp</span>
                            </li>
                            <li class="list-group-item d-flex justify-content-between align-items-center">
                                Health Check
                                <span class="badge bg-success rounded-pill">/mcp/health</span>
                            </li>
                            <li class="list-group-item d-flex justify-content-between align-items-center">
                                Tools List
                                <span class="badge bg-info rounded-pill">/mcp/tools</span>
                            </li>
                        </ul>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="h-100 p-5 bg-body-tertiary border rounded-3">
                        <h2>MCP Implementation</h2>
                        <p>This server implements both HTTP-based MCP and stdio-based MCP for Claude Desktop integration.</p>
                        <a href="/mcp/metadata" class="btn btn-outline-primary">View Metadata</a>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html_content)

# Standard MCP protocol endpoint
@app.route("/mcp", methods=["POST"])
def handle_standard_mcp():
    """Handle standard MCP protocol requests"""
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        request_type = data.get("type")
        
        if request_type == "metadata":
            metadata = {
                "name": "Razorpay MCP Server",
                "version": "1.0.0",
                "description": "Model Context Protocol server for Razorpay integration",
                "tools": RAZORPAY_TOOLS
            }
            return jsonify({"type": "metadata", "data": metadata}), 200
            
        elif request_type == "tool":
            tool_name = data.get("name")
            arguments = data.get("parameters", {})
            
            if not tool_name:
                return jsonify({"error": "No tool name provided"}), 400
                
            result = execute_tool(tool_name, arguments)
            return jsonify({"type": "tool_result", "data": result}), 200
            
        else:
            return jsonify({"error": f"Unsupported request type: {request_type}"}), 400
            
    except Exception as e:
        logger.error(f"Error handling standard MCP request: {e}")
        return jsonify({"error": str(e)}), 500

# MCP server thread
mcp_server_thread = None
mcp_server_running = False

@app.route("/start-mcp", methods=["GET"])
def start_mcp_server():
    """Start the MCP server in a separate thread"""
    global mcp_server_thread, mcp_server_running
    
    if mcp_server_running and mcp_server_thread and mcp_server_thread.is_alive():
        return render_template_string('''
        <!DOCTYPE html>
        <html data-bs-theme="dark">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>MCP Server Already Running</title>
            <link href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css" rel="stylesheet">
        </head>
        <body>
            <div class="container py-4">
                <div class="alert alert-info" role="alert">
                    <h4 class="alert-heading">MCP Server is already running!</h4>
                    <p>The Razorpay MCP server is already running in stdio mode.</p>
                    <hr>
                    <p class="mb-0">You can now connect to it using Claude Desktop or other MCP-compatible clients.</p>
                </div>
                <a href="/" class="btn btn-primary">Return to Dashboard</a>
            </div>
        </body>
        </html>
        ''')
    
    # Start the server in a new thread
    def run_mcp_server():
        try:
            import subprocess
            process = subprocess.Popen(
                ["python", "razorpay_mcp_server.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = process.communicate()
            logger.info(f"MCP server stopped. Exit code: {process.returncode}")
            logger.info(f"Stdout: {stdout}")
            if stderr:
                logger.error(f"Stderr: {stderr}")
            global mcp_server_running
            mcp_server_running = False
        except Exception as e:
            logger.error(f"Error running MCP server: {str(e)}")
            logger.error(traceback.format_exc())
            mcp_server_running = False
    
    mcp_server_thread = threading.Thread(target=run_mcp_server)
    mcp_server_thread.daemon = True
    mcp_server_thread.start()
    mcp_server_running = True
    
    # Return success page
    return render_template_string('''
    <!DOCTYPE html>
    <html data-bs-theme="dark">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>MCP Server Started</title>
        <link href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container py-4">
            <div class="alert alert-success" role="alert">
                <h4 class="alert-heading">MCP Server Started!</h4>
                <p>The Razorpay MCP server has been started in stdio mode.</p>
                <hr>
                <p class="mb-0">You can now connect to it using Claude Desktop or other MCP-compatible clients.</p>
            </div>
            <div class="card mb-4">
                <div class="card-header">
                    Connection Instructions
                </div>
                <div class="card-body">
                    <h5 class="card-title">Connecting with Claude Desktop</h5>
                    <ol>
                        <li>Open Claude Desktop</li>
                        <li>Go to Settings > Desktop</li>
                        <li>Click "Add Service"</li>
                        <li>Enter the following details:
                            <ul>
                                <li>Name: Razorpay MCP</li>
                                <li>Command: python razorpay_mcp_server.py</li>
                                <li>Working Directory: (Your project directory)</li>
                            </ul>
                        </li>
                        <li>Click "Save" and then "Connect"</li>
                    </ol>
                </div>
            </div>
            <a href="/" class="btn btn-primary">Return to Dashboard</a>
        </div>
    </body>
    </html>
    ''')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)