"""
Duda API Client Module
Handles all interactions with the Duda REST API.
"""

import requests
from requests.auth import HTTPBasicAuth
from typing import List, Dict, Optional
from datetime import datetime, timedelta


class DudaAPIClient:
    """Client for interacting with Duda REST API."""
    
    BASE_URL = "https://api.duda.co/api"
    
    def __init__(self, api_user: str, api_password: str):
        """
        Initialize Duda API client.
        
        Args:
            api_user: Duda API username
            api_password: Duda API password
        """
        self.auth = HTTPBasicAuth(api_user, api_password)
        self.session = requests.Session()
        self.session.auth = self.auth
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Optional[Dict]:
        """
        Make HTTP request to Duda API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            **kwargs: Additional arguments for requests
            
        Returns:
            Response JSON or None on error
        """
        url = f"{self.BASE_URL}/{endpoint}"
        
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            
            # Some endpoints return empty responses
            if response.status_code == 204 or not response.content:
                return {}
            
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
            print(f"Response: {e.response.text if e.response else 'No response'}")
            return None
        except Exception as e:
            print(f"Error making request to {endpoint}: {e}")
            return None
    
    # ===== SITES API =====
    
    def list_sites(self, limit: int = 50, offset: int = 0) -> Optional[List[Dict]]:
        """
        List all sites.
        
        Args:
            limit: Number of sites to return
            offset: Pagination offset
            
        Returns:
            List of site objects
        """
        params = {'limit': limit, 'offset': offset}
        response = self._make_request('GET', 'sites/multiscreen', params=params)
        
        if response and 'sites' in response:
            return response['sites']
        return []
    
    def get_site(self, site_name: str) -> Optional[Dict]:
        """
        Get details for a specific site.
        
        Args:
            site_name: Site identifier
            
        Returns:
            Site details
        """
        return self._make_request('GET', f'sites/multiscreen/{site_name}')
    
    # ===== ANALYTICS/STATS API =====
    
    def get_site_stats(self, site_name: str, from_date: str = None, to_date: str = None, 
                       dimension: str = 'DAYS') -> Optional[Dict]:
        """
        Get site analytics/statistics.
        
        Args:
            site_name: Site identifier
            from_date: Start date (YYYY-MM-DD)
            to_date: End date (YYYY-MM-DD)
            dimension: Time dimension (DAYS, WEEKS, MONTHS)
            
        Returns:
            Analytics data
        """
        # Default to last 30 days if no dates provided
        if not to_date:
            to_date = datetime.now().strftime('%Y-%m-%d')
        if not from_date:
            from_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        
        params = {
            'from': from_date,
            'to': to_date,
            'dimension': dimension
        }
        
        return self._make_request('GET', f'sites/multiscreen/analytics/{site_name}', params=params)
    
    def get_site_activities(self, site_name: str, limit: int = 50, offset: int = 0,
                           from_date: str = None, to_date: str = None,
                           activities: List[str] = None) -> Optional[List[Dict]]:
        """
        Get site activity log.
        
        Args:
            site_name: Site identifier
            limit: Number of activities to return
            offset: Pagination offset
            from_date: Start date (YYYY-MM-DD)
            to_date: End date (YYYY-MM-DD)
            activities: List of activity types to filter
            
        Returns:
            List of activity objects
        """
        params = {'limit': limit, 'offset': offset}
        
        if from_date:
            params['from'] = from_date
        if to_date:
            params['to'] = to_date
        if activities:
            params['activities'] = ','.join(activities)
        
        response = self._make_request('GET', f'sites/multiscreen/{site_name}/activities', params=params)
        
        if response and 'activities' in response:
            return response['activities']
        return []
    
    # ===== FORMS API =====
    
    def get_form_submissions(self, site_name: str, from_date: str = None, 
                            to_date: str = None) -> Optional[List[Dict]]:
        """
        Get form submissions for a site.
        
        Args:
            site_name: Site identifier
            from_date: Start date (YYYY-MM-DD)
            to_date: End date (YYYY-MM-DD)
            
        Returns:
            List of form submissions
        """
        params = {}
        
        if from_date:
            params['from'] = from_date
        if to_date:
            params['to'] = to_date
        
        response = self._make_request('GET', f'sites/multiscreen/{site_name}/forms', params=params)
        
        if isinstance(response, list):
            return response
        elif isinstance(response, dict) and 'results' in response:
            return response['results']
        return []
    
    # ===== ECOMMERCE API =====
    
    def get_store_enabled(self, site_name: str) -> bool:
        """
        Check if eCommerce is enabled for a site.
        
        Args:
            site_name: Site identifier
            
        Returns:
            True if store is enabled
        """
        site_details = self.get_site(site_name)
        if site_details:
            return site_details.get('store_enabled', False)
        return False
    
    def list_products(self, site_name: str) -> Optional[List[Dict]]:
        """
        List all products in a site's store.
        
        Args:
            site_name: Site identifier
            
        Returns:
            List of products
        """
        response = self._make_request('GET', f'sites/multiscreen/{site_name}/ecommerce/products')
        
        if isinstance(response, list):
            return response
        elif isinstance(response, dict) and 'results' in response:
            return response['results']
        return []
    
    def get_product(self, site_name: str, product_id: str) -> Optional[Dict]:
        """
        Get details for a specific product.
        
        Args:
            site_name: Site identifier
            product_id: Product identifier
            
        Returns:
            Product details
        """
        return self._make_request('GET', f'sites/multiscreen/{site_name}/ecommerce/products/{product_id}')
    
    def list_orders(self, site_name: str, offset: int = 0, limit: int = 50,
                   status: str = None) -> Optional[List[Dict]]:
        """
        List eCommerce orders.
        
        Args:
            site_name: Site identifier
            offset: Pagination offset
            limit: Number of orders to return
            status: Filter by order status
            
        Returns:
            List of orders
        """
        params = {'offset': offset, 'limit': limit}
        
        if status:
            params['status'] = status
        
        response = self._make_request('GET', f'sites/multiscreen/{site_name}/ecommerce/orders', params=params)
        
        if isinstance(response, list):
            return response
        elif isinstance(response, dict) and 'results' in response:
            return response['results']
        return []
    
    def get_order(self, site_name: str, order_id: str) -> Optional[Dict]:
        """
        Get details for a specific order.
        
        Args:
            site_name: Site identifier
            order_id: Order identifier
            
        Returns:
            Order details
        """
        return self._make_request('GET', f'sites/multiscreen/{site_name}/ecommerce/orders/{order_id}')
    
    # ===== CONTENT LIBRARY API =====
    
    def get_content_library(self, site_name: str) -> Optional[Dict]:
        """
        Get content library data for a site.
        
        Args:
            site_name: Site identifier
            
        Returns:
            Content library data
        """
        return self._make_request('GET', f'sites/multiscreen/{site_name}/content')
    
    # ===== COLLECTIONS API =====
    
    def list_collections(self, site_name: str) -> Optional[List[Dict]]:
        """
        List all collections for a site.
        
        Args:
            site_name: Site identifier
            
        Returns:
            List of collections
        """
        response = self._make_request('GET', f'sites/multiscreen/{site_name}/collection')
        
        if isinstance(response, list):
            return response
        return []
    
    def get_collection(self, site_name: str, collection_name: str) -> Optional[Dict]:
        """
        Get a specific collection with its data.
        
        Args:
            site_name: Site identifier
            collection_name: Collection name
            
        Returns:
            Collection data
        """
        return self._make_request('GET', f'sites/multiscreen/{site_name}/collection/{collection_name}')
    
    # ===== BLOG API =====
    
    def list_blog_posts(self, site_name: str, limit: int = 50, offset: int = 0) -> Optional[List[Dict]]:
        """
        List blog posts for a site.
        
        Args:
            site_name: Site identifier
            limit: Number of posts to return
            offset: Pagination offset
            
        Returns:
            List of blog posts
        """
        params = {'limit': limit, 'offset': offset}
        response = self._make_request('GET', f'sites/multiscreen/{site_name}/blog/posts', params=params)
        
        if isinstance(response, list):
            return response
        elif isinstance(response, dict) and 'results' in response:
            return response['results']
        return []
    
    def get_blog_post(self, site_name: str, post_id: str) -> Optional[Dict]:
        """
        Get a specific blog post.
        
        Args:
            site_name: Site identifier
            post_id: Blog post identifier
            
        Returns:
            Blog post details
        """
        return self._make_request('GET', f'sites/multiscreen/{site_name}/blog/posts/{post_id}')
    
    # ===== UTILITY METHODS =====
    
    def test_connection(self) -> bool:
        """
        Test API connection and credentials.
        
        Returns:
            True if connection is successful
        """
        try:
            result = self.list_sites(limit=1)
            return result is not None
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False
