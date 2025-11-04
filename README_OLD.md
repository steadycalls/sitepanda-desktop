# Duda Site Manager

A desktop application for managing Duda websites, fetching site data, and sending webhook notifications.

## Features

- **Fetch Duda Site Data**: Automatically retrieve data from your Duda sites via the Duda API
  - Site information and metadata
  - Form submissions from contact forms
  - eCommerce products and orders
  - Site analytics and statistics
  - Content collections and blog posts

- **S3 Integration**: Pull site statistics from Duda-provided S3 buckets

- **Local Database Storage**: All data is stored locally in SQLite for fast access and offline viewing

- **Webhook Notifications**: Automatically send data to webhook URLs when events occur:
  - New form submissions
  - New eCommerce orders
  - Daily statistics summaries
  - New blog posts

- **User-Friendly Interface**: Clean, tabbed interface for viewing all your data

## Installation

### Prerequisites

- Python 3.11 or higher
- pip (Python package installer)

### Install Dependencies

```bash
cd duda-manager
pip3 install -r requirements.txt
```

The following packages will be installed:
- `requests` - For API communication
- `boto3` - For AWS S3 integration
- `PyQt6` - For the desktop GUI
- `cryptography` - For secure credential storage
- `python-dotenv` - For environment configuration

## Configuration

### 1. Duda API Credentials

To use this application, you need Duda API credentials:

1. Log in to your Duda account
2. Navigate to **Settings → Developer Tools** or **API Access**
3. Generate or view your API credentials
4. Copy the **Username** and **Password**

**Note**: API access requires a paid Duda plan (Agency, Custom, or higher).

### 2. AWS S3 Credentials (Optional)

If Duda provides S3 access for your white-label site statistics:

1. Contact Duda support to obtain S3 credentials
2. You'll need:
   - AWS Access Key ID
   - AWS Secret Access Key
   - S3 Bucket Name
   - AWS Region (usually `us-east-1`)

### 3. Webhook URLs (Optional)

Configure webhook URLs to receive notifications when events occur. The application sends POST requests with JSON payloads to these URLs.

Example webhook services you can use:
- **Zapier**: Create a webhook trigger
- **Make (Integromat)**: Set up a webhook module
- **Custom Server**: Any endpoint that accepts POST requests
- **Slack**: Use incoming webhooks
- **Discord**: Use webhook URLs

## Usage

### Running the Application

```bash
cd duda-manager
python3 app.py
```

Or make it executable and run directly:

```bash
chmod +x app.py
./app.py
```

### First-Time Setup

1. When you first run the application, you'll be prompted to configure your credentials
2. Click **Settings** or go to **File → Settings**
3. Enter your credentials in the appropriate tabs:
   - **Duda API**: Enter your API username and password
   - **Amazon S3**: (Optional) Enter S3 credentials if provided by Duda
   - **Webhooks**: (Optional) Enter webhook URLs for events you want to monitor
   - **App Settings**: Configure auto-fetch interval and notifications
4. Click **Save Settings**

### Fetching Data

1. Click the **Fetch Data** button in the toolbar, or go to **Data → Fetch All Data**
2. The application will retrieve all available data from your Duda sites
3. Progress will be shown in the status bar
4. Once complete, you'll see a summary of fetched data

### Viewing Data

The application has multiple tabs for different data types:

- **Sites**: View all your Duda sites with their status
- **Form Submissions**: See all form submissions with contact details
  - Double-click a row to view full form data
- **eCommerce Orders**: View all orders with customer and payment information
  - Double-click a row to view full order details
- **Products**: Browse all products across your sites
- **Analytics**: View site statistics and analytics data

### Webhooks

Webhooks are automatically processed after each data fetch. The application will:

1. Detect new form submissions and orders
2. Send POST requests to configured webhook URLs
3. Mark records as processed to avoid duplicate notifications
4. Log all webhook activity in the database

#### Webhook Payload Format

All webhooks send JSON data in this format:

```json
{
  "event_type": "new_form_submission",
  "timestamp": "2025-10-30T13:45:00",
  "data": {
    // Event-specific data here
  }
}
```

#### Event Types

- **new_form_submission**: Triggered when a new form is submitted
- **new_ecommerce_order**: Triggered when a new order is placed
- **daily_stats_summary**: Daily summary of site statistics
- **new_blog_post**: Triggered when a new blog post is published

## Data Storage

All data is stored locally in:
- **Database**: `/home/ubuntu/.duda-manager/duda_data.db` (SQLite)
- **Configuration**: `/home/ubuntu/.duda-manager/config.enc` (Encrypted)
- **Encryption Key**: `/home/ubuntu/.duda-manager/key.key` (Secure)

**Security**: All credentials are encrypted using Fernet symmetric encryption. The encryption key is stored with restricted file permissions (600).

## Troubleshooting

### "Not Configured" Error

If you see this error when trying to fetch data:
1. Go to **Settings**
2. Verify your Duda API credentials are entered correctly
3. Click **Save Settings**
4. Try fetching data again

### Connection Errors

If the application can't connect to Duda:
1. Check your internet connection
2. Verify your API credentials are correct
3. Ensure your Duda account has API access enabled
4. Check if your IP is whitelisted (if required by your Duda plan)

### S3 Access Errors

If S3 integration isn't working:
1. Verify your AWS credentials are correct
2. Check the bucket name matches exactly
3. Ensure the IAM user has read permissions for the bucket
4. Verify the region is correct

### Webhook Failures

If webhooks aren't being delivered:
1. Check the webhook URL is correct and accessible
2. Verify the endpoint accepts POST requests with JSON
3. Check the webhook log in the database for error details
4. Test the webhook URL manually with a tool like Postman

## Advanced Features

### Auto-Fetch

Configure automatic data fetching in **Settings → App Settings**:
- Set the **Auto-Fetch Interval** (in seconds)
- The application will automatically fetch new data at this interval
- Minimum interval: 60 seconds (1 minute)
- Default: 300 seconds (5 minutes)

### Database Access

You can access the SQLite database directly for custom queries:

```bash
sqlite3 ~/.duda-manager/duda_data.db
```

Example queries:

```sql
-- View all sites
SELECT * FROM sites;

-- View recent form submissions
SELECT * FROM form_submissions ORDER BY submission_date DESC LIMIT 10;

-- View orders by total amount
SELECT * FROM ecommerce_orders ORDER BY total_amount DESC;

-- View webhook log
SELECT * FROM webhook_log ORDER BY timestamp DESC LIMIT 20;
```

## Architecture

The application is built with a modular architecture:

- **app.py**: Main application controller
- **modules/config_manager.py**: Encrypted configuration storage
- **modules/database.py**: SQLite database operations
- **modules/duda_client.py**: Duda REST API client
- **modules/s3_client.py**: AWS S3 client
- **modules/data_fetcher.py**: Data fetching orchestration
- **modules/webhook_manager.py**: Webhook notification system
- **modules/main_window.py**: Main GUI window
- **modules/settings_dialog.py**: Settings configuration dialog

## API Reference

### Duda API Endpoints Used

- `GET /api/sites/multiscreen` - List all sites
- `GET /api/sites/multiscreen/{site_name}` - Get site details
- `GET /api/sites/multiscreen/analytics/{site_name}` - Get analytics
- `GET /api/sites/multiscreen/{site_name}/forms` - Get form submissions
- `GET /api/sites/multiscreen/{site_name}/ecommerce/products` - List products
- `GET /api/sites/multiscreen/{site_name}/ecommerce/orders` - List orders
- `GET /api/sites/multiscreen/{site_name}/blog/posts` - List blog posts
- `GET /api/sites/multiscreen/{site_name}/collection` - List collections

For full API documentation, visit: https://developer.duda.co/reference

## License

This application is provided as-is for managing Duda sites. Use at your own discretion.

## Support

For issues related to:
- **Duda API**: Contact Duda support or visit https://help.duda.co
- **This Application**: Check the troubleshooting section above

## Version History

### Version 1.0 (2025-10-30)
- Initial release
- Duda API integration
- S3 statistics support
- Webhook notifications
- Desktop GUI with PyQt6
- Encrypted credential storage
- SQLite database storage
