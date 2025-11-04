"""
Logger Module
Provides comprehensive logging for all application operations, errors, and events.
"""

import logging
import os
from pathlib import Path
from datetime import datetime
from logging.handlers import RotatingFileHandler


class AppLogger:
    """Application-wide logger with file and console output."""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        """Singleton pattern to ensure only one logger instance."""
        if cls._instance is None:
            cls._instance = super(AppLogger, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize logger (only once)."""
        if not AppLogger._initialized:
            self._setup_logger()
            AppLogger._initialized = True
    
    def _setup_logger(self):
        """Set up logging configuration."""
        # Create logs directory on D: drive (avoids Windows user profile permission issues)
        log_dir = Path(r'D:\sitepanda-data\logs')
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Log file paths
        self.log_file = log_dir / "sitepanda.log"
        self.error_log_file = log_dir / "sitepanda_errors.log"
        
        # Create main logger
        self.logger = logging.getLogger("SitePanda")
        self.logger.setLevel(logging.DEBUG)
        
        # Clear any existing handlers
        self.logger.handlers.clear()
        
        # File handler - all logs (with rotation)
        file_handler = RotatingFileHandler(
            self.log_file,
            maxBytes=10*1024*1024,  # 10 MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
        
        # Error file handler - errors only (with rotation)
        error_handler = RotatingFileHandler(
            self.error_log_file,
            maxBytes=10*1024*1024,  # 10 MB
            backupCount=5,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(file_formatter)
        self.logger.addHandler(error_handler)
        
        # Console handler - info and above
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # Log startup
        self.logger.info("=" * 80)
        self.logger.info("SitePanda Desktop - Logging Started")
        self.logger.info(f"Log file: {self.log_file}")
        self.logger.info(f"Error log file: {self.error_log_file}")
        self.logger.info("=" * 80)
    
    def debug(self, message: str):
        """Log debug message."""
        self.logger.debug(message)
    
    def info(self, message: str):
        """Log info message."""
        self.logger.info(message)
    
    def warning(self, message: str):
        """Log warning message."""
        self.logger.warning(message)
    
    def error(self, message: str, exc_info: bool = False):
        """
        Log error message.
        
        Args:
            message: Error message
            exc_info: Include exception traceback
        """
        self.logger.error(message, exc_info=exc_info)
    
    def critical(self, message: str, exc_info: bool = False):
        """
        Log critical message.
        
        Args:
            message: Critical message
            exc_info: Include exception traceback
        """
        self.logger.critical(message, exc_info=exc_info)
    
    def exception(self, message: str):
        """
        Log exception with full traceback.
        
        Args:
            message: Exception message
        """
        self.logger.exception(message)
    
    def log_operation(self, operation: str, status: str, details: str = ""):
        """
        Log an operation with status.
        
        Args:
            operation: Operation name (e.g., "Fetch Duda Sites")
            status: Status (e.g., "SUCCESS", "FAILED", "STARTED")
            details: Additional details
        """
        message = f"[{operation}] {status}"
        if details:
            message += f" - {details}"
        
        if status in ["SUCCESS", "COMPLETED"]:
            self.info(message)
        elif status in ["FAILED", "ERROR"]:
            self.error(message)
        elif status in ["STARTED", "RUNNING"]:
            self.info(message)
        else:
            self.debug(message)
    
    def log_api_call(self, api: str, endpoint: str, status_code: int = None, error: str = None):
        """
        Log API call.
        
        Args:
            api: API name (e.g., "Duda", "DataForSEO")
            endpoint: API endpoint
            status_code: HTTP status code
            error: Error message if failed
        """
        if error:
            self.error(f"[{api} API] {endpoint} - FAILED - {error}")
        elif status_code:
            if 200 <= status_code < 300:
                self.info(f"[{api} API] {endpoint} - SUCCESS - Status {status_code}")
            else:
                self.warning(f"[{api} API] {endpoint} - Status {status_code}")
        else:
            self.debug(f"[{api} API] {endpoint}")
    
    def log_webhook(self, event: str, url: str, status: str, response_code: int = None):
        """
        Log webhook notification.
        
        Args:
            event: Event type
            url: Webhook URL
            status: Status (SUCCESS/FAILED)
            response_code: HTTP response code
        """
        message = f"[Webhook] {event} -> {url} - {status}"
        if response_code:
            message += f" (HTTP {response_code})"
        
        if status == "SUCCESS":
            self.info(message)
        else:
            self.error(message)
    
    def log_audit(self, domain: str, status: str, details: str = ""):
        """
        Log SEO audit operation.
        
        Args:
            domain: Domain being audited
            status: Audit status
            details: Additional details
        """
        self.log_operation(f"SEO Audit: {domain}", status, details)
    
    def log_database(self, operation: str, table: str, status: str, details: str = ""):
        """
        Log database operation.
        
        Args:
            operation: Operation type (INSERT, UPDATE, SELECT, etc.)
            table: Table name
            status: Status
            details: Additional details
        """
        message = f"[Database] {operation} on {table} - {status}"
        if details:
            message += f" - {details}"
        
        if status == "SUCCESS":
            self.debug(message)
        else:
            self.error(message)
    
    def get_log_file_path(self) -> str:
        """Get path to main log file."""
        return str(self.log_file)
    
    def get_error_log_file_path(self) -> str:
        """Get path to error log file."""
        return str(self.error_log_file)
    
    def get_recent_logs(self, lines: int = 100) -> list:
        """
        Get recent log entries.
        
        Args:
            lines: Number of lines to retrieve
            
        Returns:
            List of log lines
        """
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                all_lines = f.readlines()
                return all_lines[-lines:]
        except Exception as e:
            return [f"Error reading log file: {e}"]
    
    def get_recent_errors(self, lines: int = 50) -> list:
        """
        Get recent error log entries.
        
        Args:
            lines: Number of lines to retrieve
            
        Returns:
            List of error log lines
        """
        try:
            if not self.error_log_file.exists():
                return ["No errors logged yet."]
            
            with open(self.error_log_file, 'r', encoding='utf-8') as f:
                all_lines = f.readlines()
                return all_lines[-lines:]
        except Exception as e:
            return [f"Error reading error log file: {e}"]
    
    def clear_logs(self):
        """Clear all log files."""
        try:
            # Truncate main log
            with open(self.log_file, 'w', encoding='utf-8') as f:
                f.write("")
            
            # Truncate error log
            with open(self.error_log_file, 'w', encoding='utf-8') as f:
                f.write("")
            
            self.info("Log files cleared")
            return True
        except Exception as e:
            self.error(f"Failed to clear log files: {e}")
            return False


# Global logger instance
logger = AppLogger()


# Convenience functions
def debug(message: str):
    """Log debug message."""
    logger.debug(message)


def info(message: str):
    """Log info message."""
    logger.info(message)


def warning(message: str):
    """Log warning message."""
    logger.warning(message)


def error(message: str, exc_info: bool = False):
    """Log error message."""
    logger.error(message, exc_info=exc_info)


def critical(message: str, exc_info: bool = False):
    """Log critical message."""
    logger.critical(message, exc_info=exc_info)


def exception(message: str):
    """Log exception with traceback."""
    logger.exception(message)


def log_operation(operation: str, status: str, details: str = ""):
    """Log an operation."""
    logger.log_operation(operation, status, details)


def log_api_call(api: str, endpoint: str, status_code: int = None, error: str = None):
    """Log API call."""
    logger.log_api_call(api, endpoint, status_code, error)


def log_webhook(event: str, url: str, status: str, response_code: int = None):
    """Log webhook notification."""
    logger.log_webhook(event, url, status, response_code)


def log_audit(domain: str, status: str, details: str = ""):
    """Log SEO audit."""
    logger.log_audit(domain, status, details)


def log_database(operation: str, table: str, status: str, details: str = ""):
    """Log database operation."""
    logger.log_database(operation, table, status, details)
