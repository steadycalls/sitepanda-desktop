"""
Google Search Console (GSC) Client Module
Handles fetching search performance data from Google Search Console.
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta

try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    GSC_AVAILABLE = True
except ImportError:
    GSC_AVAILABLE = False


class GSCClient:
    """Client for Google Search Console API."""
    
    SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]
    
    def __init__(self, service_account_file: str):
        """
        Initialize GSC client.
        
        Args:
            service_account_file: Path to Google service account JSON file
        """
        if not GSC_AVAILABLE:
            raise ImportError(
                "Google API libraries not installed. "
                "Install with: pip install google-api-python-client google-auth"
            )
        
        self.service_account_file = service_account_file
        self.service = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the GSC client with credentials."""
        try:
            credentials = service_account.Credentials.from_service_account_file(
                self.service_account_file,
                scopes=self.SCOPES
            )
            self.service = build(
                "searchconsole",
                "v1",
                credentials=credentials,
                cache_discovery=False
            )
        except Exception as e:
            raise Exception(f"Failed to initialize GSC client: {e}")
    
    def test_connection(self, site_url: str) -> bool:
        """
        Test connection to GSC property.
        
        Args:
            site_url: Site URL (e.g., "https://example.com/")
            
        Returns:
            True if connection successful
        """
        try:
            # Try a simple query
            self._query(site_url, dimensions=["date"], row_limit=1, days=7)
            return True
        except:
            return False
    
    def _date_range(self, days: int = 28) -> tuple:
        """
        Get date range for the last N days.
        
        Args:
            days: Number of days to look back
            
        Returns:
            Tuple of (start_date, end_date) as strings
        """
        end = datetime.now().date()
        start = end - timedelta(days=days)
        return str(start), str(end)
    
    def _query(
        self,
        site_url: str,
        dimensions: List[str],
        row_limit: int = 5000,
        days: int = 28
    ) -> Dict:
        """
        Execute a GSC search analytics query.
        
        Args:
            site_url: Site URL
            dimensions: List of dimensions (e.g., ["page", "query"])
            row_limit: Maximum rows to return
            days: Number of days to look back
            
        Returns:
            Query response
        """
        start_date, end_date = self._date_range(days)
        
        body = {
            "startDate": start_date,
            "endDate": end_date,
            "dimensions": dimensions,
            "rowLimit": row_limit
        }
        
        return self.service.searchanalytics().query(
            siteUrl=site_url,
            body=body
        ).execute()
    
    def _response_to_rows(self, response: Dict, dimensions: List[str]) -> List[Dict]:
        """
        Convert GSC response to list of dictionaries.
        
        Args:
            response: GSC query response
            dimensions: List of dimension names
            
        Returns:
            List of row dictionaries
        """
        rows = []
        
        for row in response.get("rows", []):
            data = {}
            
            # Add dimensions
            for i, dim in enumerate(dimensions):
                data[dim] = row["keys"][i]
            
            # Add metrics
            data["clicks"] = row.get("clicks", 0)
            data["impressions"] = row.get("impressions", 0)
            data["ctr"] = row.get("ctr", 0)
            data["position"] = row.get("position", 0)
            
            rows.append(data)
        
        return rows
    
    def normalize_site_url(self, domain: str) -> str:
        """
        Normalize domain to GSC site URL format.
        
        Args:
            domain: Domain name (e.g., "example.com")
            
        Returns:
            Normalized site URL (e.g., "https://example.com/")
        """
        if not domain.startswith("http"):
            domain = f"https://{domain}"
        if not domain.endswith("/"):
            domain = f"{domain}/"
        return domain
    
    def get_pages(self, site_url: str, days: int = 28) -> List[Dict]:
        """
        Get search performance by page.
        
        Args:
            site_url: Site URL
            days: Number of days to look back
            
        Returns:
            List of page performance data
        """
        response = self._query(site_url, dimensions=["page"], days=days)
        return self._response_to_rows(response, ["page"])
    
    def get_queries(self, site_url: str, days: int = 28) -> List[Dict]:
        """
        Get search performance by query.
        
        Args:
            site_url: Site URL
            days: Number of days to look back
            
        Returns:
            List of query performance data
        """
        response = self._query(site_url, dimensions=["query"], days=days)
        return self._response_to_rows(response, ["query"])
    
    def get_countries(self, site_url: str, days: int = 28) -> List[Dict]:
        """
        Get search performance by country.
        
        Args:
            site_url: Site URL
            days: Number of days to look back
            
        Returns:
            List of country performance data
        """
        response = self._query(site_url, dimensions=["country"], days=days)
        return self._response_to_rows(response, ["country"])
    
    def get_devices(self, site_url: str, days: int = 28) -> List[Dict]:
        """
        Get search performance by device.
        
        Args:
            site_url: Site URL
            days: Number of days to look back
            
        Returns:
            List of device performance data
        """
        response = self._query(site_url, dimensions=["device"], days=days)
        return self._response_to_rows(response, ["device"])
    
    def get_page_queries(self, site_url: str, days: int = 28, limit: int = 1000) -> List[Dict]:
        """
        Get search performance by page and query combination.
        
        Args:
            site_url: Site URL
            days: Number of days to look back
            limit: Maximum rows to return
            
        Returns:
            List of page-query performance data
        """
        response = self._query(
            site_url,
            dimensions=["page", "query"],
            row_limit=limit,
            days=days
        )
        return self._response_to_rows(response, ["page", "query"])
    
    def list_sites(self) -> List[str]:
        """
        List all sites the service account has access to.
        
        Returns:
            List of site URLs
        """
        try:
            sites = self.service.sites().list().execute()
            return [site["siteUrl"] for site in sites.get("siteEntry", [])]
        except Exception as e:
            raise Exception(f"Failed to list sites: {e}")

