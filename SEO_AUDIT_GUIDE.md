# SEO Audit Feature Guide

## Overview

SitePanda Desktop now includes comprehensive SEO audit functionality powered by DataForSEO API, with optional integration for Google Analytics 4 (GA4) and Google Search Console (GSC). This feature allows you to run detailed SEO audits on any domain, analyze crawl data, backlinks, keywords, and generate professional reports.

## Features

### Core Capabilities

**DataForSEO Integration:**
- **On-Page Crawl**: Crawl up to 500 pages per domain to identify technical SEO issues
- **Keyword Rankings**: Discover which keywords the domain ranks for
- **Backlink Analysis**: Analyze backlink profile, referring domains, and referring IPs
- **Competitor Analysis**: Identify top organic search competitors
- **Domain Metrics**: Get authority scores and traffic estimates

**Optional GA4 Integration:**
- Page-level analytics (views, sessions, engagement)
- Landing page performance
- Device and geographic breakdowns
- Traffic source analysis

**Optional GSC Integration:**
- Search query performance
- Click-through rates (CTR)
- Average positions
- Impressions and clicks by page
- Device and country breakdowns

**Report Generation:**
- Professional HTML reports with styled tables and charts
- PDF export capability
- Downloadable reports saved locally
- Webhook notifications when audits complete

## Setup

### 1. DataForSEO API (Required)

DataForSEO provides the core crawl and analysis functionality.

**Sign Up:**
1. Visit [https://dataforseo.com](https://dataforseo.com)
2. Create an account
3. Subscribe to a plan (starts at $50/month with credits)
4. Get your login credentials (email and password or API key)

**Configure in SitePanda:**
1. Open SitePanda Desktop
2. Go to **Settings** → **SEO Tools** tab
3. Enter your DataForSEO Login/Email
4. Enter your DataForSEO Password
5. Click **Save Settings**

### 2. Google Analytics 4 (Optional)

GA4 integration provides traffic and engagement metrics.

**Prerequisites:**
- A Google Cloud project
- Analytics Data API enabled
- A service account with access to your GA4 property

**Setup Steps:**

1. **Create Google Cloud Project:**
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Create a new project or select existing

2. **Enable Analytics Data API:**
   - In your project, go to **APIs & Services** → **Library**
   - Search for "Google Analytics Data API"
   - Click **Enable**

3. **Create Service Account:**
   - Go to **IAM & Admin** → **Service Accounts**
   - Click **Create Service Account**
   - Give it a name (e.g., "sitepanda-analytics")
   - Click **Create and Continue**
   - Skip role assignment (we'll add in GA4)
   - Click **Done**

4. **Download Service Account Key:**
   - Click on the service account you just created
   - Go to **Keys** tab
   - Click **Add Key** → **Create New Key**
   - Select **JSON** format
   - Click **Create** (file downloads automatically)
   - Save this file securely (e.g., `~/google-service-account.json`)

5. **Grant Access in GA4:**
   - Go to [Google Analytics](https://analytics.google.com)
   - Select your GA4 property
   - Go to **Admin** (gear icon)
   - Under **Property**, click **Property Access Management**
   - Click **+** to add users
   - Enter the service account email (looks like `name@project-id.iam.gserviceaccount.com`)
   - Select **Viewer** or **Analyst** role
   - Click **Add**

6. **Get GA4 Property ID:**
   - In GA4, go to **Admin** → **Property Settings**
   - Note the **Property ID** (format: `properties/123456789`)

7. **Configure in SitePanda:**
   - Go to **Settings** → **SEO Tools** tab
   - In "Google Analytics 4" section, enter the path to your service account JSON file
   - Click **Save Settings**

### 3. Google Search Console (Optional)

GSC integration provides search query and position data.

**Prerequisites:**
- A Google Cloud project (can be same as GA4)
- Search Console API enabled
- A service account with access to your GSC property

**Setup Steps:**

1. **Enable Search Console API:**
   - In [Google Cloud Console](https://console.cloud.google.com)
   - Go to **APIs & Services** → **Library**
   - Search for "Google Search Console API"
   - Click **Enable**

2. **Use Same Service Account:**
   - You can use the same service account JSON file from GA4 setup
   - Or create a new one following the same steps

3. **Grant Access in Search Console:**
   - Go to [Google Search Console](https://search.google.com/search-console)
   - Select your property
   - Click **Settings** (gear icon)
   - Click **Users and permissions**
   - Click **Add user**
   - Enter the service account email
   - Select **Full** permission
   - Click **Add**

4. **Configure in SitePanda:**
   - Go to **Settings** → **SEO Tools** tab
   - In "Google Search Console" section, enter the path to your service account JSON file
   - Can be the same file as GA4
   - Click **Save Settings**

## Running an Audit

### Starting an Audit

1. Open SitePanda Desktop
2. Go to the **SEO Audits** tab
3. Click **Run New Audit** button
4. Enter the domain to audit (e.g., `example.com`)
5. Optionally enter GA4 Property ID if you have GA4 configured
6. Click **Start Audit**

### Audit Process

The audit runs in the background and typically takes 5-15 minutes depending on:
- Number of pages to crawl
- DataForSEO API response time
- Whether GA4/GSC are enabled

**Progress Indicators:**
- Status bar shows current step
- Progress bar displays activity
- Audit status updates in the table

### Viewing Results

**In the Application:**
1. Audits appear in the **SEO Audits** tab table
2. Double-click any audit row to view summary
3. Status colors:
   - **Green**: Completed successfully
   - **Red**: Failed (check error message)
   - **Blue**: Currently running

**Reports:**
- HTML and PDF reports are automatically generated
- Saved to `~/.sitepanda-desktop/reports/`
- Filename format: `domain_auditid_timestamp.html`

## Understanding Audit Data

### Crawl Analysis

**Metrics Provided:**
- Total pages crawled
- HTTP status codes (200, 301, 302, 404, 500, etc.)
- Page load times
- Duplicate titles and meta descriptions
- Missing H1 tags
- Broken links
- Image optimization issues

### Keyword Rankings

**Data Included:**
- Keywords the domain ranks for
- Current position in search results
- Search volume estimates
- Keyword difficulty scores
- Top-ranking pages for each keyword

### Backlink Profile

**Metrics:**
- Total backlinks
- Referring domains
- Referring IPs
- Domain authority of referring sites
- Anchor text distribution
- Follow vs. nofollow ratio

### Competitor Analysis

**Insights:**
- Top 10-50 organic competitors
- Shared keywords
- Competitor ranking positions
- Traffic estimates

### GA4 Data (if configured)

**Metrics:**
- Total pageviews (last 28 days)
- Sessions and engaged sessions
- Engagement rate
- Average session duration
- Top pages by traffic
- Device breakdown
- Geographic distribution
- Traffic sources

### GSC Data (if configured)

**Metrics:**
- Total clicks (last 28 days)
- Total impressions
- Average CTR
- Average position
- Top search queries
- Query-level click and impression data
- Device and country breakdowns

## Reports

### HTML Report

Professional HTML report includes:
- Executive summary with key metrics
- Crawl analysis section
- Competitor analysis
- Backlink profile overview
- Keyword rankings table
- GA4 analytics (if available)
- GSC search data (if available)
- Styled with responsive CSS
- Printable format

### PDF Report

- Same content as HTML report
- Professional formatting
- Suitable for client delivery
- Generated using WeasyPrint

### Accessing Reports

**From Application:**
1. Go to **SEO Audits** tab
2. Right-click on audit row
3. Select "Open Report" (feature coming soon)

**From File System:**
```bash
# macOS/Linux
open ~/.sitepanda-desktop/reports/

# Windows
explorer %USERPROFILE%\.sitepanda-desktop\reports\
```

## Webhooks

### Audit Complete Webhook

Get notified when audits finish.

**Setup:**
1. Go to **Settings** → **SEO Tools** tab
2. In "SEO Audit Webhooks" section
3. Enter your webhook URL
4. Click **Save Settings**

**Webhook Payload:**
```json
{
  "event": "audit_complete",
  "audit_id": 123,
  "domain": "example.com",
  "status": "completed",
  "started_at": "2025-10-30T10:00:00",
  "completed_at": "2025-10-30T10:15:00",
  "report_url": "/path/to/report.html",
  "summary": {
    "total_pages": 250,
    "total_backlinks": 1500,
    "referring_domains": 85,
    "ranked_keywords": 120
  }
}
```

## Troubleshooting

### DataForSEO Issues

**Error: "Authentication failed"**
- Verify login credentials in Settings
- Check that your DataForSEO account is active
- Ensure you have sufficient credits

**Error: "Crawl task timed out"**
- Large sites may take longer
- Try reducing max crawl pages
- Check DataForSEO service status

### GA4 Issues

**Error: "Failed to initialize GA4 client"**
- Verify service account JSON file path is correct
- Ensure Analytics Data API is enabled
- Check service account has access to GA4 property

**Error: "Permission denied"**
- Verify service account email is added to GA4 property
- Ensure role is Viewer or Analyst
- Check Property ID format (should be `properties/123456789`)

### GSC Issues

**Error: "Failed to initialize GSC client"**
- Verify service account JSON file path is correct
- Ensure Search Console API is enabled
- Check service account has access to GSC property

**Error: "Site not found"**
- Verify service account email is added to Search Console
- Ensure permission level is Full
- Check domain format (should be `https://example.com/`)

### Report Generation Issues

**Error: "Failed to generate PDF"**
- Ensure WeasyPrint is installed: `pip install weasyprint`
- On Windows, may need Visual C++ redistributables
- HTML report will still be generated

## Best Practices

### Audit Frequency

**Recommended Schedule:**
- **New sites**: Weekly for first month, then monthly
- **Established sites**: Monthly or quarterly
- **After major changes**: Immediately after site updates
- **Competitive analysis**: Quarterly

### Crawl Limits

**DataForSEO Credits:**
- Each crawl uses credits based on pages crawled
- Start with 500 pages max
- Increase for larger sites as needed
- Monitor credit usage in DataForSEO dashboard

### Data Retention

**Audit History:**
- Audits are stored in local SQLite database
- Reports saved to disk indefinitely
- Consider archiving old reports periodically
- Database location: `~/.sitepanda-desktop/sitepanda_data.db`

### Integration Tips

**GA4 + GSC Together:**
- Use same service account for both
- Provides complete picture: traffic + search
- Cross-reference data for insights
- GA4 for behavior, GSC for acquisition

**Webhook Integration:**
- Use with Zapier, Make, or custom endpoints
- Automate report delivery to clients
- Trigger follow-up tasks
- Log audit completion in project management tools

## API Costs

### DataForSEO Pricing

**Typical Costs:**
- On-page crawl: ~$0.10 per 100 pages
- Keyword rankings: ~$0.01 per keyword
- Backlinks: ~$0.10 per domain
- Competitor analysis: ~$0.05 per request

**Example Audit Cost:**
- 500 page crawl: $0.50
- 100 keywords: $1.00
- Backlinks: $0.10
- Competitors: $0.05
- **Total**: ~$1.65 per audit

**Plans:**
- Pay-as-you-go: $50 minimum
- Monthly subscriptions available
- Volume discounts for agencies

### Google APIs

**GA4 and GSC:**
- **Free** for standard usage
- No cost for API calls
- Only requires Google Cloud project (free tier)

## Support

### Getting Help

**DataForSEO:**
- Documentation: [https://docs.dataforseo.com](https://docs.dataforseo.com)
- Support: support@dataforseo.com
- API Status: [https://status.dataforseo.com](https://status.dataforseo.com)

**Google APIs:**
- GA4 API Docs: [https://developers.google.com/analytics/devguides/reporting/data/v1](https://developers.google.com/analytics/devguides/reporting/data/v1)
- GSC API Docs: [https://developers.google.com/webmaster-tools/v1](https://developers.google.com/webmaster-tools/v1)

**SitePanda Desktop:**
- GitHub Issues: [https://github.com/steadycalls/sitepanda-desktop/issues](https://github.com/steadycalls/sitepanda-desktop/issues)
- Documentation: See README.md and USER_GUIDE.md

## Advanced Usage

### Custom Crawl Parameters

Edit `modules/dataforseo_client.py` to customize:
- Max crawl pages
- JavaScript rendering
- Custom user agents
- Crawl depth limits

### Custom Report Templates

Edit `modules/report_generator.py` to:
- Customize HTML styling
- Add custom metrics
- Change report layout
- Add company branding

### Automated Audits

Schedule regular audits using system cron or Task Scheduler:

**Linux/macOS (cron):**
```bash
# Run audit every Monday at 9 AM
0 9 * * 1 /usr/bin/python3 /path/to/sitepanda-desktop/audit_script.py example.com
```

**Windows (Task Scheduler):**
Create a scheduled task to run audit script weekly.

---

**Happy Auditing!**

For more information, see the main [README.md](README.md) and [USER_GUIDE.md](USER_GUIDE.md).
