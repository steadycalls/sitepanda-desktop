"""
Settings Dialog Module
Provides UI for configuring API credentials and webhook URLs.
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget,
    QLabel, QLineEdit, QPushButton, QGroupBox, QFormLayout,
    QMessageBox, QSpinBox, QCheckBox
)
from PyQt6.QtCore import Qt
from modules.config_manager import ConfigManager


class SettingsDialog(QDialog):
    """Dialog for managing application settings and credentials."""
    
    def __init__(self, config_manager: ConfigManager, parent=None):
        super().__init__(parent)
        self.config_manager = config_manager
        self.setWindowTitle("Settings")
        self.setMinimumWidth(600)
        self.setMinimumHeight(500)
        
        self._init_ui()
        self._load_current_settings()
    
    def _init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout()
        
        # Create tab widget
        tabs = QTabWidget()
        
        # Duda API tab
        duda_tab = self._create_duda_tab()
        tabs.addTab(duda_tab, "Duda API")
        
        # S3 tab
        s3_tab = self._create_s3_tab()
        tabs.addTab(s3_tab, "Amazon S3")
        
        # Webhooks tab
        webhooks_tab = self._create_webhooks_tab()
        tabs.addTab(webhooks_tab, "Webhooks")
        
        # SEO Tools tab
        seo_tab = self._create_seo_tab()
        tabs.addTab(seo_tab, "SEO Tools")
        
        # App Settings tab
        app_tab = self._create_app_settings_tab()
        tabs.addTab(app_tab, "App Settings")
        
        layout.addWidget(tabs)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        save_btn = QPushButton("Save Settings")
        save_btn.clicked.connect(self._save_settings)
        button_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def _create_duda_tab(self) -> QWidget:
        """Create Duda API credentials tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Credentials group
        creds_group = QGroupBox("API Credentials")
        creds_layout = QFormLayout()
        
        self.duda_user_input = QLineEdit()
        self.duda_user_input.setPlaceholderText("Enter your Duda API username")
        creds_layout.addRow("API Username:", self.duda_user_input)
        
        self.duda_password_input = QLineEdit()
        self.duda_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.duda_password_input.setPlaceholderText("Enter your Duda API password")
        creds_layout.addRow("API Password:", self.duda_password_input)
        
        creds_group.setLayout(creds_layout)
        layout.addWidget(creds_group)
        
        # Info label
        info_label = QLabel(
            "<b>How to get Duda API credentials:</b><br>"
            "1. Log in to your Duda account<br>"
            "2. Navigate to Settings → Developer Tools<br>"
            "3. Generate or view your API credentials<br>"
            "4. Copy the Username and Password here<br><br>"
            "<i>Note: API access requires a paid Duda plan (Agency or higher)</i>"
        )
        info_label.setWordWrap(True)
        info_label.setStyleSheet("padding: 10px; background-color: #f0f0f0; border-radius: 5px;")
        layout.addWidget(info_label)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def _create_s3_tab(self) -> QWidget:
        """Create S3 credentials tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # S3 credentials group
        s3_group = QGroupBox("S3 Credentials")
        s3_layout = QFormLayout()
        
        self.s3_access_key_input = QLineEdit()
        self.s3_access_key_input.setPlaceholderText("AWS Access Key ID")
        s3_layout.addRow("Access Key ID:", self.s3_access_key_input)
        
        self.s3_secret_key_input = QLineEdit()
        self.s3_secret_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.s3_secret_key_input.setPlaceholderText("AWS Secret Access Key")
        s3_layout.addRow("Secret Access Key:", self.s3_secret_key_input)
        
        self.s3_bucket_input = QLineEdit()
        self.s3_bucket_input.setPlaceholderText("Bucket name provided by Duda")
        s3_layout.addRow("Bucket Name:", self.s3_bucket_input)
        
        self.s3_region_input = QLineEdit()
        self.s3_region_input.setPlaceholderText("us-east-1")
        s3_layout.addRow("Region:", self.s3_region_input)
        
        s3_group.setLayout(s3_layout)
        layout.addWidget(s3_group)
        
        # Info label
        info_label = QLabel(
            "<b>About S3 Integration:</b><br>"
            "If Duda provides S3 access for your white-label site statistics, "
            "enter the credentials here. The application will fetch and parse "
            "statistical data from the S3 bucket.<br><br>"
            "<i>Contact Duda support if you need S3 access credentials.</i>"
        )
        info_label.setWordWrap(True)
        info_label.setStyleSheet("padding: 10px; background-color: #f0f0f0; border-radius: 5px;")
        layout.addWidget(info_label)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def _create_webhooks_tab(self) -> QWidget:
        """Create webhooks configuration tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Webhooks group
        webhooks_group = QGroupBox("Webhook URLs")
        webhooks_layout = QFormLayout()
        
        self.webhook_form_input = QLineEdit()
        self.webhook_form_input.setPlaceholderText("https://your-webhook-url.com/form-submission")
        webhooks_layout.addRow("New Form Submission:", self.webhook_form_input)
        
        self.webhook_order_input = QLineEdit()
        self.webhook_order_input.setPlaceholderText("https://your-webhook-url.com/new-order")
        webhooks_layout.addRow("New eCommerce Order:", self.webhook_order_input)
        
        self.webhook_stats_input = QLineEdit()
        self.webhook_stats_input.setPlaceholderText("https://your-webhook-url.com/daily-stats")
        webhooks_layout.addRow("Daily Stats Summary:", self.webhook_stats_input)
        
        self.webhook_blog_input = QLineEdit()
        self.webhook_blog_input.setPlaceholderText("https://your-webhook-url.com/new-blog-post")
        webhooks_layout.addRow("New Blog Post:", self.webhook_blog_input)
        
        webhooks_group.setLayout(webhooks_layout)
        layout.addWidget(webhooks_group)
        
        # Info label
        info_label = QLabel(
            "<b>About Webhooks:</b><br>"
            "Webhooks allow the application to automatically send data to external services "
            "when specific events occur. Enter the URL endpoints where you want to receive "
            "notifications.<br><br>"
            "The application will send POST requests with JSON payloads containing the event data.<br><br>"
            "<i>Leave blank to disable webhooks for specific events.</i>"
        )
        info_label.setWordWrap(True)
        info_label.setStyleSheet("padding: 10px; background-color: #f0f0f0; border-radius: 5px;")
        layout.addWidget(info_label)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def _create_seo_tab(self) -> QWidget:
        """Create SEO tools configuration tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # DataForSEO credentials group
        dfs_group = QGroupBox("DataForSEO API Credentials")
        dfs_layout = QFormLayout()
        
        self.dfs_login_input = QLineEdit()
        self.dfs_login_input.setPlaceholderText("Enter your DataForSEO login/email")
        dfs_layout.addRow("Login/Email:", self.dfs_login_input)
        
        self.dfs_password_input = QLineEdit()
        self.dfs_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.dfs_password_input.setPlaceholderText("Enter your DataForSEO password")
        dfs_layout.addRow("Password:", self.dfs_password_input)
        
        dfs_group.setLayout(dfs_layout)
        layout.addWidget(dfs_group)
        
        # Google Analytics 4 group (optional)
        ga4_group = QGroupBox("Google Analytics 4 (Optional)")
        ga4_layout = QFormLayout()
        
        self.ga4_service_account_input = QLineEdit()
        self.ga4_service_account_input.setPlaceholderText("/path/to/service-account.json")
        ga4_layout.addRow("Service Account File:", self.ga4_service_account_input)
        
        ga4_group.setLayout(ga4_layout)
        layout.addWidget(ga4_group)
        
        # Google Search Console group (optional)
        gsc_group = QGroupBox("Google Search Console (Optional)")
        gsc_layout = QFormLayout()
        
        self.gsc_service_account_input = QLineEdit()
        self.gsc_service_account_input.setPlaceholderText("/path/to/service-account.json (can be same as GA4)")
        gsc_layout.addRow("Service Account File:", self.gsc_service_account_input)
        
        gsc_group.setLayout(gsc_layout)
        layout.addWidget(gsc_group)
        
        # SEO Audit webhook
        webhook_group = QGroupBox("SEO Audit Webhooks")
        webhook_layout = QFormLayout()
        
        self.webhook_audit_complete_input = QLineEdit()
        self.webhook_audit_complete_input.setPlaceholderText("https://your-webhook-url.com/audit-complete")
        webhook_layout.addRow("Audit Complete:", self.webhook_audit_complete_input)
        
        webhook_group.setLayout(webhook_layout)
        layout.addWidget(webhook_group)
        
        # Info label
        info_label = QLabel(
            "<b>SEO Tools Configuration:</b><br><br>"
            "<b>DataForSEO:</b> Required for crawls, keywords, backlinks, and competitor analysis.<br>"
            "Sign up at <a href='https://dataforseo.com'>dataforseo.com</a><br><br>"
            "<b>Google Analytics 4:</b> Optional. Provides traffic and engagement metrics.<br>"
            "Requires a service account JSON file with Analytics Data API enabled.<br><br>"
            "<b>Google Search Console:</b> Optional. Provides search query and position data.<br>"
            "Requires a service account JSON file with Search Console API enabled.<br><br>"
            "<i>Note: GA4 and GSC can use the same service account file.</i>"
        )
        info_label.setWordWrap(True)
        info_label.setOpenExternalLinks(True)
        info_label.setStyleSheet("padding: 10px; background-color: #f0f0f0; border-radius: 5px;")
        layout.addWidget(info_label)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def _create_app_settings_tab(self) -> QWidget:
        """Create application settings tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # General settings group
        settings_group = QGroupBox("General Settings")
        settings_layout = QFormLayout()
        
        self.auto_fetch_interval = QSpinBox()
        self.auto_fetch_interval.setMinimum(60)
        self.auto_fetch_interval.setMaximum(86400)
        self.auto_fetch_interval.setValue(300)
        self.auto_fetch_interval.setSuffix(" seconds")
        settings_layout.addRow("Auto-Fetch Interval:", self.auto_fetch_interval)
        
        self.enable_notifications = QCheckBox("Enable desktop notifications")
        self.enable_notifications.setChecked(True)
        settings_layout.addRow("Notifications:", self.enable_notifications)
        
        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)
        
        # Info label
        info_label = QLabel(
            "<b>Application Settings:</b><br>"
            "<b>Auto-Fetch Interval:</b> How often the application automatically checks "
            "for new data from Duda (in seconds).<br><br>"
            "<b>Notifications:</b> Show desktop notifications when new events are detected."
        )
        info_label.setWordWrap(True)
        info_label.setStyleSheet("padding: 10px; background-color: #f0f0f0; border-radius: 5px;")
        layout.addWidget(info_label)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def _load_current_settings(self):
        """Load current settings from config manager."""
        config = self.config_manager.load_config()
        
        # Duda credentials
        duda = config.get('duda', {})
        self.duda_user_input.setText(duda.get('api_user', ''))
        self.duda_password_input.setText(duda.get('api_password', ''))
        
        # S3 credentials
        s3 = config.get('s3', {})
        self.s3_access_key_input.setText(s3.get('access_key_id', ''))
        self.s3_secret_key_input.setText(s3.get('secret_access_key', ''))
        self.s3_bucket_input.setText(s3.get('bucket_name', ''))
        self.s3_region_input.setText(s3.get('region', 'us-east-1'))
        
        # Webhooks
        webhooks = config.get('webhooks', {})
        self.webhook_form_input.setText(webhooks.get('new_form_submission', ''))
        self.webhook_order_input.setText(webhooks.get('new_ecommerce_order', ''))
        self.webhook_stats_input.setText(webhooks.get('daily_stats_summary', ''))
        self.webhook_blog_input.setText(webhooks.get('new_blog_post', ''))
        
        # SEO tools
        seo = config.get('seo', {})
        self.dfs_login_input.setText(seo.get('dataforseo_login', ''))
        self.dfs_password_input.setText(seo.get('dataforseo_password', ''))
        self.ga4_service_account_input.setText(seo.get('ga4_service_account', ''))
        self.gsc_service_account_input.setText(seo.get('gsc_service_account', ''))
        self.webhook_audit_complete_input.setText(seo.get('webhook_audit_complete', ''))
        
        # App settings
        app_settings = config.get('app_settings', {})
        self.auto_fetch_interval.setValue(app_settings.get('auto_fetch_interval', 300))
        self.enable_notifications.setChecked(app_settings.get('enable_notifications', True))
    
    def _save_settings(self):
        """Save settings to config manager."""
        config = {
            'duda': {
                'api_user': self.duda_user_input.text().strip(),
                'api_password': self.duda_password_input.text().strip()
            },
            's3': {
                'access_key_id': self.s3_access_key_input.text().strip(),
                'secret_access_key': self.s3_secret_key_input.text().strip(),
                'bucket_name': self.s3_bucket_input.text().strip(),
                'region': self.s3_region_input.text().strip() or 'us-east-1'
            },
            'webhooks': {
                'new_form_submission': self.webhook_form_input.text().strip(),
                'new_ecommerce_order': self.webhook_order_input.text().strip(),
                'daily_stats_summary': self.webhook_stats_input.text().strip(),
                'new_blog_post': self.webhook_blog_input.text().strip()
            },
            'seo': {
                'dataforseo_login': self.dfs_login_input.text().strip(),
                'dataforseo_password': self.dfs_password_input.text().strip(),
                'ga4_service_account': self.ga4_service_account_input.text().strip(),
                'gsc_service_account': self.gsc_service_account_input.text().strip(),
                'webhook_audit_complete': self.webhook_audit_complete_input.text().strip()
            },
            'app_settings': {
                'auto_fetch_interval': self.auto_fetch_interval.value(),
                'enable_notifications': self.enable_notifications.isChecked(),
                'last_fetch_timestamp': self.config_manager.load_config().get('app_settings', {}).get('last_fetch_timestamp')
            }
        }
        
        if self.config_manager.save_config(config):
            QMessageBox.information(
                self,
                "Settings Saved",
                "Your settings have been saved successfully!"
            )
            self.accept()
        else:
            QMessageBox.critical(
                self,
                "Error",
                "Failed to save settings. Please try again."
            )
