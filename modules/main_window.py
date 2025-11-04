"""
Main Window Module
Main application window with tabbed interface for displaying data.
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QPushButton, QLabel, QTableWidget, QTableWidgetItem, QHeaderView,
    QMessageBox, QStatusBar, QMenuBar, QMenu, QProgressBar
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QAction
from datetime import datetime
import json


class MainWindow(QMainWindow):
    """Main application window."""
    
    # Signals
    fetch_data_requested = pyqtSignal()
    settings_requested = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SitePanda Desktop")
        self.setMinimumSize(1200, 700)
        
        self._init_ui()
        self._init_menu()
        self._init_statusbar()
    
    def _init_ui(self):
        """Initialize the user interface."""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        
        # Header with action buttons
        header = self._create_header()
        layout.addWidget(header)
        
        # Tab widget for different data views
        self.tabs = QTabWidget()
        
        # Sites tab
        self.sites_tab = self._create_sites_tab()
        self.tabs.addTab(self.sites_tab, "Sites")
        
        # Form Submissions tab
        self.forms_tab = self._create_forms_tab()
        self.tabs.addTab(self.forms_tab, "Form Submissions")
        
        # eCommerce Orders tab
        self.orders_tab = self._create_orders_tab()
        self.tabs.addTab(self.orders_tab, "eCommerce Orders")
        
        # Products tab
        self.products_tab = self._create_products_tab()
        self.tabs.addTab(self.products_tab, "Products")
        
        # Analytics tab
        self.analytics_tab = self._create_analytics_tab()
        self.tabs.addTab(self.analytics_tab, "Analytics")
        
        # SEO Audits tab
        self.seo_audits_tab = self._create_seo_audits_tab()
        self.tabs.addTab(self.seo_audits_tab, "SEO Audits")
        
        layout.addWidget(self.tabs)
        
        central_widget.setLayout(layout)
    
    def _create_header(self) -> QWidget:
        """Create header with action buttons."""
        header = QWidget()
        layout = QHBoxLayout()
        
        # Title
        title = QLabel("<h2>SitePanda Desktop</h2>")
        layout.addWidget(title)
        
        layout.addStretch()
        
        # Fetch Data button
        self.fetch_btn = QPushButton("Fetch Data")
        self.fetch_btn.clicked.connect(self.fetch_data_requested.emit)
        layout.addWidget(self.fetch_btn)
        
        # Settings button
        settings_btn = QPushButton("Settings")
        settings_btn.clicked.connect(self.settings_requested.emit)
        layout.addWidget(settings_btn)
        
        header.setLayout(layout)
        return header
    
    def _create_sites_tab(self) -> QWidget:
        """Create sites data tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Table
        self.sites_table = QTableWidget()
        self.sites_table.setColumnCount(7)
        self.sites_table.setHorizontalHeaderLabels([
            "Site Name", "Title", "Domain", "Published", "Store", "Blog", "Last Updated"
        ])
        self.sites_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.sites_table.setAlternatingRowColors(True)
        self.sites_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        layout.addWidget(self.sites_table)
        
        widget.setLayout(layout)
        return widget
    
    def _create_forms_tab(self) -> QWidget:
        """Create form submissions tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Table
        self.forms_table = QTableWidget()
        self.forms_table.setColumnCount(6)
        self.forms_table.setHorizontalHeaderLabels([
            "Site", "Form Title", "Submission Date", "Name", "Email", "Webhook Sent"
        ])
        self.forms_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.forms_table.setAlternatingRowColors(True)
        self.forms_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.forms_table.doubleClicked.connect(self._on_form_double_click)
        
        layout.addWidget(self.forms_table)
        
        widget.setLayout(layout)
        return widget
    
    def _create_orders_tab(self) -> QWidget:
        """Create eCommerce orders tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Table
        self.orders_table = QTableWidget()
        self.orders_table.setColumnCount(7)
        self.orders_table.setHorizontalHeaderLabels([
            "Site", "Order #", "Date", "Customer", "Email", "Total", "Status"
        ])
        self.orders_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.orders_table.setAlternatingRowColors(True)
        self.orders_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.orders_table.doubleClicked.connect(self._on_order_double_click)
        
        layout.addWidget(self.orders_table)
        
        widget.setLayout(layout)
        return widget
    
    def _create_products_tab(self) -> QWidget:
        """Create products tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Table
        self.products_table = QTableWidget()
        self.products_table.setColumnCount(6)
        self.products_table.setHorizontalHeaderLabels([
            "Site", "Product Name", "SKU", "Price", "Stock", "Active"
        ])
        self.products_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.products_table.setAlternatingRowColors(True)
        self.products_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        layout.addWidget(self.products_table)
        
        widget.setLayout(layout)
        return widget
    
    def _create_analytics_tab(self) -> QWidget:
        """Create analytics/stats tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        
        info_label = QLabel(
            "<h3>Analytics Dashboard</h3>"
            "<p>Site statistics and analytics data will be displayed here.</p>"
            "<p>This includes visitor numbers, page views, traffic sources, and more.</p>"
        )
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def _create_seo_audits_tab(self) -> QWidget:
        """Create SEO audits tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Header with Run Audit button
        header = QWidget()
        header_layout = QHBoxLayout()
        
        header_label = QLabel("<h3>SEO Audits</h3>")
        header_layout.addWidget(header_label)
        header_layout.addStretch()
        
        self.run_audit_btn = QPushButton("Run New Audit")
        self.run_audit_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        header_layout.addWidget(self.run_audit_btn)
        
        header.setLayout(header_layout)
        layout.addWidget(header)
        
        # Audits table
        self.audits_table = QTableWidget()
        self.audits_table.setColumnCount(6)
        self.audits_table.setHorizontalHeaderLabels([
            "Domain", "Status", "Started", "Completed", "Duration", "Actions"
        ])
        self.audits_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.audits_table.setAlternatingRowColors(True)
        self.audits_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.audits_table.doubleClicked.connect(self._on_audit_double_click)
        
        layout.addWidget(self.audits_table)
        
        widget.setLayout(layout)
        return widget
    
    def _on_audit_double_click(self, index):
        """Handle double-click on audit row."""
        row = index.row()
        item = self.audits_table.item(row, 0)
        if item:
            audit_data = item.data(Qt.ItemDataRole.UserRole)
            if audit_data:
                self._show_audit_details(audit_data)
    
    def _show_audit_details(self, audit_data: dict):
        """Show audit details dialog."""
        domain = audit_data.get('domain', 'Unknown')
        status = audit_data.get('status', 'unknown')
        
        insights_str = audit_data.get('insights', '{}')
        try:
            insights = json.loads(insights_str) if isinstance(insights_str, str) else insights_str
        except:
            insights = {}
        
        summary = insights.get('summary', {})
        
        # Build details message
        details = f"<h2>SEO Audit: {domain}</h2>"
        details += f"<p><b>Status:</b> {status}</p>"
        details += f"<p><b>Started:</b> {audit_data.get('started_at', 'N/A')}</p>"
        details += f"<p><b>Completed:</b> {audit_data.get('completed_at', 'N/A')}</p>"
        
        if summary:
            details += "<h3>Summary:</h3><ul>"
            for key, value in summary.items():
                details += f"<li><b>{key}:</b> {value}</li>"
            details += "</ul>"
        
        msg = QMessageBox(self)
        msg.setWindowTitle(f"Audit Details - {domain}")
        msg.setText(details)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()
    
    def update_audits_table(self, audits: list):
        """Update SEO audits table with data."""
        self.audits_table.setRowCount(len(audits))
        
        for row, audit in enumerate(audits):
            # Domain
            domain_item = QTableWidgetItem(audit.get('domain', ''))
            domain_item.setData(Qt.ItemDataRole.UserRole, audit)
            self.audits_table.setItem(row, 0, domain_item)
            
            # Status
            status = audit.get('status', 'unknown')
            status_item = QTableWidgetItem(status.upper())
            if status == 'completed':
                status_item.setForeground(Qt.GlobalColor.darkGreen)
            elif status == 'failed':
                status_item.setForeground(Qt.GlobalColor.red)
            elif status == 'running':
                status_item.setForeground(Qt.GlobalColor.blue)
            self.audits_table.setItem(row, 1, status_item)
            
            # Started
            self.audits_table.setItem(row, 2, QTableWidgetItem(audit.get('started_at', '')))
            
            # Completed
            self.audits_table.setItem(row, 3, QTableWidgetItem(audit.get('completed_at', '') or 'In Progress'))
            
            # Duration (calculate if completed)
            duration = ""
            if audit.get('started_at') and audit.get('completed_at'):
                try:
                    from datetime import datetime
                    start = datetime.fromisoformat(audit['started_at'])
                    end = datetime.fromisoformat(audit['completed_at'])
                    delta = end - start
                    duration = str(delta).split('.')[0]  # Remove microseconds
                except:
                    pass
            self.audits_table.setItem(row, 4, QTableWidgetItem(duration))
            
            # Actions (placeholder for now)
            self.audits_table.setItem(row, 5, QTableWidgetItem("View Report"))
    
    def _init_menu(self):
        """Initialize menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.settings_requested.emit)
        file_menu.addAction(settings_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Data menu
        data_menu = menubar.addMenu("Data")
        
        fetch_action = QAction("Fetch All Data", self)
        fetch_action.triggered.connect(self.fetch_data_requested.emit)
        data_menu.addAction(fetch_action)
        
        refresh_action = QAction("Refresh Display", self)
        refresh_action.triggered.connect(self.refresh_display_requested)
        data_menu.addAction(refresh_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
    
    def _init_statusbar(self):
        """Initialize status bar."""
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setMaximumWidth(200)
        self.statusbar.addPermanentWidget(self.progress_bar)
        
        self.set_status("Ready")
    
    def set_status(self, message: str):
        """Set status bar message."""
        self.statusbar.showMessage(message)
    
    def show_progress(self, visible: bool = True):
        """Show or hide progress bar."""
        self.progress_bar.setVisible(visible)
        if visible:
            self.progress_bar.setRange(0, 0)  # Indeterminate progress
    
    def update_sites_table(self, sites: list):
        """Update sites table with data."""
        self.sites_table.setRowCount(len(sites))
        
        for row, site in enumerate(sites):
            self.sites_table.setItem(row, 0, QTableWidgetItem(site.get('site_name', '')))
            self.sites_table.setItem(row, 1, QTableWidgetItem(site.get('site_title', '')))
            self.sites_table.setItem(row, 2, QTableWidgetItem(site.get('site_domain', '')))
            self.sites_table.setItem(row, 3, QTableWidgetItem('Yes' if site.get('is_published') else 'No'))
            self.sites_table.setItem(row, 4, QTableWidgetItem('Yes' if site.get('store_enabled') else 'No'))
            self.sites_table.setItem(row, 5, QTableWidgetItem('Yes' if site.get('blog_enabled') else 'No'))
            self.sites_table.setItem(row, 6, QTableWidgetItem(site.get('last_updated', '')))
    
    def update_forms_table(self, submissions: list):
        """Update form submissions table with data."""
        self.forms_table.setRowCount(len(submissions))
        
        for row, submission in enumerate(submissions):
            self.forms_table.setItem(row, 0, QTableWidgetItem(submission.get('site_name', '')))
            self.forms_table.setItem(row, 1, QTableWidgetItem(submission.get('form_title', '')))
            self.forms_table.setItem(row, 2, QTableWidgetItem(submission.get('submission_date', '')))
            self.forms_table.setItem(row, 3, QTableWidgetItem(submission.get('submitter_name', '')))
            self.forms_table.setItem(row, 4, QTableWidgetItem(submission.get('submitter_email', '')))
            self.forms_table.setItem(row, 5, QTableWidgetItem('Yes' if submission.get('webhook_sent') else 'No'))
            
            # Store full data in first cell
            item = self.forms_table.item(row, 0)
            item.setData(Qt.ItemDataRole.UserRole, submission)
    
    def update_orders_table(self, orders: list):
        """Update eCommerce orders table with data."""
        self.orders_table.setRowCount(len(orders))
        
        for row, order in enumerate(orders):
            self.orders_table.setItem(row, 0, QTableWidgetItem(order.get('site_name', '')))
            self.orders_table.setItem(row, 1, QTableWidgetItem(order.get('order_number', '')))
            self.orders_table.setItem(row, 2, QTableWidgetItem(order.get('order_date', '')))
            self.orders_table.setItem(row, 3, QTableWidgetItem(order.get('customer_name', '')))
            self.orders_table.setItem(row, 4, QTableWidgetItem(order.get('customer_email', '')))
            
            amount = order.get('total_amount', 0)
            currency = order.get('currency', 'USD')
            self.orders_table.setItem(row, 5, QTableWidgetItem(f"{currency} {amount:.2f}" if amount else ''))
            
            self.orders_table.setItem(row, 6, QTableWidgetItem(order.get('status', '')))
            
            # Store full data in first cell
            item = self.orders_table.item(row, 0)
            item.setData(Qt.ItemDataRole.UserRole, order)
    
    def update_products_table(self, products: list):
        """Update products table with data."""
        self.products_table.setRowCount(len(products))
        
        for row, product in enumerate(products):
            self.products_table.setItem(row, 0, QTableWidgetItem(product.get('site_name', '')))
            self.products_table.setItem(row, 1, QTableWidgetItem(product.get('product_name', '')))
            self.products_table.setItem(row, 2, QTableWidgetItem(product.get('sku', '')))
            
            price = product.get('price', 0)
            currency = product.get('currency', 'USD')
            self.products_table.setItem(row, 3, QTableWidgetItem(f"{currency} {price:.2f}" if price else ''))
            
            stock = product.get('stock_quantity', 0)
            self.products_table.setItem(row, 4, QTableWidgetItem(str(stock) if stock is not None else ''))
            
            self.products_table.setItem(row, 5, QTableWidgetItem('Yes' if product.get('is_active') else 'No'))
    
    def _on_form_double_click(self, index):
        """Handle double-click on form submission."""
        row = index.row()
        item = self.forms_table.item(row, 0)
        submission = item.data(Qt.ItemDataRole.UserRole)
        
        if submission:
            # Show form data in a dialog
            form_data = submission.get('form_data', {})
            if isinstance(form_data, str):
                try:
                    form_data = json.loads(form_data)
                except:
                    pass
            
            details = f"<h3>Form Submission Details</h3>"
            details += f"<p><b>Site:</b> {submission.get('site_name', '')}</p>"
            details += f"<p><b>Form:</b> {submission.get('form_title', '')}</p>"
            details += f"<p><b>Date:</b> {submission.get('submission_date', '')}</p>"
            details += f"<p><b>Name:</b> {submission.get('submitter_name', '')}</p>"
            details += f"<p><b>Email:</b> {submission.get('submitter_email', '')}</p>"
            details += "<p><b>Form Data:</b></p><pre>"
            details += json.dumps(form_data, indent=2)
            details += "</pre>"
            
            msg = QMessageBox(self)
            msg.setWindowTitle("Form Submission Details")
            msg.setTextFormat(Qt.TextFormat.RichText)
            msg.setText(details)
            msg.exec()
    
    def _on_order_double_click(self, index):
        """Handle double-click on order."""
        row = index.row()
        item = self.orders_table.item(row, 0)
        order = item.data(Qt.ItemDataRole.UserRole)
        
        if order:
            # Show order details in a dialog
            items = order.get('items', [])
            if isinstance(items, str):
                try:
                    items = json.loads(items)
                except:
                    pass
            
            details = f"<h3>Order Details</h3>"
            details += f"<p><b>Site:</b> {order.get('site_name', '')}</p>"
            details += f"<p><b>Order #:</b> {order.get('order_number', '')}</p>"
            details += f"<p><b>Date:</b> {order.get('order_date', '')}</p>"
            details += f"<p><b>Customer:</b> {order.get('customer_name', '')}</p>"
            details += f"<p><b>Email:</b> {order.get('customer_email', '')}</p>"
            details += f"<p><b>Total:</b> {order.get('currency', 'USD')} {order.get('total_amount', 0):.2f}</p>"
            details += f"<p><b>Status:</b> {order.get('status', '')}</p>"
            details += "<p><b>Items:</b></p><pre>"
            details += json.dumps(items, indent=2)
            details += "</pre>"
            
            msg = QMessageBox(self)
            msg.setWindowTitle("Order Details")
            msg.setTextFormat(Qt.TextFormat.RichText)
            msg.setText(details)
            msg.exec()
    
    def refresh_display_requested(self):
        """Signal that display refresh is requested."""
        # This will be connected to the controller
        pass
    
    def _show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self,
            "About SitePanda Desktop",
            "<h3>SitePanda Desktop</h3>"
            "<p>Version 1.0</p>"
            "<p>A desktop application for managing Duda sites, fetching data, "
            "and sending webhooks.</p>"
            "<p><b>Features:</b></p>"
            "<ul>"
            "<li>Fetch site data from Duda API</li>"
            "<li>Pull statistics from S3</li>"
            "<li>View form submissions and eCommerce orders</li>"
            "<li>Send data to webhooks</li>"
            "</ul>"
        )
