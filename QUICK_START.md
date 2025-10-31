# Quick Start Guide

Get up and running with Duda Site Manager in 5 minutes!

## Step 1: Install Dependencies

```bash
cd duda-manager
pip3 install -r requirements.txt
```

## Step 2: Run the Application

```bash
python3 app.py
```

## Step 3: Configure Your Credentials

When the application opens:

1. Click **Settings** button (or File → Settings)
2. In the **Duda API** tab:
   - Enter your Duda API Username
   - Enter your Duda API Password
3. (Optional) In the **Amazon S3** tab:
   - Enter S3 credentials if provided by Duda
4. (Optional) In the **Webhooks** tab:
   - Enter webhook URLs for events you want to monitor
5. Click **Save Settings**

### Where to Find Duda API Credentials

1. Log in to your Duda account
2. Go to **Settings → Developer Tools**
3. Generate or view your API credentials
4. Copy the Username and Password

**Note**: You need a paid Duda plan (Agency or higher) for API access.

## Step 4: Fetch Your Data

1. Click the **Fetch Data** button in the toolbar
2. Wait for the fetch to complete (progress shown in status bar)
3. View the summary of fetched data

## Step 5: Explore Your Data

Browse through the tabs:

- **Sites**: All your Duda websites
- **Form Submissions**: Contact form entries (double-click to view details)
- **eCommerce Orders**: Customer orders (double-click to view details)
- **Products**: All products across your sites
- **Analytics**: Site statistics

## Webhook Setup (Optional)

To receive notifications when events occur:

1. Go to **Settings → Webhooks**
2. Enter webhook URLs for the events you want:
   - **New Form Submission**: Notified when someone fills out a form
   - **New eCommerce Order**: Notified when an order is placed
   - **Daily Stats Summary**: Daily summary of all sites
   - **New Blog Post**: Notified when a blog post is published
3. Save settings

### Testing Webhooks

You can use these free services to test webhooks:

- **Webhook.site**: https://webhook.site (instant testing)
- **RequestBin**: https://requestbin.com
- **Zapier**: Create a webhook trigger
- **Discord**: Use a webhook URL from a Discord channel

## Tips

- **Auto-Refresh**: Set an auto-fetch interval in Settings → App Settings
- **View Details**: Double-click on form submissions or orders to see full details
- **Database Location**: Data is stored in `~/.duda-manager/duda_data.db`
- **Secure Storage**: All credentials are encrypted automatically

## Common Issues

### "Not Configured" Error
→ Go to Settings and enter your Duda API credentials

### Can't Connect to Duda
→ Check your API credentials and internet connection

### Webhooks Not Working
→ Verify the webhook URL is correct and accepts POST requests

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Set up automatic data fetching
- Configure webhooks for your workflow
- Explore the database for custom queries

## Need Help?

- Check the [README.md](README.md) troubleshooting section
- Contact Duda support for API-related issues
- Review webhook logs in the database

---

**You're all set!** The application will now fetch and display your Duda site data, and send webhooks when configured.
