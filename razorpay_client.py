import os
import logging
import traceback
from razorpay import Client

logger = logging.getLogger(__name__)

class RazorpayClient:
    """Client for interacting with the Razorpay API."""
    
    def __init__(self):
        """Initialize the Razorpay client with API credentials."""
        self.key_id = os.environ.get("RAZORPAY_KEY_ID")
        self.key_secret = os.environ.get("RAZORPAY_KEY_SECRET")
        
        if not self.key_id or not self.key_secret:
            logger.warning("Razorpay API credentials not set. Using test mode.")
            self.key_id = self.key_id or "rzp_test_key"
            self.key_secret = self.key_secret or "rzp_test_secret"
        
        self.client = Client(auth=(self.key_id, self.key_secret))

    # Payment Methods
    def get_payment(self, params):
        """Get payment details by payment ID."""
        try:
            payment_id = params.get('id')
            if not payment_id:
                raise ValueError("Payment ID is required")
            
            return self.client.payment.fetch(payment_id)
        except Exception as e:
            logger.error(f"Error fetching payment: {str(e)}")
            logger.error(traceback.format_exc())
            raise

    def list_payments(self, params):
        """List payments with optional filtering."""
        try:
            # Convert params to format expected by Razorpay
            razorpay_params = {}
            if 'count' in params:
                razorpay_params['count'] = params['count']
            if 'skip' in params:
                razorpay_params['skip'] = params['skip']
            if 'from' in params:
                razorpay_params['from'] = params['from']
            if 'to' in params:
                razorpay_params['to'] = params['to']
            
            return self.client.payment.all(razorpay_params)
        except Exception as e:
            logger.error(f"Error listing payments: {str(e)}")
            logger.error(traceback.format_exc())
            raise

    def create_payment(self, params):
        """Create a new payment."""
        try:
            # Razorpay doesn't directly create payments like Stripe
            # Instead, we create an order and then capture payment against it
            order_params = {
                'amount': params.get('amount'),
                'currency': params.get('currency', 'INR'),
                'receipt': params.get('receipt', ''),
                'notes': params.get('notes', {})
            }
            
            order = self.client.order.create(data=order_params)
            
            # For MCP purposes, we'll return the order with payment info
            return {
                'id': order['id'],
                'amount': order['amount'],
                'currency': order['currency'],
                'receipt': order.get('receipt'),
                'notes': order.get('notes', {}),
                'status': order['status'],
                'created_at': order['created_at'],
                'order_url': f"https://api.razorpay.com/v1/checkout/embedded/{self.key_id}/{order['id']}"
            }
        except Exception as e:
            logger.error(f"Error creating payment: {str(e)}")
            logger.error(traceback.format_exc())
            raise

    # Refund Methods
    def get_refund(self, params):
        """Get refund details by refund ID."""
        try:
            refund_id = params.get('id')
            if not refund_id:
                raise ValueError("Refund ID is required")
            
            return self.client.refund.fetch(refund_id)
        except Exception as e:
            logger.error(f"Error fetching refund: {str(e)}")
            logger.error(traceback.format_exc())
            raise

    def create_refund(self, params):
        """Create a new refund."""
        try:
            payment_id = params.get('payment_id')
            if not payment_id:
                raise ValueError("Payment ID is required")
            
            refund_params = {
                'payment_id': payment_id,
                'amount': params.get('amount'),
                'notes': params.get('notes', {})
            }
            
            return self.client.refund.create(data=refund_params)
        except Exception as e:
            logger.error(f"Error creating refund: {str(e)}")
            logger.error(traceback.format_exc())
            raise

    # Order Methods
    def get_order(self, params):
        """Get order details by order ID."""
        try:
            order_id = params.get('id')
            if not order_id:
                raise ValueError("Order ID is required")
            
            return self.client.order.fetch(order_id)
        except Exception as e:
            logger.error(f"Error fetching order: {str(e)}")
            logger.error(traceback.format_exc())
            raise

    def list_orders(self, params):
        """List orders with optional filtering."""
        try:
            # Convert params to format expected by Razorpay
            razorpay_params = {}
            if 'count' in params:
                razorpay_params['count'] = params['count']
            if 'skip' in params:
                razorpay_params['skip'] = params['skip']
            if 'from' in params:
                razorpay_params['from'] = params['from']
            if 'to' in params:
                razorpay_params['to'] = params['to']
            
            return self.client.order.all(razorpay_params)
        except Exception as e:
            logger.error(f"Error listing orders: {str(e)}")
            logger.error(traceback.format_exc())
            raise

    def create_order(self, params):
        """Create a new order."""
        try:
            order_params = {
                'amount': params.get('amount'),
                'currency': params.get('currency', 'INR'),
                'receipt': params.get('receipt', ''),
                'notes': params.get('notes', {}),
                'payment_capture': params.get('payment_capture', True)
            }
            
            return self.client.order.create(data=order_params)
        except Exception as e:
            logger.error(f"Error creating order: {str(e)}")
            logger.error(traceback.format_exc())
            raise

    # Customer Methods
    def get_customer(self, params):
        """Get customer details by customer ID."""
        try:
            customer_id = params.get('id')
            if not customer_id:
                raise ValueError("Customer ID is required")
            
            return self.client.customer.fetch(customer_id)
        except Exception as e:
            logger.error(f"Error fetching customer: {str(e)}")
            logger.error(traceback.format_exc())
            raise

    def create_customer(self, params):
        """Create a new customer."""
        try:
            customer_params = {
                'name': params.get('name'),
                'email': params.get('email'),
                'contact': params.get('contact', ''),
                'notes': params.get('notes', {})
            }
            
            return self.client.customer.create(data=customer_params)
        except Exception as e:
            logger.error(f"Error creating customer: {str(e)}")
            logger.error(traceback.format_exc())
            raise

    # Payment Link Methods
    def get_payment_link(self, params):
        """Get payment link details by payment link ID."""
        try:
            link_id = params.get('id')
            if not link_id:
                raise ValueError("Payment Link ID is required")
            
            return self.client.payment_link.fetch(link_id)
        except Exception as e:
            logger.error(f"Error fetching payment link: {str(e)}")
            logger.error(traceback.format_exc())
            raise

    def create_payment_link(self, params):
        """Create a new payment link."""
        try:
            required_fields = ['amount', 'currency', 'description']
            for field in required_fields:
                if field not in params:
                    raise ValueError(f"{field} is required for creating a payment link")
            
            link_params = {
                'amount': params.get('amount'),
                'currency': params.get('currency', 'INR'),
                'description': params.get('description'),
                'customer': {
                    'name': params.get('customer_name', ''),
                    'email': params.get('customer_email', ''),
                    'contact': params.get('customer_contact', '')
                },
                'notify': {
                    'sms': params.get('notify_sms', True),
                    'email': params.get('notify_email', True)
                },
                'reminder_enable': params.get('reminder_enable', True),
                'notes': params.get('notes', {}),
                'callback_url': params.get('callback_url', ''),
                'callback_method': params.get('callback_method', 'get')
            }
            
            return self.client.payment_link.create(data=link_params)
        except Exception as e:
            logger.error(f"Error creating payment link: {str(e)}")
            logger.error(traceback.format_exc())
            raise
            
    # Settlement Methods
    def get_settlement(self, params):
        """Get settlement details by settlement ID."""
        try:
            settlement_id = params.get('id')
            if not settlement_id:
                raise ValueError("Settlement ID is required")
            
            return self.client.settlement.fetch(settlement_id)
        except Exception as e:
            logger.error(f"Error fetching settlement: {str(e)}")
            logger.error(traceback.format_exc())
            raise
    
    def list_settlements(self, params):
        """List settlements with optional filtering."""
        try:
            # Convert params to format expected by Razorpay
            razorpay_params = {}
            if 'count' in params:
                razorpay_params['count'] = params['count']
            if 'skip' in params:
                razorpay_params['skip'] = params['skip']
            if 'from' in params:
                razorpay_params['from'] = params['from']
            if 'to' in params:
                razorpay_params['to'] = params['to']
            
            return self.client.settlement.all(razorpay_params)
        except Exception as e:
            logger.error(f"Error listing settlements: {str(e)}")
            logger.error(traceback.format_exc())
            raise
    
    def create_ondemand_settlement(self, params):
        """Create an on-demand settlement."""
        try:
            settlement_params = {
                'amount': params.get('amount'),
                'settle_full_balance': params.get('settle_full_balance', False),
                'description': params.get('description', ''),
                'notes': params.get('notes', {})
            }
            
            return self.client.settlement.create_ondemand_settlement(data=settlement_params)
        except Exception as e:
            logger.error(f"Error creating on-demand settlement: {str(e)}")
            logger.error(traceback.format_exc())
            raise
    
    def get_settlement_report(self, params):
        """Get settlement reports with filtering."""
        try:
            report_params = {
                'year': params.get('year'),
                'month': params.get('month'),
                'day': params.get('day', None),
                'count': params.get('count', None),
                'skip': params.get('skip', None)
            }
            
            return self.client.settlement.report(data=report_params)
        except Exception as e:
            logger.error(f"Error getting settlement report: {str(e)}")
            logger.error(traceback.format_exc())
            raise
            
    # Plan Methods
    def get_plan(self, params):
        """Get plan details by plan ID."""
        try:
            plan_id = params.get('id')
            if not plan_id:
                raise ValueError("Plan ID is required")
            
            return self.client.plan.fetch(plan_id)
        except Exception as e:
            logger.error(f"Error fetching plan: {str(e)}")
            logger.error(traceback.format_exc())
            raise
            
    def list_plans(self, params):
        """List plans with optional filtering."""
        try:
            options = {}
            if 'count' in params:
                options['count'] = params['count']
            if 'skip' in params:
                options['skip'] = params['skip']
                
            return self.client.plan.all(options)
        except Exception as e:
            logger.error(f"Error listing plans: {str(e)}")
            logger.error(traceback.format_exc())
            raise
            
    def create_plan(self, params):
        """Create a new plan."""
        try:
            if not params.get('period'):
                raise ValueError("Period is required")
            if not params.get('interval'):
                raise ValueError("Interval is required")
            if not params.get('item'):
                raise ValueError("Item details are required")
                
            plan_data = {
                'period': params.get('period'),
                'interval': params.get('interval'),
                'item': params.get('item')
            }
            
            if 'notes' in params:
                plan_data['notes'] = params['notes']
                
            return self.client.plan.create(plan_data)
        except Exception as e:
            logger.error(f"Error creating plan: {str(e)}")
            logger.error(traceback.format_exc())
            raise
    
    # Subscription Methods
    def get_subscription(self, params):
        """Get subscription details by subscription ID."""
        try:
            subscription_id = params.get('id')
            if not subscription_id:
                raise ValueError("Subscription ID is required")
            
            return self.client.subscription.fetch(subscription_id)
        except Exception as e:
            logger.error(f"Error fetching subscription: {str(e)}")
            logger.error(traceback.format_exc())
            raise
    
    def list_subscriptions(self, params):
        """List subscriptions with optional filtering."""
        try:
            # Convert params to format expected by Razorpay
            razorpay_params = {}
            if 'count' in params:
                razorpay_params['count'] = params['count']
            if 'skip' in params:
                razorpay_params['skip'] = params['skip']
            if 'plan_id' in params:
                razorpay_params['plan_id'] = params['plan_id']
            if 'customer_id' in params:
                razorpay_params['customer_id'] = params['customer_id']
            
            return self.client.subscription.all(razorpay_params)
        except Exception as e:
            logger.error(f"Error listing subscriptions: {str(e)}")
            logger.error(traceback.format_exc())
            raise
    
    def create_subscription(self, params):
        """Create a new subscription."""
        try:
            required_fields = ['plan_id', 'customer_id', 'total_count']
            for field in required_fields:
                if field not in params:
                    raise ValueError(f"{field} is required for creating a subscription")
            
            subscription_params = {
                'plan_id': params.get('plan_id'),
                'customer_id': params.get('customer_id'),
                'total_count': params.get('total_count'),
                'quantity': params.get('quantity', 1),
                'start_at': params.get('start_at', None),
                'expire_by': params.get('expire_by', None),
                'customer_notify': params.get('customer_notify', True),
                'notes': params.get('notes', {})
            }
            
            return self.client.subscription.create(data=subscription_params)
        except Exception as e:
            logger.error(f"Error creating subscription: {str(e)}")
            logger.error(traceback.format_exc())
            raise
    
    def cancel_subscription(self, params):
        """Cancel an active subscription."""
        try:
            subscription_id = params.get('id')
            if not subscription_id:
                raise ValueError("Subscription ID is required")
                
            cancel_params = {
                'cancel_at_cycle_end': params.get('cancel_at_cycle_end', False)
            }
            
            return self.client.subscription.cancel(subscription_id, data=cancel_params)
        except Exception as e:
            logger.error(f"Error cancelling subscription: {str(e)}")
            logger.error(traceback.format_exc())
            raise
    
    def pause_subscription(self, params):
        """Pause an active subscription."""
        try:
            subscription_id = params.get('id')
            if not subscription_id:
                raise ValueError("Subscription ID is required")
                
            pause_params = {
                'pause_at': params.get('pause_at', 'now')
            }
            
            return self.client.subscription.pause(subscription_id, data=pause_params)
        except Exception as e:
            logger.error(f"Error pausing subscription: {str(e)}")
            logger.error(traceback.format_exc())
            raise
    
    def resume_subscription(self, params):
        """Resume a paused subscription."""
        try:
            subscription_id = params.get('id')
            if not subscription_id:
                raise ValueError("Subscription ID is required")
                
            resume_params = {}
            if 'resume_at' in params:
                resume_params['resume_at'] = params['resume_at']
            
            return self.client.subscription.resume(subscription_id, data=resume_params)
        except Exception as e:
            logger.error(f"Error resuming subscription: {str(e)}")
            logger.error(traceback.format_exc())
            raise