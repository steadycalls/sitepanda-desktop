"""
Configuration Manager Module
Handles secure storage and retrieval of API credentials and application settings.
"""

import json
import os
from pathlib import Path
from cryptography.fernet import Fernet
from typing import Dict, Optional


class ConfigManager:
    """Manages encrypted configuration storage for the application."""
    
    def __init__(self, config_dir: str = None):
        """
        Initialize the configuration manager.
        
        Args:
            config_dir: Directory to store configuration files. Defaults to user's home directory.
        """
        if config_dir is None:
            config_dir = os.path.join(str(Path.home()), '.sitepanda-desktop')
        
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self.config_file = self.config_dir / 'config.enc'
        self.key_file = self.config_dir / 'key.key'
        
        self._ensure_key_exists()
        self.cipher = Fernet(self._load_key())
    
    def _ensure_key_exists(self):
        """Create encryption key if it doesn't exist."""
        if not self.key_file.exists():
            key = Fernet.generate_key()
            self.key_file.write_bytes(key)
            # Set restrictive permissions on the key file
            os.chmod(self.key_file, 0o600)
    
    def _load_key(self) -> bytes:
        """Load the encryption key."""
        return self.key_file.read_bytes()
    
    def save_config(self, config: Dict) -> bool:
        """
        Save configuration data (encrypted).
        
        Args:
            config: Dictionary containing configuration data
            
        Returns:
            True if successful, False otherwise
        """
        try:
            json_data = json.dumps(config, indent=2)
            encrypted_data = self.cipher.encrypt(json_data.encode())
            self.config_file.write_bytes(encrypted_data)
            # Set restrictive permissions on the config file
            os.chmod(self.config_file, 0o600)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def load_config(self) -> Dict:
        """
        Load configuration data (decrypted).
        
        Returns:
            Dictionary containing configuration data, or empty dict if no config exists
        """
        if not self.config_file.exists():
            return self._get_default_config()
        
        try:
            encrypted_data = self.config_file.read_bytes()
            decrypted_data = self.cipher.decrypt(encrypted_data)
            config = json.loads(decrypted_data.decode())
            return config
        except Exception as e:
            print(f"Error loading config: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict:
        """Return default configuration structure."""
        return {
            'duda': {
                'api_user': '',
                'api_password': ''
            },
            's3': {
                'access_key_id': '',
                'secret_access_key': '',
                'bucket_name': '',
                'region': 'us-east-1'
            },
            'webhooks': {
                'new_form_submission': '',
                'new_ecommerce_order': '',
                'daily_stats_summary': '',
                'new_blog_post': ''
            },
            'app_settings': {
                'auto_fetch_interval': 300,  # seconds
                'enable_notifications': True,
                'last_fetch_timestamp': None
            }
        }
    
    def get_duda_credentials(self) -> tuple:
        """
        Get Duda API credentials.
        
        Returns:
            Tuple of (api_user, api_password)
        """
        config = self.load_config()
        return (
            config.get('duda', {}).get('api_user', ''),
            config.get('duda', {}).get('api_password', '')
        )
    
    def get_s3_credentials(self) -> Dict:
        """
        Get S3 credentials.
        
        Returns:
            Dictionary with S3 configuration
        """
        config = self.load_config()
        return config.get('s3', {})
    
    def get_webhooks(self) -> Dict:
        """
        Get webhook URLs.
        
        Returns:
            Dictionary with webhook configurations
        """
        config = self.load_config()
        return config.get('webhooks', {})
    
    def get_app_settings(self) -> Dict:
        """
        Get application settings.
        
        Returns:
            Dictionary with app settings
        """
        config = self.load_config()
        return config.get('app_settings', {})
    
    def update_setting(self, section: str, key: str, value) -> bool:
        """
        Update a specific setting.
        
        Args:
            section: Configuration section (e.g., 'duda', 's3', 'webhooks')
            key: Setting key
            value: New value
            
        Returns:
            True if successful
        """
        config = self.load_config()
        if section not in config:
            config[section] = {}
        config[section][key] = value
        return self.save_config(config)
    
    def validate_duda_credentials(self) -> bool:
        """Check if Duda credentials are configured."""
        user, password = self.get_duda_credentials()
        return bool(user and password)
    
    def validate_s3_credentials(self) -> bool:
        """Check if S3 credentials are configured."""
        s3_config = self.get_s3_credentials()
        return bool(
            s3_config.get('access_key_id') and 
            s3_config.get('secret_access_key') and
            s3_config.get('bucket_name')
        )
