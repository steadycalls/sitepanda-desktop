"""
Database Manager Module
Handles SQLite database operations for storing Duda site data.
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional, Any
from pathlib import Path


class DatabaseManager:
    """Manages SQLite database for storing Duda site data."""
    
    def __init__(self, db_path: str = None):
        """
        Initialize the database manager.
        
        Args:
            db_path: Path to SQLite database file
        """
        if db_path is None:
            db_path = str(Path(__file__).parent.parent / 'data' / 'duda_data.db')
        
        self.db_path = db_path
        self.conn = None
        self._initialize_database()
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get or create database connection."""
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
        return self.conn
    
    def _initialize_database(self):
        """Create database tables if they don't exist."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Sites table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sites (
                site_name TEXT PRIMARY KEY,
                site_title TEXT,
                template_id TEXT,
                site_domain TEXT,
                is_published INTEGER,
                created_date TEXT,
                last_published_date TEXT,
                store_enabled INTEGER,
                blog_enabled INTEGER,
                metadata TEXT,
                last_updated TEXT
            )
        ''')
        
        # Analytics/Stats table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS site_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                site_name TEXT,
                stat_date TEXT,
                visitors INTEGER,
                page_views INTEGER,
                unique_visitors INTEGER,
                bounce_rate REAL,
                avg_time_on_site REAL,
                traffic_sources TEXT,
                device_breakdown TEXT,
                geo_data TEXT,
                last_updated TEXT,
                FOREIGN KEY (site_name) REFERENCES sites(site_name)
            )
        ''')
        
        # Form submissions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS form_submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                site_name TEXT,
                form_id TEXT,
                form_title TEXT,
                submission_date TEXT,
                form_data TEXT,
                submitter_email TEXT,
                submitter_name TEXT,
                is_processed INTEGER DEFAULT 0,
                webhook_sent INTEGER DEFAULT 0,
                last_updated TEXT,
                FOREIGN KEY (site_name) REFERENCES sites(site_name)
            )
        ''')
        
        # eCommerce orders table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ecommerce_orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                site_name TEXT,
                order_id TEXT UNIQUE,
                order_number TEXT,
                order_date TEXT,
                customer_name TEXT,
                customer_email TEXT,
                total_amount REAL,
                currency TEXT,
                status TEXT,
                items TEXT,
                shipping_address TEXT,
                billing_address TEXT,
                is_processed INTEGER DEFAULT 0,
                webhook_sent INTEGER DEFAULT 0,
                last_updated TEXT,
                FOREIGN KEY (site_name) REFERENCES sites(site_name)
            )
        ''')
        
        # eCommerce products table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ecommerce_products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                site_name TEXT,
                product_id TEXT,
                product_name TEXT,
                description TEXT,
                price REAL,
                currency TEXT,
                sku TEXT,
                stock_quantity INTEGER,
                category TEXT,
                images TEXT,
                is_active INTEGER,
                last_updated TEXT,
                FOREIGN KEY (site_name) REFERENCES sites(site_name),
                UNIQUE(site_name, product_id)
            )
        ''')
        
        # Content collections table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS content_collections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                site_name TEXT,
                collection_name TEXT,
                collection_data TEXT,
                row_count INTEGER,
                last_updated TEXT,
                FOREIGN KEY (site_name) REFERENCES sites(site_name),
                UNIQUE(site_name, collection_name)
            )
        ''')
        
        # Blog posts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS blog_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                site_name TEXT,
                post_id TEXT,
                title TEXT,
                author TEXT,
                publish_date TEXT,
                content TEXT,
                excerpt TEXT,
                tags TEXT,
                is_published INTEGER,
                post_url TEXT,
                last_updated TEXT,
                FOREIGN KEY (site_name) REFERENCES sites(site_name),
                UNIQUE(site_name, post_id)
            )
        ''')
        
        # Webhook log table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS webhook_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT,
                webhook_url TEXT,
                payload TEXT,
                response_code INTEGER,
                response_body TEXT,
                success INTEGER,
                timestamp TEXT
            )
        ''')
        
        conn.commit()
    
    def insert_site(self, site_data: Dict) -> bool:
        """Insert or update site information."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO sites 
                (site_name, site_title, template_id, site_domain, is_published, 
                 created_date, last_published_date, store_enabled, blog_enabled, 
                 metadata, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                site_data.get('site_name'),
                site_data.get('site_title'),
                site_data.get('template_id'),
                site_data.get('site_domain'),
                site_data.get('is_published', 0),
                site_data.get('created_date'),
                site_data.get('last_published_date'),
                site_data.get('store_enabled', 0),
                site_data.get('blog_enabled', 0),
                json.dumps(site_data.get('metadata', {})),
                datetime.now().isoformat()
            ))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error inserting site: {e}")
            return False
    
    def insert_form_submission(self, submission_data: Dict) -> bool:
        """Insert form submission data."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO form_submissions 
                (site_name, form_id, form_title, submission_date, form_data, 
                 submitter_email, submitter_name, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                submission_data.get('site_name'),
                submission_data.get('form_id'),
                submission_data.get('form_title'),
                submission_data.get('submission_date'),
                json.dumps(submission_data.get('form_data', {})),
                submission_data.get('submitter_email'),
                submission_data.get('submitter_name'),
                datetime.now().isoformat()
            ))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error inserting form submission: {e}")
            return False
    
    def insert_ecommerce_order(self, order_data: Dict) -> bool:
        """Insert eCommerce order data."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO ecommerce_orders 
                (site_name, order_id, order_number, order_date, customer_name, 
                 customer_email, total_amount, currency, status, items, 
                 shipping_address, billing_address, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                order_data.get('site_name'),
                order_data.get('order_id'),
                order_data.get('order_number'),
                order_data.get('order_date'),
                order_data.get('customer_name'),
                order_data.get('customer_email'),
                order_data.get('total_amount'),
                order_data.get('currency'),
                order_data.get('status'),
                json.dumps(order_data.get('items', [])),
                json.dumps(order_data.get('shipping_address', {})),
                json.dumps(order_data.get('billing_address', {})),
                datetime.now().isoformat()
            ))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error inserting eCommerce order: {e}")
            return False
    
    def insert_product(self, product_data: Dict) -> bool:
        """Insert or update product data."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO ecommerce_products 
                (site_name, product_id, product_name, description, price, currency, 
                 sku, stock_quantity, category, images, is_active, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                product_data.get('site_name'),
                product_data.get('product_id'),
                product_data.get('product_name'),
                product_data.get('description'),
                product_data.get('price'),
                product_data.get('currency'),
                product_data.get('sku'),
                product_data.get('stock_quantity'),
                product_data.get('category'),
                json.dumps(product_data.get('images', [])),
                product_data.get('is_active', 1),
                datetime.now().isoformat()
            ))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error inserting product: {e}")
            return False
    
    def get_all_sites(self) -> List[Dict]:
        """Retrieve all sites from database."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM sites ORDER BY last_updated DESC')
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            print(f"Error retrieving sites: {e}")
            return []
    
    def get_form_submissions(self, site_name: str = None, unprocessed_only: bool = False) -> List[Dict]:
        """Retrieve form submissions."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            query = 'SELECT * FROM form_submissions WHERE 1=1'
            params = []
            
            if site_name:
                query += ' AND site_name = ?'
                params.append(site_name)
            
            if unprocessed_only:
                query += ' AND webhook_sent = 0'
            
            query += ' ORDER BY submission_date DESC'
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            print(f"Error retrieving form submissions: {e}")
            return []
    
    def get_ecommerce_orders(self, site_name: str = None, unprocessed_only: bool = False) -> List[Dict]:
        """Retrieve eCommerce orders."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            query = 'SELECT * FROM ecommerce_orders WHERE 1=1'
            params = []
            
            if site_name:
                query += ' AND site_name = ?'
                params.append(site_name)
            
            if unprocessed_only:
                query += ' AND webhook_sent = 0'
            
            query += ' ORDER BY order_date DESC'
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            print(f"Error retrieving orders: {e}")
            return []
    
    def mark_webhook_sent(self, table: str, record_id: int) -> bool:
        """Mark a record as having sent webhook."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(f'UPDATE {table} SET webhook_sent = 1 WHERE id = ?', (record_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error marking webhook sent: {e}")
            return False
    
    def log_webhook(self, event_type: str, webhook_url: str, payload: Dict, 
                    response_code: int, response_body: str, success: bool) -> bool:
        """Log webhook activity."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO webhook_log 
                (event_type, webhook_url, payload, response_code, response_body, success, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                event_type,
                webhook_url,
                json.dumps(payload),
                response_code,
                response_body,
                1 if success else 0,
                datetime.now().isoformat()
            ))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error logging webhook: {e}")
            return False
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None
