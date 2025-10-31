"""
Webhook Manager Module
Handles sending data to webhook URLs when events occur.
"""

import requests
import json
from typing import Dict, Optional
from datetime import datetime
from modules.database import DatabaseManager


class WebhookManager:
    """Manages webhook notifications for various events."""
    
    def __init__(self, db_manager: DatabaseManager, webhooks_config: Dict):
        """
        Initialize webhook manager.
        
        Args:
            db_manager: Database manager instance
            webhooks_config: Dictionary of webhook URLs for different events
        """
        self.db = db_manager
        self.webhooks = webhooks_config
        self.timeout = 10  # seconds
    
    def update_webhooks(self, webhooks_config: Dict):
        """Update webhook URLs configuration."""
        self.webhooks = webhooks_config
    
    def send_webhook(self, event_type: str, payload: Dict) -> bool:
        """
        Send data to a webhook URL.
        
        Args:
            event_type: Type of event (e.g., 'new_form_submission')
            payload: Data to send
            
        Returns:
            True if successful
        """
        webhook_url = self.webhooks.get(event_type)
        
        if not webhook_url:
            print(f"No webhook URL configured for event: {event_type}")
            return False
        
        try:
            # Add metadata to payload
            full_payload = {
                'event_type': event_type,
                'timestamp': datetime.now().isoformat(),
                'data': payload
            }
            
            # Send POST request
            response = requests.post(
                webhook_url,
                json=full_payload,
                headers={'Content-Type': 'application/json'},
                timeout=self.timeout
            )
            
            # Log the webhook
            success = response.status_code in [200, 201, 202, 204]
            
            self.db.log_webhook(
                event_type=event_type,
                webhook_url=webhook_url,
                payload=full_payload,
                response_code=response.status_code,
                response_body=response.text[:500],  # Limit response body length
                success=success
            )
            
            if success:
                print(f"Webhook sent successfully for {event_type}")
                return True
            else:
                print(f"Webhook failed with status {response.status_code}: {response.text}")
                return False
                
        except requests.exceptions.Timeout:
            print(f"Webhook timeout for {event_type}")
            self.db.log_webhook(
                event_type=event_type,
                webhook_url=webhook_url,
                payload=full_payload,
                response_code=0,
                response_body="Request timeout",
                success=False
            )
            return False
        except Exception as e:
            print(f"Error sending webhook for {event_type}: {e}")
            self.db.log_webhook(
                event_type=event_type,
                webhook_url=webhook_url,
                payload=full_payload,
                response_code=0,
                response_body=str(e),
                success=False
            )
            return False
    
    def process_new_form_submissions(self) -> int:
        """
        Process and send webhooks for new form submissions.
        
        Returns:
            Number of webhooks sent
        """
        # Get unprocessed form submissions
        submissions = self.db.get_form_submissions(unprocessed_only=True)
        
        count = 0
        for submission in submissions:
            # Prepare payload
            payload = {
                'site_name': submission.get('site_name'),
                'form_id': submission.get('form_id'),
                'form_title': submission.get('form_title'),
                'submission_date': submission.get('submission_date'),
                'submitter_name': submission.get('submitter_name'),
                'submitter_email': submission.get('submitter_email'),
                'form_data': json.loads(submission.get('form_data', '{}')) if isinstance(submission.get('form_data'), str) else submission.get('form_data', {})
            }
            
            # Send webhook
            if self.send_webhook('new_form_submission', payload):
                # Mark as sent
                self.db.mark_webhook_sent('form_submissions', submission['id'])
                count += 1
        
        return count
    
    def process_new_orders(self) -> int:
        """
        Process and send webhooks for new eCommerce orders.
        
        Returns:
            Number of webhooks sent
        """
        # Get unprocessed orders
        orders = self.db.get_ecommerce_orders(unprocessed_only=True)
        
        count = 0
        for order in orders:
            # Prepare payload
            payload = {
                'site_name': order.get('site_name'),
                'order_id': order.get('order_id'),
                'order_number': order.get('order_number'),
                'order_date': order.get('order_date'),
                'customer_name': order.get('customer_name'),
                'customer_email': order.get('customer_email'),
                'total_amount': order.get('total_amount'),
                'currency': order.get('currency'),
                'status': order.get('status'),
                'items': json.loads(order.get('items', '[]')) if isinstance(order.get('items'), str) else order.get('items', []),
                'shipping_address': json.loads(order.get('shipping_address', '{}')) if isinstance(order.get('shipping_address'), str) else order.get('shipping_address', {}),
                'billing_address': json.loads(order.get('billing_address', '{}')) if isinstance(order.get('billing_address'), str) else order.get('billing_address', {})
            }
            
            # Send webhook
            if self.send_webhook('new_ecommerce_order', payload):
                # Mark as sent
                self.db.mark_webhook_sent('ecommerce_orders', order['id'])
                count += 1
        
        return count
    
    def send_daily_stats_summary(self) -> bool:
        """
        Send daily statistics summary webhook.
        
        Returns:
            True if successful
        """
        # Get all sites
        sites = self.db.get_all_sites()
        
        # Get recent form submissions (last 24 hours)
        recent_forms = self.db.get_form_submissions()
        
        # Get recent orders (last 24 hours)
        recent_orders = self.db.get_ecommerce_orders()
        
        # Prepare summary payload
        payload = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'summary': {
                'total_sites': len(sites),
                'published_sites': sum(1 for s in sites if s.get('is_published')),
                'sites_with_store': sum(1 for s in sites if s.get('store_enabled')),
                'sites_with_blog': sum(1 for s in sites if s.get('blog_enabled')),
                'form_submissions_today': len(recent_forms),
                'orders_today': len(recent_orders),
                'total_revenue_today': sum(o.get('total_amount', 0) for o in recent_orders)
            },
            'sites': [
                {
                    'site_name': s.get('site_name'),
                    'site_title': s.get('site_title'),
                    'domain': s.get('site_domain'),
                    'is_published': bool(s.get('is_published'))
                }
                for s in sites[:10]  # Limit to first 10 sites
            ]
        }
        
        return self.send_webhook('daily_stats_summary', payload)
    
    def process_all_pending_webhooks(self) -> Dict[str, int]:
        """
        Process all pending webhooks.
        
        Returns:
            Dictionary with counts of webhooks sent for each type
        """
        result = {
            'form_submissions': 0,
            'orders': 0
        }
        
        # Process form submissions
        result['form_submissions'] = self.process_new_form_submissions()
        
        # Process orders
        result['orders'] = self.process_new_orders()
        
        return result
    
    def test_webhook(self, event_type: str) -> bool:
        """
        Send a test webhook.
        
        Args:
            event_type: Type of event to test
            
        Returns:
            True if successful
        """
        test_payload = {
            'test': True,
            'message': f'This is a test webhook for {event_type}',
            'timestamp': datetime.now().isoformat()
        }
        
        return self.send_webhook(event_type, test_payload)
