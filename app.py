#!/usr/bin/env python3
"""
SitePanda Desktop
Main application entry point.
"""

import sys
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QThread, pyqtSignal
from modules.config_manager import ConfigManager
from modules.database import DatabaseManager
from modules.duda_client import DudaAPIClient
from modules.s3_client import S3Client
from modules.data_fetcher import DataFetcher
from modules.webhook_manager import WebhookManager
from modules.main_window import MainWindow
from modules.settings_dialog import SettingsDialog


class DataFetchThread(QThread):
    """Background thread for fetching data."""
    
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, data_fetcher):
        super().__init__()
        self.data_fetcher = data_fetcher
    
    def run(self):
        """Run data fetching in background."""
        try:
            stats = self.data_fetcher.fetch_all_data()
            self.finished.emit(stats)
        except Exception as e:
            self.error.emit(str(e))


class WebhookThread(QThread):
    """Background thread for processing webhooks."""
    
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, webhook_manager):
        super().__init__()
        self.webhook_manager = webhook_manager
    
    def run(self):
        """Process webhooks in background."""
        try:
            result = self.webhook_manager.process_all_pending_webhooks()
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class SitePandaApp:
    """Main application controller."""
    
    def __init__(self):
        """Initialize the application."""
        # Initialize components
        self.config_manager = ConfigManager()
        self.db_manager = DatabaseManager()
        
        # Initialize clients (will be None if not configured)
        self.duda_client = None
        self.s3_client = None
        self.data_fetcher = None
        self.webhook_manager = None
        
        # Initialize UI
        self.window = MainWindow()
        
        # Connect signals
        self.window.fetch_data_requested.connect(self.fetch_data)
        self.window.settings_requested.connect(self.show_settings)
        
        # Initialize clients if credentials are available
        self._initialize_clients()
        
        # Load initial data
        self.refresh_display()
    
    def _initialize_clients(self):
        """Initialize API clients with saved credentials."""
        # Duda API client
        if self.config_manager.validate_duda_credentials():
            user, password = self.config_manager.get_duda_credentials()
            self.duda_client = DudaAPIClient(user, password)
            
            # Test connection
            if self.duda_client.test_connection():
                self.window.set_status("Connected to Duda API")
            else:
                self.window.set_status("Duda API credentials invalid")
                self.duda_client = None
        
        # S3 client
        if self.config_manager.validate_s3_credentials():
            s3_config = self.config_manager.get_s3_credentials()
            self.s3_client = S3Client(
                s3_config['access_key_id'],
                s3_config['secret_access_key'],
                s3_config['bucket_name'],
                s3_config.get('region', 'us-east-1')
            )
            
            # Test connection
            if not self.s3_client.test_connection():
                self.window.set_status("S3 credentials invalid")
                self.s3_client = None
        
        # Data fetcher
        if self.duda_client:
            self.data_fetcher = DataFetcher(self.duda_client, self.db_manager)
        
        # Webhook manager
        webhooks = self.config_manager.get_webhooks()
        self.webhook_manager = WebhookManager(self.db_manager, webhooks)
    
    def show_settings(self):
        """Show settings dialog."""
        dialog = SettingsDialog(self.config_manager, self.window)
        
        if dialog.exec():
            # Settings were saved, reinitialize clients
            self._initialize_clients()
            QMessageBox.information(
                self.window,
                "Settings Applied",
                "Settings have been applied. Credentials will be used for the next data fetch."
            )
    
    def fetch_data(self):
        """Fetch data from Duda API."""
        if not self.duda_client:
            QMessageBox.warning(
                self.window,
                "Not Configured",
                "Please configure your Duda API credentials in Settings first."
            )
            self.show_settings()
            return
        
        # Show progress
        self.window.set_status("Fetching data from Duda...")
        self.window.show_progress(True)
        self.window.fetch_btn.setEnabled(False)
        
        # Create and start fetch thread
        self.fetch_thread = DataFetchThread(self.data_fetcher)
        self.fetch_thread.finished.connect(self._on_fetch_finished)
        self.fetch_thread.error.connect(self._on_fetch_error)
        self.fetch_thread.start()
    
    def _on_fetch_finished(self, stats):
        """Handle data fetch completion."""
        self.window.show_progress(False)
        self.window.fetch_btn.setEnabled(True)
        
        # Show summary
        message = f"Data fetch completed!\n\n"
        message += f"Sites: {stats.get('sites', 0)}\n"
        message += f"Form Submissions: {stats.get('form_submissions', 0)}\n"
        message += f"Products: {stats.get('products', 0)}\n"
        message += f"Orders: {stats.get('orders', 0)}"
        
        self.window.set_status("Data fetch completed")
        
        QMessageBox.information(
            self.window,
            "Fetch Complete",
            message
        )
        
        # Refresh display
        self.refresh_display()
        
        # Process webhooks for new data
        if self.webhook_manager:
            self._process_webhooks()
    
    def _on_fetch_error(self, error_msg):
        """Handle data fetch error."""
        self.window.show_progress(False)
        self.window.fetch_btn.setEnabled(True)
        self.window.set_status("Error fetching data")
        
        QMessageBox.critical(
            self.window,
            "Fetch Error",
            f"An error occurred while fetching data:\n\n{error_msg}"
        )
    
    def _process_webhooks(self):
        """Process pending webhooks in background."""
        if not self.webhook_manager:
            return
        
        self.window.set_status("Processing webhooks...")
        
        # Create and start webhook thread
        self.webhook_thread = WebhookThread(self.webhook_manager)
        self.webhook_thread.finished.connect(self._on_webhooks_finished)
        self.webhook_thread.error.connect(self._on_webhooks_error)
        self.webhook_thread.start()
    
    def _on_webhooks_finished(self, result):
        """Handle webhook processing completion."""
        total = result.get('form_submissions', 0) + result.get('orders', 0)
        
        if total > 0:
            self.window.set_status(f"Sent {total} webhooks")
        else:
            self.window.set_status("No new webhooks to send")
        
        # Refresh display to update webhook_sent status
        self.refresh_display()
    
    def _on_webhooks_error(self, error_msg):
        """Handle webhook processing error."""
        self.window.set_status("Error processing webhooks")
        print(f"Webhook error: {error_msg}")
    
    def refresh_display(self):
        """Refresh all data displays."""
        # Load data from database
        sites = self.db_manager.get_all_sites()
        submissions = self.db_manager.get_form_submissions()
        orders = self.db_manager.get_ecommerce_orders()
        
        # Get all products
        try:
            conn = self.db_manager._get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM ecommerce_products ORDER BY last_updated DESC')
            products = [dict(row) for row in cursor.fetchall()]
        except:
            products = []
        
        # Update tables
        self.window.update_sites_table(sites)
        self.window.update_forms_table(submissions)
        self.window.update_orders_table(orders)
        self.window.update_products_table(products)
        
        # Update status
        self.window.set_status(f"Displaying {len(sites)} sites, {len(submissions)} submissions, {len(orders)} orders")
    
    def run(self):
        """Run the application."""
        self.window.show()
        
        # Check if credentials are configured
        if not self.config_manager.validate_duda_credentials():
            QMessageBox.information(
                self.window,
                "Welcome to SitePanda Desktop",
                "Welcome! Please configure your API credentials to get started.\n\n"
                "You'll need:\n"
                "• Duda API Username and Password\n"
                "• (Optional) AWS S3 credentials for site statistics\n"
                "• (Optional) Webhook URLs for event notifications"
            )
            self.show_settings()
        
        return self.window


def main():
    """Main entry point."""
    app = QApplication(sys.argv)
    
    # Set application metadata
    app.setApplicationName("SitePanda Desktop")
    app.setOrganizationName("SitePanda")
    
    # Create and run application
    manager = SitePandaApp()
    manager.run()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
