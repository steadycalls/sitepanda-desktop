# Duda Site Manager - User Guide

Complete guide to using the Duda Site Manager desktop application.

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [First-Time Setup](#first-time-setup)
4. [Main Interface](#main-interface)
5. [Fetching Data](#fetching-data)
6. [Viewing Data](#viewing-data)
7. [Webhook Configuration](#webhook-configuration)
8. [Advanced Features](#advanced-features)
9. [Troubleshooting](#troubleshooting)

---

## Introduction

Duda Site Manager is a desktop application that helps you manage your Duda websites by:

- Fetching data from the Duda API (sites, forms, orders, products, analytics)
- Storing data locally in a SQLite database for fast access
- Displaying data in an organized, tabbed interface
- Sending webhook notifications when events occur
- Pulling statistics from S3 (if provided by Duda)

### System Requirements

- **Operating System**: Windows 10+, macOS 10.14+, or Linux
- **Python**: Version 3.11 or higher
- **Internet Connection**: Required for API access
- **Duda Account**: With API access (Agency plan or higher)

---

## Installation

### Method 1: Using the Install Script (Recommended)

1. Extract the application files to a directory
2. Open a terminal/command prompt
3. Navigate to the application directory
4. Run the install script:

```bash
cd duda-manager
./install.sh
```

The script will:
- Check Python version
- Install all dependencies
- Run installation tests
- Confirm successful installation

### Method 2: Manual Installation

1. Extract the application files
2. Install dependencies:

```bash
cd duda-manager
pip3 install -r requirements.txt
```

3. Verify installation:

```bash
python3 test_installation.py
```

---

## First-Time Setup

### Step 1: Launch the Application

```bash
python3 app.py
```

### Step 2: Configure Credentials

When you first launch the application, you'll see a welcome message prompting you to configure your credentials.

Click **Settings** or go to **File → Settings** to open the Settings dialog.

### Step 3: Enter Duda API Credentials

In the **Duda API** tab:

1. **API Username**: Enter your Duda API username
2. **API Password**: Enter your Duda API password

**How to get Duda API credentials:**

1. Log in to your Duda account at https://my.duda.co
2. Navigate to **Settings → Developer Tools** (or **API Access**)
3. Click **Generate API Credentials** if you don't have them
4. Copy the **Username** and **Password**

**Important Notes:**
- API access requires a paid Duda plan (Agency, Custom, or higher)
- Keep your credentials secure and never share them
- The application encrypts credentials automatically

### Step 4: Configure S3 (Optional)

If Duda has provided you with S3 access for site statistics:

In the **Amazon S3** tab:

1. **Access Key ID**: Enter your AWS Access Key ID
2. **Secret Access Key**: Enter your AWS Secret Access Key
3. **Bucket Name**: Enter the S3 bucket name provided by Duda
4. **Region**: Enter the AWS region (usually `us-east-1`)

**Note**: Contact Duda support if you need S3 access credentials.

### Step 5: Configure Webhooks (Optional)

In the **Webhooks** tab, enter webhook URLs for the events you want to monitor:

- **New Form Submission**: Triggered when someone submits a contact form
- **New eCommerce Order**: Triggered when an order is placed
- **Daily Stats Summary**: Daily summary of all site statistics
- **New Blog Post**: Triggered when a blog post is published

Leave fields blank for events you don't want to monitor.

### Step 6: Configure App Settings

In the **App Settings** tab:

- **Auto-Fetch Interval**: How often to automatically check for new data (in seconds)
  - Minimum: 60 seconds
  - Default: 300 seconds (5 minutes)
  - Set to 0 to disable auto-fetch

- **Enable Notifications**: Check to receive desktop notifications for new events

### Step 7: Save Settings

Click **Save Settings** to save your configuration.

---

## Main Interface

The main window has several components:

### Header Bar

- **Title**: "Duda Site Manager"
- **Fetch Data Button**: Click to manually fetch data from Duda
- **Settings Button**: Open the Settings dialog

### Menu Bar

**File Menu:**
- Settings: Open Settings dialog
- Exit: Close the application

**Data Menu:**
- Fetch All Data: Manually fetch data from Duda
- Refresh Display: Reload data from local database

**Help Menu:**
- About: View application information

### Tabs

The main interface has 5 tabs:

1. **Sites**: View all your Duda websites
2. **Form Submissions**: View contact form submissions
3. **eCommerce Orders**: View customer orders
4. **Products**: View all products across your sites
5. **Analytics**: View site statistics (coming soon)

### Status Bar

At the bottom of the window:
- **Status Message**: Shows current operation status
- **Progress Bar**: Displays progress during data fetching

---

## Fetching Data

### Manual Fetch

1. Click the **Fetch Data** button in the header
2. The application will connect to Duda and retrieve:
   - All sites and their metadata
   - Form submissions
   - eCommerce products and orders
   - Site analytics
3. Progress is shown in the status bar
4. When complete, a summary dialog appears

### What Gets Fetched

For each site, the application retrieves:

- **Site Information**: Name, domain, publish status, template
- **Form Submissions**: All contact form entries with submitter details
- **eCommerce Data**: 
  - Products: Name, price, SKU, stock, images
  - Orders: Customer info, items, totals, status
- **Analytics**: Visitor stats, page views, traffic sources
- **Content**: Collections and blog posts

### Automatic Fetching

If you've configured an auto-fetch interval:

1. The application will automatically fetch data at the specified interval
2. New data triggers webhook notifications (if configured)
3. The display updates automatically

---

## Viewing Data

### Sites Tab

Displays all your Duda websites in a table:

| Column | Description |
|--------|-------------|
| Site Name | Internal Duda site identifier |
| Title | Site display name or domain |
| Domain | Primary domain for the site |
| Published | Whether the site is live |
| Store | Whether eCommerce is enabled |
| Blog | Whether blog is enabled |
| Last Updated | When data was last fetched |

**Tips:**
- Click column headers to sort
- Rows alternate colors for easier reading

### Form Submissions Tab

Displays all form submissions:

| Column | Description |
|--------|-------------|
| Site | Which site the form is from |
| Form Title | Name of the form |
| Submission Date | When the form was submitted |
| Name | Submitter's name |
| Email | Submitter's email |
| Webhook Sent | Whether webhook was sent |

**Viewing Details:**
- **Double-click** any row to view the full form data
- A dialog will show all form fields and values

### eCommerce Orders Tab

Displays all customer orders:

| Column | Description |
|--------|-------------|
| Site | Which site the order is from |
| Order # | Order number |
| Date | When the order was placed |
| Customer | Customer name |
| Email | Customer email |
| Total | Order total amount |
| Status | Order status (pending, completed, etc.) |

**Viewing Details:**
- **Double-click** any row to view full order details
- A dialog will show items, addresses, and payment info

### Products Tab

Displays all products across all sites:

| Column | Description |
|--------|-------------|
| Site | Which site the product belongs to |
| Product Name | Name of the product |
| SKU | Stock Keeping Unit |
| Price | Product price with currency |
| Stock | Available quantity |
| Active | Whether product is active |

### Analytics Tab

Displays site statistics and analytics data.

**Note**: This tab is currently a placeholder. Full analytics visualization will be added in a future version.

---

## Webhook Configuration

### What Are Webhooks?

Webhooks allow the application to automatically send data to external services when specific events occur. This enables integration with:

- **Zapier**: Automate workflows
- **Make (Integromat)**: Connect to other services
- **Slack**: Post notifications to channels
- **Discord**: Send messages to Discord servers
- **Custom APIs**: Your own backend services

### Setting Up Webhooks

1. Go to **Settings → Webhooks**
2. Enter webhook URLs for the events you want to monitor
3. Save settings

### Webhook Events

**New Form Submission:**
- Triggered when a new contact form is submitted
- Payload includes: site name, form title, submitter details, form data

**New eCommerce Order:**
- Triggered when a new order is placed
- Payload includes: order details, customer info, items, totals

**Daily Stats Summary:**
- Triggered once per day (manually or scheduled)
- Payload includes: total sites, form count, order count, revenue

**New Blog Post:**
- Triggered when a new blog post is published
- Payload includes: post title, author, content, publish date

### Webhook Payload Format

All webhooks send JSON data in this format:

```json
{
  "event_type": "new_form_submission",
  "timestamp": "2025-10-30T13:45:00",
  "data": {
    "site_name": "example-site",
    "form_title": "Contact Form",
    "submitter_name": "John Doe",
    "submitter_email": "john@example.com",
    "form_data": {
      "name": "John Doe",
      "email": "john@example.com",
      "message": "Hello!"
    }
  }
}
```

### Testing Webhooks

To test your webhook configuration:

1. Use a free webhook testing service:
   - **Webhook.site**: https://webhook.site
   - **RequestBin**: https://requestbin.com

2. Copy the test URL
3. Paste it into the webhook field in Settings
4. Fetch data or wait for a new event
5. Check the testing service to see the received payload

### Webhook Logs

All webhook activity is logged in the database. You can view logs by querying:

```bash
sqlite3 ~/.duda-manager/duda_data.db
SELECT * FROM webhook_log ORDER BY timestamp DESC LIMIT 20;
```

---

## Advanced Features

### Database Access

All data is stored in a SQLite database at:
```
~/.duda-manager/duda_data.db
```

You can access it directly for custom queries:

```bash
sqlite3 ~/.duda-manager/duda_data.db
```

**Useful Queries:**

```sql
-- View all sites
SELECT * FROM sites;

-- Recent form submissions
SELECT * FROM form_submissions 
ORDER BY submission_date DESC 
LIMIT 10;

-- Orders by revenue
SELECT * FROM ecommerce_orders 
ORDER BY total_amount DESC;

-- Webhook success rate
SELECT 
  event_type,
  COUNT(*) as total,
  SUM(success) as successful
FROM webhook_log 
GROUP BY event_type;
```

### Configuration Files

Configuration is stored in:
```
~/.duda-manager/config.enc (encrypted)
~/.duda-manager/key.key (encryption key)
```

**Security:**
- All credentials are encrypted using Fernet symmetric encryption
- Files have restricted permissions (600)
- Never share these files

### Exporting Data

To export data from the database:

```bash
# Export to CSV
sqlite3 -header -csv ~/.duda-manager/duda_data.db \
  "SELECT * FROM form_submissions;" > submissions.csv

# Export to JSON
sqlite3 ~/.duda-manager/duda_data.db \
  "SELECT json_object('site', site_name, 'email', submitter_email) 
   FROM form_submissions;" > submissions.json
```

---

## Troubleshooting

### Application Won't Start

**Error: "No module named 'PyQt6'"**

Solution: Install dependencies
```bash
pip3 install -r requirements.txt
```

**Error: "Python version too old"**

Solution: Upgrade to Python 3.11+
```bash
python3 --version  # Check current version
```

### Can't Connect to Duda

**Error: "Not Configured"**

Solution:
1. Go to Settings
2. Enter your Duda API credentials
3. Save settings

**Error: "Connection failed"**

Possible causes:
- Invalid API credentials
- No internet connection
- API access not enabled on your Duda account
- IP address not whitelisted (if required)

Solution:
1. Verify credentials in Duda dashboard
2. Check internet connection
3. Contact Duda support to verify API access

### No Data Appears

**After fetching, tables are empty**

Possible causes:
- No sites in your Duda account
- No data available (no forms, orders, etc.)
- API returned errors

Solution:
1. Check status bar for error messages
2. Verify you have sites in your Duda account
3. Check terminal output for API errors

### Webhooks Not Working

**Webhooks not being sent**

Possible causes:
- Webhook URL is incorrect
- Endpoint doesn't accept POST requests
- Endpoint requires authentication
- No new events to trigger webhooks

Solution:
1. Test webhook URL with webhook.site
2. Verify endpoint accepts POST with JSON
3. Check webhook log in database for errors
4. Ensure new data exists to trigger webhooks

**How to check webhook logs:**

```bash
sqlite3 ~/.duda-manager/duda_data.db
SELECT * FROM webhook_log ORDER BY timestamp DESC LIMIT 10;
```

### S3 Access Issues

**Error: "Access denied to bucket"**

Solution:
1. Verify AWS credentials are correct
2. Check bucket name is exact
3. Ensure IAM user has read permissions
4. Verify region is correct

### Performance Issues

**Application is slow**

Solution:
1. Reduce auto-fetch interval
2. Clear old data from database
3. Limit number of sites if possible

**Database is large**

Solution: Archive old data
```bash
# Backup database
cp ~/.duda-manager/duda_data.db ~/duda_backup.db

# Delete old records (example: older than 90 days)
sqlite3 ~/.duda-manager/duda_data.db \
  "DELETE FROM form_submissions 
   WHERE submission_date < date('now', '-90 days');"
```

---

## Getting Help

### Resources

- **README.md**: Full documentation
- **QUICK_START.md**: Quick start guide
- **This Guide**: Comprehensive user guide

### Support

For issues related to:

- **Duda API**: Contact Duda support at https://help.duda.co
- **This Application**: Check troubleshooting section above
- **Webhooks**: Test with webhook.site first

### Feedback

If you encounter bugs or have feature requests, please document:
1. What you were trying to do
2. What happened instead
3. Error messages (if any)
4. Steps to reproduce

---

## Tips and Best Practices

### Security

- Never share your API credentials
- Keep the `.duda-manager` directory secure
- Don't commit credentials to version control
- Use webhook URLs over HTTPS when possible

### Performance

- Set reasonable auto-fetch intervals (5-15 minutes)
- Archive old data periodically
- Use database queries for complex analysis

### Workflow

- Fetch data regularly to catch new submissions/orders
- Configure webhooks for real-time notifications
- Double-click rows to view full details
- Export data for reporting and analysis

### Integration

- Use Zapier to connect to 3000+ apps
- Send to Slack for team notifications
- Store in Google Sheets for analysis
- Trigger custom workflows with webhooks

---

**Enjoy using Duda Site Manager!**
