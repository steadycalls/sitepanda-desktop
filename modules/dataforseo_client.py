"""
DataForSEO API Client Module
Handles API calls to DataForSEO for crawls, keywords, backlinks, and competitor analysis.
"""

import requests
import base64
import time
import json
from typing import Dict, List, Optional


class DataForSEOClient:
    """Client for DataForSEO API."""
    
    BASE_URL = "https://api.dataforseo.com/v3"
    
    def __init__(self, login: str, password: str):
        """
        Initialize DataForSEO client.
        
        Args:
            login: DataForSEO login/email
            password: DataForSEO password or API key
        """
        self.login = login
        self.password = password
        self.session = requests.Session()
    
    def _auth_headers(self) -> Dict[str, str]:
        """Generate authorization headers."""
        token = base64.b64encode(f"{self.login}:{self.password}".encode()).decode()
        return {
            "Authorization": f"Basic {token}",
            "Content-Type": "application/json"
        }
    
    def _post(self, endpoint: str, payload: List[Dict]) -> Dict:
        """
        Make POST request to DataForSEO API.
        
        Args:
            endpoint: API endpoint (e.g., "/serp/google/organic/live")
            payload: List of task dictionaries
            
        Returns:
            API response as dictionary
        """
        url = f"{self.BASE_URL}{endpoint}"
        
        try:
            response = self.session.post(
                url,
                headers=self._auth_headers(),
                data=json.dumps(payload),
                timeout=120
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"DataForSEO API error: {e}")
    
    def test_connection(self) -> bool:
        """
        Test API connection and credentials.
        
        Returns:
            True if connection successful
        """
        try:
            # Use a simple endpoint to test
            response = self._post("/serp/google/locations", [])
            return response.get("status_code") == 20000
        except:
            return False
    
    def get_on_page_summary(self, domain: str, max_crawl_pages: int = 500) -> Dict:
        """
        Get on-page SEO summary for a domain.
        
        Args:
            domain: Domain to crawl (e.g., "example.com")
            max_crawl_pages: Maximum pages to crawl
            
        Returns:
            On-page summary data
        """
        payload = [{
            "target": domain,
            "max_crawl_pages": max_crawl_pages,
            "load_resources": True,
            "enable_javascript": True,
            "custom_js": "",
            "tag": "on_page_crawl"
        }]
        
        # Post task
        response = self._post("/on_page/task_post", payload)
        
        if response.get("status_code") != 20000:
            raise Exception(f"Failed to create crawl task: {response.get('status_message')}")
        
        task_id = response["tasks"][0]["id"]
        
        # Wait for task to complete (poll every 10 seconds)
        max_wait = 600  # 10 minutes
        waited = 0
        
        while waited < max_wait:
            time.sleep(10)
            waited += 10
            
            # Check task status
            result = self._post(f"/on_page/summary/{task_id}", [{}])
            
            if result.get("tasks", [{}])[0].get("status_code") == 20000:
                return result
            
        raise Exception("Crawl task timed out")
    
    def get_organic_competitors(self, domain: str, location: str = "United States", language: str = "en") -> Dict:
        """
        Get organic search competitors for a domain.
        
        Args:
            domain: Target domain
            location: Location name
            language: Language code
            
        Returns:
            Competitor data
        """
        payload = [{
            "target": domain,
            "location_name": location,
            "language_name": language,
            "limit": 50
        }]
        
        return self._post("/serp/competitors/domain_organic/live", payload)
    
    def get_backlinks_summary(self, domain: str) -> Dict:
        """
        Get backlinks summary for a domain.
        
        Args:
            domain: Target domain
            
        Returns:
            Backlinks summary data
        """
        payload = [{
            "target": domain,
            "include_subdomains": True,
            "backlinks_status_type": "all"
        }]
        
        return self._post("/backlinks/summary/live", payload)
    
    def get_backlinks_referring_domains(self, domain: str, limit: int = 100) -> Dict:
        """
        Get referring domains for backlinks.
        
        Args:
            domain: Target domain
            limit: Maximum referring domains to return
            
        Returns:
            Referring domains data
        """
        payload = [{
            "target": domain,
            "limit": limit,
            "include_subdomains": True,
            "order_by": ["rank,desc"]
        }]
        
        return self._post("/backlinks/referring_domains/live", payload)
    
    def get_ranked_keywords(self, domain: str, location: str = "United States", language: str = "en", limit: int = 100) -> Dict:
        """
        Get keywords the domain ranks for.
        
        Args:
            domain: Target domain
            location: Location name
            language: Language code
            limit: Maximum keywords to return
            
        Returns:
            Ranked keywords data
        """
        payload = [{
            "target": domain,
            "location_name": location,
            "language_name": language,
            "limit": limit,
            "order_by": ["ranked_serp_element.serp_item.rank_group,asc"]
        }]
        
        return self._post("/dataforseo_labs/google/ranked_keywords/live", payload)
    
    def get_domain_metrics(self, domain: str) -> Dict:
        """
        Get domain metrics (authority, traffic estimates, etc.).
        
        Args:
            domain: Target domain
            
        Returns:
            Domain metrics data
        """
        payload = [{
            "target": domain
        }]
        
        return self._post("/dataforseo_labs/google/domain_metrics/live", payload)
    
    def get_page_insights(self, url: str) -> Dict:
        """
        Get detailed insights for a specific page.
        
        Args:
            url: Full URL to analyze
            
        Returns:
            Page insights data
        """
        payload = [{
            "url": url,
            "enable_javascript": True,
            "load_resources": True
        }]
        
        return self._post("/on_page/instant_pages", payload)

