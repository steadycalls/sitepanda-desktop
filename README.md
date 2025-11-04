# SitePanda Desktop

A desktop application for managing Duda websites, fetching site data, and sending webhook notifications.

[![GitHub](https://img.shields.io/badge/GitHub-sitepanda--desktop-blue?logo=github)](https://github.com/steadycalls/sitepanda-desktop)
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## Features

**SitePanda Desktop** provides a comprehensive solution for managing your Duda websites with the following capabilities:

### Data Management
- Fetches and stores site information, form submissions, eCommerce orders, products, and analytics from the Duda API
- Integrates with S3 to pull site statistics from Duda-provided buckets
- Stores all data locally in an encrypted SQLite database for fast access and offline viewing

### SEO Audit Tools
- Comprehensive SEO audits powered by DataForSEO API
- On-page crawls, keyword rankings, backlink analysis, and competitor research
- Optional Google Analytics 4 (GA4) integration for traffic metrics
- Optional Google Search Console (GSC) integration for search performance data
- Automated HTML and PDF report generation
- Webhook notifications when audits complete

### User Interface
- Clean, tabbed desktop interface built with PyQt6
- Separate views for Sites, Form Submissions, eCommerce Orders, Products, and Analytics
- Double-click any row to view detailed information
- Real-time progress indicators and status updates

### Webhook System
- Automatically sends data to configured webhook URLs when events occur
- Supports webhooks for: new form submissions, new eCommerce orders, daily stats summaries, and new blog posts
- All webhook activity is logged for monitoring and debugging

### Security
- All credentials (Duda API, S3, webhooks) are encrypted using Fernet symmetric encryption
- Secure file permissions prevent unauthorized access
- Built-in settings dialog where you can safely input all your credentials

## Quick Installation

### One-Click Install

**Linux/macOS:**
```bash
git clone https://github.com/steadycalls/sitepanda-desktop.git
cd sitepanda-desktop
./install_sitepanda.sh
```

**Windows:**
```cmd
git clone https://github.com/steadycalls/sitepanda-desktop.git
cd sitepanda-desktop
install_sitepanda.bat
```

The installer will:
- Check Python version (3.11+ required)
- Install all dependencies
- Run installation tests
- Optionally create desktop shortcuts

### Manual Installation

1. **Clone the repository:**
```bash
git clone https://github.com/steadycalls/sitepanda-desktop.git
cd sitepanda-desktop
```

2. **Install dependencies:**
```bash
pip3 install -r requirements.txt
```

3. **Verify installation:**
```bash
python3 test_installation.py
```

4. **Run the application:**
```bash
python3 app.py
```

## Desktop Shortcuts

Create desktop shortcuts for easy access:

**Linux:**
```bash
./create_desktop_shortcut_linux.sh
```

**macOS:**
```bash
./create_desktop_shortcut_macos.sh
```

**Windows:**
```cmd
create_desktop_shortcut_windows.bat
```

## First-Time Setup

When you first launch SitePanda Desktop, you'll be prompted to configure your credentials:

1. **Duda API Credentials** (Required)
   - API Username
   - API Password
   - Get these from your Duda account: Settings → Developer Tools

2. **AWS S3 Credentials** (Optional)
   - Access Key ID
   - Secret Access Key
   - Bucket Name
   - Region (usually `us-east-1`)
   - Required only if Duda provides S3 access for site statistics

3. **Webhook URLs** (Optional)
   - Configure URLs for events you want to monitor
   - Supports: form submissions, orders, stats, blog posts

4. **App Settings**
   - Auto-fetch interval (default: 5 minutes)
   - Enable/disable notifications

All credentials are encrypted and stored securely in `~/.sitepanda-desktop/`

## Usage

### Fetching Data

Click the **Fetch Data** button to retrieve all your site data from Duda. The application will:
- Connect to the Duda API
- Fetch sites, forms, orders, products, and analytics
- Store data in the local database
- Send webhook notifications for new events
- Display results in organized tabs

### Viewing Data

Browse through the tabs to view different types of data:
- **Sites**: All your Duda websites
- **Form Submissions**: Contact form entries (double-click for details)
- **eCommerce Orders**: Customer orders (double-click for details)
- **Products**: All products across your sites
- **Analytics**: Site statistics

### Webhooks

Configure webhook URLs in Settings to receive real-time notifications when:
- A new form is submitted
- A new order is placed
- Daily statistics are available
- A new blog post is published

Webhooks send JSON payloads via POST requests. Test with services like:
- [Webhook.site](https://webhook.site)
- [Zapier](https://zapier.com)
- [Make (Integromat)](https://make.com)
- [Slack](https://slack.com)
- [Discord](https://discord.com)

## Documentation

- **[QUICK_START.md](QUICK_START.md)** - 5-minute setup guide
- **[USER_GUIDE.md](USER_GUIDE.md)** - Comprehensive user manual
- **[SEO_AUDIT_GUIDE.md](SEO_AUDIT_GUIDE.md)** - SEO audit feature guide
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Technical overview

## System Requirements

- **Operating System**: Windows 10+, macOS 10.14+, or Linux
- **Python**: Version 3.11 or higher
- **Internet Connection**: Required for API access
- **Duda Account**: With API access (Agency plan or higher)

## Dependencies

```
requests>=2.31.0      # HTTP client
boto3>=1.28.0         # AWS SDK
PyQt6>=6.5.0          # GUI framework
cryptography>=41.0.0  # Encryption
python-dotenv>=1.0.0  # Environment config
```

## Project Structure

```
sitepanda-desktop/
├── app.py                              # Main application entry point
├── requirements.txt                    # Python dependencies
├── install_sitepanda.sh               # One-click installer (Linux/macOS)
├── install_sitepanda.bat              # One-click installer (Windows)
├── create_desktop_shortcut_linux.sh   # Desktop shortcut creator (Linux)
├── create_desktop_shortcut_macos.sh   # Desktop shortcut creator (macOS)
├── create_desktop_shortcut_windows.bat # Desktop shortcut creator (Windows)
├── test_installation.py               # Installation verification
├── README.md                          # This file
├── QUICK_START.md                     # Quick start guide
├── USER_GUIDE.md                      # User manual
├── PROJECT_SUMMARY.md                 # Technical overview
└── modules/                           # Application modules
    ├── config_manager.py              # Encrypted credential storage
    ├── database.py                    # SQLite database operations
    ├── duda_client.py                 # Duda REST API client
    ├── s3_client.py                   # AWS S3 client
    ├── data_fetcher.py                # Data fetching orchestration
    ├── webhook_manager.py             # Webhook notification system
    ├── main_window.py                 # Main GUI window
    └── settings_dialog.py             # Settings configuration UI
```

## Troubleshooting

### Application Won't Start

**Error: "No module named 'PyQt6'"**
```bash
pip3 install -r requirements.txt
```

**Error: "Python version too old"**
- Upgrade to Python 3.11+
- Check version: `python3 --version`

### Can't Connect to Duda

**Error: "Not Configured"**
1. Go to Settings
2. Enter your Duda API credentials
3. Save settings

**Error: "Connection failed"**
- Verify credentials in Duda dashboard
- Check internet connection
- Contact Duda support to verify API access

### Webhooks Not Working

1. Test webhook URL with [webhook.site](https://webhook.site)
2. Verify endpoint accepts POST requests with JSON
3. Check webhook log in database for errors:
```bash
sqlite3 ~/.sitepanda-desktop/sitepanda_data.db
SELECT * FROM webhook_log ORDER BY timestamp DESC LIMIT 10;
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues related to:
- **Duda API**: Contact Duda support at https://help.duda.co
- **This Application**: Open an issue on GitHub
- **Feature Requests**: Open an issue on GitHub

## License

This project is provided as-is for managing Duda sites. Use at your own discretion.

## Version History

### Version 1.1 (2025-11-03)
- Added comprehensive SEO audit functionality
- DataForSEO API integration for crawls, keywords, backlinks, competitors
- Optional GA4 integration for traffic analytics
- Optional GSC integration for search performance
- Automated HTML and PDF report generation
- SEO audit webhook notifications

### Version 1.0 (2025-10-30)
- Initial release
- Duda API integration
- S3 statistics support
- Webhook notifications
- Desktop GUI with PyQt6
- Encrypted credential storage
- SQLite database storage
- Cross-platform desktop shortcuts
- One-click installers

## Credits

Built with:
- [Python](https://www.python.org/)
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/)
- [Duda REST API](https://developer.duda.co/)
- [AWS SDK for Python (Boto3)](https://boto3.amazonaws.com/)

---

**GitHub Repository**: https://github.com/steadycalls/sitepanda-desktop

**Made with ❤️ for SitePanda users**
