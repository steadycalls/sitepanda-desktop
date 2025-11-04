"""
SEO Audit Module
Orchestrates SEO audits using DataForSEO, GA4, and GSC data.
"""

import json
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path


class SEOAuditor:
    """Orchestrates comprehensive SEO audits."""
    
    def __init__(
        self,
        dataforseo_client,
        db_manager,
        ga4_client=None,
        gsc_client=None
    ):
        """
        Initialize SEO auditor.
        
        Args:
            dataforseo_client: DataForSEOClient instance
            db_manager: DatabaseManager instance
            ga4_client: Optional GA4Client instance
            gsc_client: Optional GSCClient instance
        """
        self.dfs = dataforseo_client
        self.db = db_manager
        self.ga4 = ga4_client
        self.gsc = gsc_client
    
    def run_audit(
        self,
        domain: str,
        ga4_property_id: Optional[str] = None,
        max_crawl_pages: int = 500
    ) -> Dict:
        """
        Run a comprehensive SEO audit for a domain.
        
        Args:
            domain: Domain to audit
            ga4_property_id: Optional GA4 property ID
            max_crawl_pages: Maximum pages to crawl
            
        Returns:
            Audit results dictionary
        """
        audit_id = self._create_audit_record(domain)
        
        try:
            # Step 1: DataForSEO crawl and analysis
            crawl_data = self._fetch_dataforseo_data(domain, max_crawl_pages)
            
            # Step 2: GA4 data (if configured)
            ga4_data = None
            if self.ga4 and ga4_property_id:
                ga4_data = self._fetch_ga4_data(ga4_property_id)
            
            # Step 3: GSC data (if configured)
            gsc_data = None
            if self.gsc:
                gsc_data = self._fetch_gsc_data(domain)
            
            # Step 4: Analyze and generate insights
            insights = self._analyze_data(crawl_data, ga4_data, gsc_data)
            
            # Step 5: Save audit results
            self._save_audit_results(audit_id, insights, crawl_data, ga4_data, gsc_data)
            
            # Step 6: Update audit status
            self._update_audit_status(audit_id, "completed")
            
            return {
                "audit_id": audit_id,
                "domain": domain,
                "status": "completed",
                "insights": insights,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self._update_audit_status(audit_id, "failed", str(e))
            raise
    
    def _create_audit_record(self, domain: str) -> int:
        """Create initial audit record in database."""
        conn = self.db._get_connection()
        cursor = conn.cursor()
        
        # Create audits table if not exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS seo_audits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                domain TEXT NOT NULL,
                status TEXT NOT NULL,
                error_message TEXT,
                started_at TEXT NOT NULL,
                completed_at TEXT,
                crawl_data TEXT,
                ga4_data TEXT,
                gsc_data TEXT,
                insights TEXT
            )
        ''')
        
        cursor.execute('''
            INSERT INTO seo_audits (domain, status, started_at)
            VALUES (?, ?, ?)
        ''', (domain, "running", datetime.now().isoformat()))
        
        conn.commit()
        return cursor.lastrowid
    
    def _fetch_dataforseo_data(self, domain: str, max_crawl_pages: int) -> Dict:
        """Fetch all DataForSEO data."""
        data = {}
        
        # On-page crawl summary
        try:
            data["crawl"] = self.dfs.get_on_page_summary(domain, max_crawl_pages)
        except Exception as e:
            data["crawl_error"] = str(e)
        
        # Competitors
        try:
            data["competitors"] = self.dfs.get_organic_competitors(domain)
        except Exception as e:
            data["competitors_error"] = str(e)
        
        # Backlinks
        try:
            data["backlinks"] = self.dfs.get_backlinks_summary(domain)
            data["referring_domains"] = self.dfs.get_backlinks_referring_domains(domain)
        except Exception as e:
            data["backlinks_error"] = str(e)
        
        # Ranked keywords
        try:
            data["keywords"] = self.dfs.get_ranked_keywords(domain)
        except Exception as e:
            data["keywords_error"] = str(e)
        
        # Domain metrics
        try:
            data["domain_metrics"] = self.dfs.get_domain_metrics(domain)
        except Exception as e:
            data["domain_metrics_error"] = str(e)
        
        return data
    
    def _fetch_ga4_data(self, property_id: str) -> Dict:
        """Fetch GA4 analytics data."""
        data = {}
        
        try:
            data["pages"] = self.ga4.get_page_analytics(property_id)
            data["landing_pages"] = self.ga4.get_landing_pages(property_id)
            data["devices"] = self.ga4.get_device_analytics(property_id)
            data["countries"] = self.ga4.get_geo_analytics(property_id)
            data["traffic_sources"] = self.ga4.get_traffic_sources(property_id)
        except Exception as e:
            data["error"] = str(e)
        
        return data
    
    def _fetch_gsc_data(self, domain: str) -> Dict:
        """Fetch Google Search Console data."""
        data = {}
        
        try:
            site_url = self.gsc.normalize_site_url(domain)
            
            data["pages"] = self.gsc.get_pages(site_url)
            data["queries"] = self.gsc.get_queries(site_url)
            data["countries"] = self.gsc.get_countries(site_url)
            data["devices"] = self.gsc.get_devices(site_url)
        except Exception as e:
            data["error"] = str(e)
        
        return data
    
    def _analyze_data(
        self,
        crawl_data: Dict,
        ga4_data: Optional[Dict],
        gsc_data: Optional[Dict]
    ) -> Dict:
        """Analyze collected data and generate insights."""
        insights = {
            "summary": {},
            "issues": [],
            "opportunities": [],
            "metrics": {}
        }
        
        # Analyze crawl data
        if "crawl" in crawl_data:
            insights["summary"]["crawl"] = self._analyze_crawl(crawl_data["crawl"])
        
        # Analyze competitors
        if "competitors" in crawl_data:
            insights["summary"]["competitors"] = self._analyze_competitors(crawl_data["competitors"])
        
        # Analyze backlinks
        if "backlinks" in crawl_data:
            insights["summary"]["backlinks"] = self._analyze_backlinks(crawl_data["backlinks"])
        
        # Analyze keywords
        if "keywords" in crawl_data:
            insights["summary"]["keywords"] = self._analyze_keywords(crawl_data["keywords"])
        
        # Analyze GA4 data
        if ga4_data and "pages" in ga4_data:
            insights["summary"]["ga4"] = self._analyze_ga4(ga4_data)
        
        # Analyze GSC data
        if gsc_data and "pages" in gsc_data:
            insights["summary"]["gsc"] = self._analyze_gsc(gsc_data)
        
        # Generate prioritized issues
        insights["issues"] = self._generate_issues(crawl_data, ga4_data, gsc_data)
        
        return insights
    
    def _analyze_crawl(self, crawl_data: Dict) -> Dict:
        """Analyze on-page crawl data."""
        summary = {}
        
        try:
            tasks = crawl_data.get("tasks", [])
            if tasks and tasks[0].get("result"):
                result = tasks[0]["result"][0]
                
                summary["total_pages"] = result.get("pages", 0)
                summary["crawl_status"] = result.get("crawl_status", "unknown")
                
                # Extract key metrics
                if "items" in result:
                    items = result["items"]
                    summary["items_count"] = len(items)
        except:
            pass
        
        return summary
    
    def _analyze_competitors(self, comp_data: Dict) -> Dict:
        """Analyze competitor data."""
        summary = {}
        
        try:
            tasks = comp_data.get("tasks", [])
            if tasks and tasks[0].get("result"):
                items = tasks[0]["result"][0].get("items", [])
                summary["competitor_count"] = len(items)
                summary["top_competitors"] = [
                    item.get("target") for item in items[:10]
                ]
        except:
            pass
        
        return summary
    
    def _analyze_backlinks(self, backlink_data: Dict) -> Dict:
        """Analyze backlink data."""
        summary = {}
        
        try:
            tasks = backlink_data.get("tasks", [])
            if tasks and tasks[0].get("result"):
                result = tasks[0]["result"][0]
                summary["total_backlinks"] = result.get("backlinks", 0)
                summary["referring_domains"] = result.get("referring_domains", 0)
                summary["referring_ips"] = result.get("referring_ips", 0)
        except:
            pass
        
        return summary
    
    def _analyze_keywords(self, keyword_data: Dict) -> Dict:
        """Analyze ranked keywords data."""
        summary = {}
        
        try:
            tasks = keyword_data.get("tasks", [])
            if tasks and tasks[0].get("result"):
                items = tasks[0]["result"][0].get("items", [])
                summary["total_keywords"] = len(items)
                
                # Top 10 keywords
                summary["top_keywords"] = [
                    {
                        "keyword": item.get("keyword"),
                        "position": item.get("ranked_serp_element", {}).get("serp_item", {}).get("rank_group", 0)
                    }
                    for item in items[:10]
                ]
        except:
            pass
        
        return summary
    
    def _analyze_ga4(self, ga4_data: Dict) -> Dict:
        """Analyze GA4 analytics data."""
        summary = {}
        
        try:
            pages = ga4_data.get("pages", [])
            summary["total_pages"] = len(pages)
            
            if pages:
                total_views = sum(p.get("screenPageViews", 0) for p in pages)
                summary["total_pageviews"] = total_views
                
                # Top pages by views
                sorted_pages = sorted(pages, key=lambda x: x.get("screenPageViews", 0), reverse=True)
                summary["top_pages"] = [
                    {
                        "path": p.get("pagePathPlusQueryString"),
                        "views": p.get("screenPageViews", 0)
                    }
                    for p in sorted_pages[:10]
                ]
        except:
            pass
        
        return summary
    
    def _analyze_gsc(self, gsc_data: Dict) -> Dict:
        """Analyze GSC search data."""
        summary = {}
        
        try:
            queries = gsc_data.get("queries", [])
            summary["total_queries"] = len(queries)
            
            if queries:
                total_clicks = sum(q.get("clicks", 0) for q in queries)
                total_impressions = sum(q.get("impressions", 0) for q in queries)
                
                summary["total_clicks"] = total_clicks
                summary["total_impressions"] = total_impressions
                summary["avg_ctr"] = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
                
                # Top queries
                sorted_queries = sorted(queries, key=lambda x: x.get("clicks", 0), reverse=True)
                summary["top_queries"] = [
                    {
                        "query": q.get("query"),
                        "clicks": q.get("clicks", 0),
                        "position": q.get("position", 0)
                    }
                    for q in sorted_queries[:10]
                ]
        except:
            pass
        
        return summary
    
    def _generate_issues(
        self,
        crawl_data: Dict,
        ga4_data: Optional[Dict],
        gsc_data: Optional[Dict]
    ) -> List[Dict]:
        """Generate prioritized list of SEO issues."""
        issues = []
        
        # Placeholder for issue detection logic
        # In a full implementation, this would analyze the data
        # and identify specific issues like:
        # - Broken links (4xx, 5xx)
        # - Duplicate titles
        # - Missing meta descriptions
        # - Thin content
        # - Slow pages
        # - Mobile usability issues
        # etc.
        
        return issues
    
    def _save_audit_results(
        self,
        audit_id: int,
        insights: Dict,
        crawl_data: Dict,
        ga4_data: Optional[Dict],
        gsc_data: Optional[Dict]
    ):
        """Save audit results to database."""
        conn = self.db._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE seo_audits
            SET crawl_data = ?,
                ga4_data = ?,
                gsc_data = ?,
                insights = ?
            WHERE id = ?
        ''', (
            json.dumps(crawl_data),
            json.dumps(ga4_data) if ga4_data else None,
            json.dumps(gsc_data) if gsc_data else None,
            json.dumps(insights),
            audit_id
        ))
        
        conn.commit()
    
    def _update_audit_status(self, audit_id: int, status: str, error: Optional[str] = None):
        """Update audit status in database."""
        conn = self.db._get_connection()
        cursor = conn.cursor()
        
        if status == "completed":
            cursor.execute('''
                UPDATE seo_audits
                SET status = ?,
                    completed_at = ?
                WHERE id = ?
            ''', (status, datetime.now().isoformat(), audit_id))
        else:
            cursor.execute('''
                UPDATE seo_audits
                SET status = ?,
                    error_message = ?,
                    completed_at = ?
                WHERE id = ?
            ''', (status, error, datetime.now().isoformat(), audit_id))
        
        conn.commit()
    
    def get_audit_results(self, audit_id: int) -> Optional[Dict]:
        """
        Get audit results by ID.
        
        Args:
            audit_id: Audit ID
            
        Returns:
            Audit results dictionary or None
        """
        conn = self.db._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM seo_audits WHERE id = ?', (audit_id,))
        row = cursor.fetchone()
        
        if row:
            return dict(row)
        return None
    
    def list_audits(self, domain: Optional[str] = None) -> List[Dict]:
        """
        List all audits, optionally filtered by domain.
        
        Args:
            domain: Optional domain filter
            
        Returns:
            List of audit records
        """
        conn = self.db._get_connection()
        cursor = conn.cursor()
        
        if domain:
            cursor.execute(
                'SELECT * FROM seo_audits WHERE domain = ? ORDER BY started_at DESC',
                (domain,)
            )
        else:
            cursor.execute('SELECT * FROM seo_audits ORDER BY started_at DESC')
        
        return [dict(row) for row in cursor.fetchall()]

