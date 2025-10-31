#!/usr/bin/env python3
"""
Test script to verify installation and dependencies.
"""

import sys

def test_imports():
    """Test if all required modules can be imported."""
    print("Testing imports...")
    
    try:
        import requests
        print("✓ requests")
    except ImportError as e:
        print(f"✗ requests: {e}")
        return False
    
    try:
        import boto3
        print("✓ boto3")
    except ImportError as e:
        print(f"✗ boto3: {e}")
        return False
    
    try:
        from PyQt6.QtWidgets import QApplication
        print("✓ PyQt6")
    except ImportError as e:
        print(f"✗ PyQt6: {e}")
        return False
    
    try:
        from cryptography.fernet import Fernet
        print("✓ cryptography")
    except ImportError as e:
        print(f"✗ cryptography: {e}")
        return False
    
    try:
        import dotenv
        print("✓ python-dotenv")
    except ImportError as e:
        print(f"✗ python-dotenv: {e}")
        return False
    
    return True

def test_modules():
    """Test if application modules can be imported."""
    print("\nTesting application modules...")
    
    try:
        from modules.config_manager import ConfigManager
        print("✓ config_manager")
    except ImportError as e:
        print(f"✗ config_manager: {e}")
        return False
    
    try:
        from modules.database import DatabaseManager
        print("✓ database")
    except ImportError as e:
        print(f"✗ database: {e}")
        return False
    
    try:
        from modules.duda_client import DudaAPIClient
        print("✓ duda_client")
    except ImportError as e:
        print(f"✗ duda_client: {e}")
        return False
    
    try:
        from modules.s3_client import S3Client
        print("✓ s3_client")
    except ImportError as e:
        print(f"✗ s3_client: {e}")
        return False
    
    try:
        from modules.data_fetcher import DataFetcher
        print("✓ data_fetcher")
    except ImportError as e:
        print(f"✗ data_fetcher: {e}")
        return False
    
    try:
        from modules.webhook_manager import WebhookManager
        print("✓ webhook_manager")
    except ImportError as e:
        print(f"✗ webhook_manager: {e}")
        return False
    
    try:
        from modules.main_window import MainWindow
        print("✓ main_window")
    except ImportError as e:
        print(f"✗ main_window: {e}")
        return False
    
    try:
        from modules.settings_dialog import SettingsDialog
        print("✓ settings_dialog")
    except ImportError as e:
        print(f"✗ settings_dialog: {e}")
        return False
    
    return True

def main():
    """Run all tests."""
    print("=" * 50)
    print("Duda Site Manager - Installation Test")
    print("=" * 50)
    
    if not test_imports():
        print("\n✗ Import test failed!")
        print("Run: pip3 install -r requirements.txt")
        return 1
    
    if not test_modules():
        print("\n✗ Module test failed!")
        return 1
    
    print("\n" + "=" * 50)
    print("✓ All tests passed!")
    print("=" * 50)
    print("\nYou can now run the application:")
    print("  python3 app.py")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
