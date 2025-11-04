"""
Report Generator Module
Generates HTML and PDF reports from SEO audit data.
"""

import json
from typing import Dict, Optional
from datetime import datetime
from pathlib import Path


class ReportGenerator:
    """Generates SEO audit reports in HTML and PDF formats."""
    
    def __init__(self, output_dir: str = None):
        """
        Initialize report generator.
        
        Args:
            output_dir: Directory to save reports (default: ~/.sitepanda-desktop/reports)
        """
        if output_dir is None:
            output_dir = str(Path.home() / ".sitepanda-desktop" / "reports")
        
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_report(self, audit_data: Dict, format: str = "html") -> str:
        """
        Generate audit report.
        
        Args:
            audit_data: Audit data dictionary
            format: Output format ("html" or "pdf")
            
        Returns:
            Path to generated report file
        """
        domain = audit_data.get("domain", "unknown")
        audit_id = audit_data.get("id", "unknown")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Generate HTML content
        html_content = self._generate_html(audit_data)
        
        # Save HTML file
        html_filename = f"{domain}_{audit_id}_{timestamp}.html"
        html_path = self.output_dir / html_filename
        html_path.write_text(html_content, encoding="utf-8")
        
        # Generate PDF if requested
        if format == "pdf":
            pdf_path = self._generate_pdf(html_content, domain, audit_id, timestamp)
            return str(pdf_path)
        
        return str(html_path)
    
    def _generate_html(self, audit_data: Dict) -> str:
        """Generate HTML report content."""
        domain = audit_data.get("domain", "Unknown")
        status = audit_data.get("status", "unknown")
        started_at = audit_data.get("started_at", "")
        completed_at = audit_data.get("completed_at", "")
        
        # Parse insights
        insights_str = audit_data.get("insights", "{}")
        try:
            insights = json.loads(insights_str) if isinstance(insights_str, str) else insights_str
        except:
            insights = {}
        
        summary = insights.get("summary", {})
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SEO Audit Report - {domain}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 30px;
        }}
        
        h2 {{
            color: #34495e;
            margin-top: 30px;
            margin-bottom: 15px;
            padding-bottom: 5px;
            border-bottom: 2px solid #ecf0f1;
        }}
        
        h3 {{
            color: #7f8c8d;
            margin-top: 20px;
            margin-bottom: 10px;
        }}
        
        .meta-info {{
            background: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 30px;
        }}
        
        .meta-info p {{
            margin: 5px 0;
        }}
        
        .status {{
            display: inline-block;
            padding: 5px 15px;
            border-radius: 3px;
            font-weight: bold;
            text-transform: uppercase;
        }}
        
        .status.completed {{
            background: #2ecc71;
            color: white;
        }}
        
        .status.failed {{
            background: #e74c3c;
            color: white;
        }}
        
        .status.running {{
            background: #f39c12;
            color: white;
        }}
        
        .metric-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        
        .metric-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 5px;
            border-left: 4px solid #3498db;
        }}
        
        .metric-card h4 {{
            color: #7f8c8d;
            font-size: 0.9em;
            margin-bottom: 10px;
            text-transform: uppercase;
        }}
        
        .metric-card .value {{
            font-size: 2em;
            font-weight: bold;
            color: #2c3e50;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ecf0f1;
        }}
        
        th {{
            background: #34495e;
            color: white;
            font-weight: 600;
        }}
        
        tr:hover {{
            background: #f8f9fa;
        }}
        
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ecf0f1;
            text-align: center;
            color: #7f8c8d;
            font-size: 0.9em;
        }}
        
        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            
            .container {{
                box-shadow: none;
                padding: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>SEO Audit Report: {domain}</h1>
        
        <div class="meta-info">
            <p><strong>Status:</strong> <span class="status {status}">{status}</span></p>
            <p><strong>Started:</strong> {started_at}</p>
            <p><strong>Completed:</strong> {completed_at or 'In Progress'}</p>
        </div>
        
        <h2>Executive Summary</h2>
        {self._generate_summary_html(summary)}
        
        <h2>Crawl Analysis</h2>
        {self._generate_crawl_html(summary.get("crawl", {}))}
        
        <h2>Competitor Analysis</h2>
        {self._generate_competitors_html(summary.get("competitors", {}))}
        
        <h2>Backlink Profile</h2>
        {self._generate_backlinks_html(summary.get("backlinks", {}))}
        
        <h2>Keyword Rankings</h2>
        {self._generate_keywords_html(summary.get("keywords", {}))}
        
        {self._generate_ga4_html(summary.get("ga4")) if summary.get("ga4") else ""}
        
        {self._generate_gsc_html(summary.get("gsc")) if summary.get("gsc") else ""}
        
        <div class="footer">
            <p>Generated by SitePanda Desktop on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        </div>
    </div>
</body>
</html>
"""
        
        return html
    
    def _generate_summary_html(self, summary: Dict) -> str:
        """Generate summary metrics HTML."""
        return """
        <div class="metric-grid">
            <div class="metric-card">
                <h4>Audit Status</h4>
                <div class="value">Complete</div>
            </div>
        </div>
        """
    
    def _generate_crawl_html(self, crawl: Dict) -> str:
        """Generate crawl analysis HTML."""
        total_pages = crawl.get("total_pages", 0)
        crawl_status = crawl.get("crawl_status", "unknown")
        
        return f"""
        <div class="metric-grid">
            <div class="metric-card">
                <h4>Total Pages Crawled</h4>
                <div class="value">{total_pages}</div>
            </div>
            <div class="metric-card">
                <h4>Crawl Status</h4>
                <div class="value">{crawl_status}</div>
            </div>
        </div>
        """
    
    def _generate_competitors_html(self, competitors: Dict) -> str:
        """Generate competitors HTML."""
        count = competitors.get("competitor_count", 0)
        top_competitors = competitors.get("top_competitors", [])
        
        competitors_list = "".join(f"<li>{comp}</li>" for comp in top_competitors)
        
        return f"""
        <div class="metric-card">
            <h4>Competitors Found</h4>
            <div class="value">{count}</div>
        </div>
        
        <h3>Top Competitors</h3>
        <ul>
            {competitors_list if competitors_list else "<li>No competitors found</li>"}
        </ul>
        """
    
    def _generate_backlinks_html(self, backlinks: Dict) -> str:
        """Generate backlinks HTML."""
        total = backlinks.get("total_backlinks", 0)
        domains = backlinks.get("referring_domains", 0)
        ips = backlinks.get("referring_ips", 0)
        
        return f"""
        <div class="metric-grid">
            <div class="metric-card">
                <h4>Total Backlinks</h4>
                <div class="value">{total:,}</div>
            </div>
            <div class="metric-card">
                <h4>Referring Domains</h4>
                <div class="value">{domains:,}</div>
            </div>
            <div class="metric-card">
                <h4>Referring IPs</h4>
                <div class="value">{ips:,}</div>
            </div>
        </div>
        """
    
    def _generate_keywords_html(self, keywords: Dict) -> str:
        """Generate keywords HTML."""
        total = keywords.get("total_keywords", 0)
        top_keywords = keywords.get("top_keywords", [])
        
        rows = ""
        for kw in top_keywords:
            rows += f"""
            <tr>
                <td>{kw.get('keyword', '')}</td>
                <td>{kw.get('position', 0)}</td>
            </tr>
            """
        
        return f"""
        <div class="metric-card">
            <h4>Total Ranked Keywords</h4>
            <div class="value">{total:,}</div>
        </div>
        
        <h3>Top Keywords</h3>
        <table>
            <thead>
                <tr>
                    <th>Keyword</th>
                    <th>Position</th>
                </tr>
            </thead>
            <tbody>
                {rows if rows else "<tr><td colspan='2'>No keywords found</td></tr>"}
            </tbody>
        </table>
        """
    
    def _generate_ga4_html(self, ga4: Optional[Dict]) -> str:
        """Generate GA4 analytics HTML."""
        if not ga4:
            return ""
        
        total_pageviews = ga4.get("total_pageviews", 0)
        top_pages = ga4.get("top_pages", [])
        
        rows = ""
        for page in top_pages:
            rows += f"""
            <tr>
                <td>{page.get('path', '')}</td>
                <td>{page.get('views', 0):,}</td>
            </tr>
            """
        
        return f"""
        <h2>Google Analytics 4 Data</h2>
        
        <div class="metric-card">
            <h4>Total Pageviews (Last 28 Days)</h4>
            <div class="value">{total_pageviews:,}</div>
        </div>
        
        <h3>Top Pages by Views</h3>
        <table>
            <thead>
                <tr>
                    <th>Page Path</th>
                    <th>Views</th>
                </tr>
            </thead>
            <tbody>
                {rows if rows else "<tr><td colspan='2'>No data available</td></tr>"}
            </tbody>
        </table>
        """
    
    def _generate_gsc_html(self, gsc: Optional[Dict]) -> str:
        """Generate GSC search data HTML."""
        if not gsc:
            return ""
        
        total_clicks = gsc.get("total_clicks", 0)
        total_impressions = gsc.get("total_impressions", 0)
        avg_ctr = gsc.get("avg_ctr", 0)
        top_queries = gsc.get("top_queries", [])
        
        rows = ""
        for query in top_queries:
            rows += f"""
            <tr>
                <td>{query.get('query', '')}</td>
                <td>{query.get('clicks', 0):,}</td>
                <td>{query.get('position', 0):.1f}</td>
            </tr>
            """
        
        return f"""
        <h2>Google Search Console Data</h2>
        
        <div class="metric-grid">
            <div class="metric-card">
                <h4>Total Clicks (Last 28 Days)</h4>
                <div class="value">{total_clicks:,}</div>
            </div>
            <div class="metric-card">
                <h4>Total Impressions</h4>
                <div class="value">{total_impressions:,}</div>
            </div>
            <div class="metric-card">
                <h4>Average CTR</h4>
                <div class="value">{avg_ctr:.2f}%</div>
            </div>
        </div>
        
        <h3>Top Search Queries</h3>
        <table>
            <thead>
                <tr>
                    <th>Query</th>
                    <th>Clicks</th>
                    <th>Avg Position</th>
                </tr>
            </thead>
            <tbody>
                {rows if rows else "<tr><td colspan='3'>No data available</td></tr>"}
            </tbody>
        </table>
        """
    
    def _generate_pdf(self, html_content: str, domain: str, audit_id: str, timestamp: str) -> Path:
        """
        Generate PDF from HTML content.
        
        Args:
            html_content: HTML content
            domain: Domain name
            audit_id: Audit ID
            timestamp: Timestamp string
            
        Returns:
            Path to PDF file
        """
        try:
            from weasyprint import HTML
            
            pdf_filename = f"{domain}_{audit_id}_{timestamp}.pdf"
            pdf_path = self.output_dir / pdf_filename
            
            HTML(string=html_content).write_pdf(str(pdf_path))
            
            return pdf_path
        except ImportError:
            raise ImportError(
                "WeasyPrint not installed. Install with: pip install weasyprint"
            )
        except Exception as e:
            raise Exception(f"Failed to generate PDF: {e}")

