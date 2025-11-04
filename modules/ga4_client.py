"""
Google Analytics 4 (GA4) Client Module
Handles fetching analytics data from GA4 properties.
"""

import json
from typing import Dict, List, Optional
from datetime import datetime, timedelta

try:
    from google.analytics.data_v1beta import BetaAnalyticsDataClient
    from google.analytics.data_v1beta.types import (
        DateRange, Dimension, Metric, RunReportRequest
    )
    from google.oauth2 import service_account
    GA4_AVAILABLE = True
except ImportError:
    GA4_AVAILABLE = False


class GA4Client:
    """Client for Google Analytics 4 API."""
    
    def __init__(self, service_account_file: str):
        """
        Initialize GA4 client.
        
        Args:
            service_account_file: Path to Google service account JSON file
        """
        if not GA4_AVAILABLE:
            raise ImportError(
                "Google Analytics libraries not installed. "
                "Install with: pip install google-analytics-data google-auth"
            )
        
        self.service_account_file = service_account_file
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the GA4 client with credentials."""
        try:
            credentials = service_account.Credentials.from_service_account_file(
                self.service_account_file
            )
            self.client = BetaAnalyticsDataClient(credentials=credentials)
        except Exception as e:
            raise Exception(f"Failed to initialize GA4 client: {e}")
    
    def test_connection(self, property_id: str) -> bool:
        """
        Test connection to GA4 property.
        
        Args:
            property_id: GA4 property ID (e.g., "properties/123456789")
            
        Returns:
            True if connection successful
        """
        try:
            # Try a simple request
            self._run_report(
                property_id,
                dimensions=["date"],
                metrics=["sessions"],
                days=7,
                limit=1
            )
            return True
        except:
            return False
    
    def _date_range(self, days: int = 28) -> DateRange:
        """
        Create a date range for the last N days.
        
        Args:
            days: Number of days to look back
            
        Returns:
            DateRange object
        """
        end = datetime.now().date()
        start = end - timedelta(days=days)
        return DateRange(start_date=str(start), end_date=str(end))
    
    def _run_report(
        self,
        property_id: str,
        dimensions: List[str],
        metrics: List[str],
        days: int = 28,
        limit: int = 10000
    ) -> Dict:
        """
        Run a GA4 report.
        
        Args:
            property_id: GA4 property ID
            dimensions: List of dimension names
            metrics: List of metric names
            days: Number of days to look back
            limit: Maximum rows to return
            
        Returns:
            Report response
        """
        request = RunReportRequest(
            property=property_id,
            date_ranges=[self._date_range(days)],
            dimensions=[Dimension(name=d) for d in dimensions],
            metrics=[Metric(name=m) for m in metrics],
            limit=limit
        )
        
        return self.client.run_report(request)
    
    def _response_to_rows(self, response) -> List[Dict]:
        """
        Convert GA4 response to list of dictionaries.
        
        Args:
            response: GA4 RunReportResponse
            
        Returns:
            List of row dictionaries
        """
        rows = []
        
        for row in response.rows:
            data = {}
            
            # Add dimensions
            for header, value in zip(response.dimension_headers, row.dimension_values):
                data[header.name] = value.value
            
            # Add metrics
            for header, value in zip(response.metric_headers, row.metric_values):
                try:
                    data[header.name] = float(value.value or 0)
                except:
                    data[header.name] = value.value
            
            rows.append(data)
        
        return rows
    
    def get_page_analytics(self, property_id: str, days: int = 28) -> List[Dict]:
        """
        Get analytics for individual pages.
        
        Args:
            property_id: GA4 property ID
            days: Number of days to look back
            
        Returns:
            List of page analytics
        """
        response = self._run_report(
            property_id,
            dimensions=["pagePathPlusQueryString", "pageTitle"],
            metrics=[
                "screenPageViews",
                "sessions",
                "engagementRate",
                "averageSessionDuration"
            ],
            days=days
        )
        
        return self._response_to_rows(response)
    
    def get_landing_pages(self, property_id: str, days: int = 28) -> List[Dict]:
        """
        Get landing page analytics.
        
        Args:
            property_id: GA4 property ID
            days: Number of days to look back
            
        Returns:
            List of landing page analytics
        """
        response = self._run_report(
            property_id,
            dimensions=["landingPagePlusQueryString"],
            metrics=[
                "sessions",
                "engagedSessions",
                "engagementRate",
                "conversions"
            ],
            days=days
        )
        
        return self._response_to_rows(response)
    
    def get_device_analytics(self, property_id: str, days: int = 28) -> List[Dict]:
        """
        Get analytics by device category.
        
        Args:
            property_id: GA4 property ID
            days: Number of days to look back
            
        Returns:
            List of device analytics
        """
        response = self._run_report(
            property_id,
            dimensions=["deviceCategory"],
            metrics=["sessions", "engagedSessions", "engagementRate"],
            days=days
        )
        
        return self._response_to_rows(response)
    
    def get_geo_analytics(self, property_id: str, days: int = 28) -> List[Dict]:
        """
        Get analytics by country.
        
        Args:
            property_id: GA4 property ID
            days: Number of days to look back
            
        Returns:
            List of country analytics
        """
        response = self._run_report(
            property_id,
            dimensions=["country"],
            metrics=["sessions", "engagedSessions", "engagementRate"],
            days=days
        )
        
        return self._response_to_rows(response)
    
    def get_traffic_sources(self, property_id: str, days: int = 28) -> List[Dict]:
        """
        Get analytics by traffic source.
        
        Args:
            property_id: GA4 property ID
            days: Number of days to look back
            
        Returns:
            List of traffic source analytics
        """
        response = self._run_report(
            property_id,
            dimensions=["sessionSource", "sessionMedium"],
            metrics=["sessions", "engagedSessions", "conversions"],
            days=days
        )
        
        return self._response_to_rows(response)

