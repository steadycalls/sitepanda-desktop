"""
Data Fetcher Module
Orchestrates fetching data from Duda API and storing in database.
"""

from typing import List, Dict, Optional
from datetime import datetime
from modules.duda_client import DudaAPIClient
from modules.database import DatabaseManager


class DataFetcher:
    """Fetches data from Duda API and stores in local database."""
    
    def __init__(self, duda_client: DudaAPIClient, db_manager: DatabaseManager):
        """
        Initialize data fetcher.
        
        Args:
            duda_client: Initialized Duda API client
            db_manager: Database manager instance
        """
        self.duda = duda_client
        self.db = db_manager
    
    def fetch_all_sites(self) -> int:
        """
        Fetch all sites and store in database.
        
        Returns:
            Number of sites fetched
        """
        print("Fetching sites...")
        sites = self.duda.list_sites(limit=100)
        
        if not sites:
            print("No sites found or error fetching sites")
            return 0
        
        count = 0
        for site in sites:
            site_data = {
                'site_name': site.get('site_name'),
                'site_title': site.get('site_default_domain') or site.get('site_name'),
                'template_id': site.get('template_id'),
                'site_domain': site.get('site_domain') or site.get('site_default_domain'),
                'is_published': 1 if site.get('published') else 0,
                'created_date': site.get('creation_date'),
                'last_published_date': site.get('last_published_date'),
                'store_enabled': 1 if site.get('store_enabled') else 0,
                'blog_enabled': 1 if site.get('blog_enabled') else 0,
                'metadata': site
            }
            
            if self.db.insert_site(site_data):
                count += 1
        
        print(f"Fetched {count} sites")
        return count
    
    def fetch_site_stats(self, site_name: str, days: int = 30) -> bool:
        """
        Fetch analytics/statistics for a site.
        
        Args:
            site_name: Site identifier
            days: Number of days of historical data to fetch
            
        Returns:
            True if successful
        """
        print(f"Fetching stats for {site_name}...")
        stats = self.duda.get_site_stats(site_name)
        
        if not stats:
            print(f"No stats available for {site_name}")
            return False
        
        # The stats API returns aggregated data
        # Store it in a format we can use
        # Note: Actual structure depends on Duda's response
        
        print(f"Stats fetched for {site_name}")
        return True
    
    def fetch_form_submissions(self, site_name: str, days: int = 30) -> int:
        """
        Fetch form submissions for a site.
        
        Args:
            site_name: Site identifier
            days: Number of days of historical data to fetch
            
        Returns:
            Number of submissions fetched
        """
        print(f"Fetching form submissions for {site_name}...")
        submissions = self.duda.get_form_submissions(site_name)
        
        if not submissions:
            print(f"No form submissions for {site_name}")
            return 0
        
        count = 0
        for submission in submissions:
            # Extract form data
            form_data = {
                'site_name': site_name,
                'form_id': submission.get('form_id', 'unknown'),
                'form_title': submission.get('form_title', 'Contact Form'),
                'submission_date': submission.get('date') or submission.get('created_at') or datetime.now().isoformat(),
                'form_data': submission.get('fields') or submission.get('data') or {},
                'submitter_email': self._extract_email(submission),
                'submitter_name': self._extract_name(submission)
            }
            
            if self.db.insert_form_submission(form_data):
                count += 1
        
        print(f"Fetched {count} form submissions for {site_name}")
        return count
    
    def fetch_ecommerce_data(self, site_name: str) -> Dict[str, int]:
        """
        Fetch eCommerce products and orders for a site.
        
        Args:
            site_name: Site identifier
            
        Returns:
            Dictionary with counts of products and orders fetched
        """
        result = {'products': 0, 'orders': 0}
        
        # Check if store is enabled
        if not self.duda.get_store_enabled(site_name):
            print(f"Store not enabled for {site_name}")
            return result
        
        # Fetch products
        print(f"Fetching products for {site_name}...")
        products = self.duda.list_products(site_name)
        
        if products:
            for product in products:
                product_data = {
                    'site_name': site_name,
                    'product_id': product.get('id') or product.get('product_id'),
                    'product_name': product.get('name'),
                    'description': product.get('description'),
                    'price': product.get('price'),
                    'currency': product.get('currency', 'USD'),
                    'sku': product.get('sku'),
                    'stock_quantity': product.get('stock_quantity') or product.get('quantity'),
                    'category': product.get('category'),
                    'images': product.get('images', []),
                    'is_active': 1 if product.get('active', True) else 0
                }
                
                if self.db.insert_product(product_data):
                    result['products'] += 1
        
        # Fetch orders
        print(f"Fetching orders for {site_name}...")
        orders = self.duda.list_orders(site_name, limit=100)
        
        if orders:
            for order in orders:
                order_data = {
                    'site_name': site_name,
                    'order_id': order.get('id') or order.get('order_id'),
                    'order_number': order.get('order_number') or order.get('invoice_number'),
                    'order_date': order.get('created') or order.get('order_date') or datetime.now().isoformat(),
                    'customer_name': order.get('billing_address', {}).get('full_name') or order.get('customer_name'),
                    'customer_email': order.get('email') or order.get('customer_email'),
                    'total_amount': order.get('total') or order.get('total_amount'),
                    'currency': order.get('currency', 'USD'),
                    'status': order.get('status'),
                    'items': order.get('items', []),
                    'shipping_address': order.get('shipping_address', {}),
                    'billing_address': order.get('billing_address', {})
                }
                
                if self.db.insert_ecommerce_order(order_data):
                    result['orders'] += 1
        
        print(f"Fetched {result['products']} products and {result['orders']} orders for {site_name}")
        return result
    
    def fetch_all_data(self) -> Dict[str, int]:
        """
        Fetch all data for all sites.
        
        Returns:
            Dictionary with counts of all data fetched
        """
        stats = {
            'sites': 0,
            'form_submissions': 0,
            'products': 0,
            'orders': 0
        }
        
        # First, fetch all sites
        stats['sites'] = self.fetch_all_sites()
        
        # Get list of sites from database
        sites = self.db.get_all_sites()
        
        # Fetch data for each site
        for site in sites:
            site_name = site['site_name']
            
            # Fetch form submissions
            stats['form_submissions'] += self.fetch_form_submissions(site_name)
            
            # Fetch eCommerce data
            ecommerce_stats = self.fetch_ecommerce_data(site_name)
            stats['products'] += ecommerce_stats['products']
            stats['orders'] += ecommerce_stats['orders']
            
            # Fetch site stats (analytics)
            self.fetch_site_stats(site_name)
        
        return stats
    
    def _extract_email(self, submission: Dict) -> Optional[str]:
        """Extract email from form submission."""
        # Try common field names
        fields = submission.get('fields', {}) or submission.get('data', {})
        
        for key in ['email', 'Email', 'e-mail', 'E-mail', 'EMAIL']:
            if key in fields:
                return fields[key]
        
        # Look in top-level
        for key in ['email', 'submitter_email', 'user_email']:
            if key in submission:
                return submission[key]
        
        return None
    
    def _extract_name(self, submission: Dict) -> Optional[str]:
        """Extract name from form submission."""
        fields = submission.get('fields', {}) or submission.get('data', {})
        
        # Try to find name field
        for key in ['name', 'Name', 'full_name', 'Full Name', 'NAME']:
            if key in fields:
                return fields[key]
        
        # Try first + last name
        first = fields.get('first_name') or fields.get('First Name')
        last = fields.get('last_name') or fields.get('Last Name')
        
        if first and last:
            return f"{first} {last}"
        elif first:
            return first
        
        # Look in top-level
        for key in ['name', 'submitter_name', 'user_name']:
            if key in submission:
                return submission[key]
        
        return None
