"""
S3 Client Module
Handles fetching site statistics from Duda-provided S3 bucket.
"""

import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from typing import List, Dict, Optional
import json
import csv
from io import StringIO


class S3Client:
    """Client for fetching data from S3 bucket."""
    
    def __init__(self, access_key_id: str, secret_access_key: str, 
                 bucket_name: str, region: str = 'us-east-1'):
        """
        Initialize S3 client.
        
        Args:
            access_key_id: AWS Access Key ID
            secret_access_key: AWS Secret Access Key
            bucket_name: S3 bucket name
            region: AWS region
        """
        self.bucket_name = bucket_name
        self.region = region
        
        try:
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=access_key_id,
                aws_secret_access_key=secret_access_key,
                region_name=region
            )
        except Exception as e:
            print(f"Error initializing S3 client: {e}")
            self.s3_client = None
    
    def test_connection(self) -> bool:
        """
        Test S3 connection and credentials.
        
        Returns:
            True if connection is successful
        """
        if not self.s3_client:
            return False
        
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            return True
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', '')
            if error_code == '404':
                print(f"Bucket '{self.bucket_name}' does not exist")
            elif error_code == '403':
                print(f"Access denied to bucket '{self.bucket_name}'")
            else:
                print(f"Error accessing bucket: {e}")
            return False
        except NoCredentialsError:
            print("No AWS credentials found")
            return False
        except Exception as e:
            print(f"Error testing S3 connection: {e}")
            return False
    
    def list_files(self, prefix: str = '', max_keys: int = 1000) -> List[str]:
        """
        List files in S3 bucket.
        
        Args:
            prefix: Prefix to filter files (folder path)
            max_keys: Maximum number of files to return
            
        Returns:
            List of file keys
        """
        if not self.s3_client:
            return []
        
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix,
                MaxKeys=max_keys
            )
            
            if 'Contents' not in response:
                return []
            
            return [obj['Key'] for obj in response['Contents']]
        except Exception as e:
            print(f"Error listing files: {e}")
            return []
    
    def download_file(self, key: str, local_path: str) -> bool:
        """
        Download a file from S3.
        
        Args:
            key: S3 object key
            local_path: Local file path to save to
            
        Returns:
            True if successful
        """
        if not self.s3_client:
            return False
        
        try:
            self.s3_client.download_file(self.bucket_name, key, local_path)
            return True
        except Exception as e:
            print(f"Error downloading file {key}: {e}")
            return False
    
    def read_file_content(self, key: str) -> Optional[str]:
        """
        Read file content from S3 as string.
        
        Args:
            key: S3 object key
            
        Returns:
            File content as string, or None on error
        """
        if not self.s3_client:
            return None
        
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=key)
            content = response['Body'].read().decode('utf-8')
            return content
        except Exception as e:
            print(f"Error reading file {key}: {e}")
            return None
    
    def read_json_file(self, key: str) -> Optional[Dict]:
        """
        Read and parse JSON file from S3.
        
        Args:
            key: S3 object key
            
        Returns:
            Parsed JSON data, or None on error
        """
        content = self.read_file_content(key)
        
        if not content:
            return None
        
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON from {key}: {e}")
            return None
    
    def read_csv_file(self, key: str) -> Optional[List[Dict]]:
        """
        Read and parse CSV file from S3.
        
        Args:
            key: S3 object key
            
        Returns:
            List of dictionaries (rows), or None on error
        """
        content = self.read_file_content(key)
        
        if not content:
            return None
        
        try:
            csv_reader = csv.DictReader(StringIO(content))
            return list(csv_reader)
        except Exception as e:
            print(f"Error parsing CSV from {key}: {e}")
            return None
    
    def get_site_stats_files(self, site_name: str = None) -> List[str]:
        """
        Get list of statistics files for a site.
        
        Args:
            site_name: Optional site name to filter by
            
        Returns:
            List of file keys
        """
        # This is a generic implementation - actual structure depends on how
        # Duda organizes files in the S3 bucket
        
        prefix = ''
        if site_name:
            # Common patterns: stats/{site_name}/, {site_name}/stats/, etc.
            # Try multiple patterns
            patterns = [
                f'stats/{site_name}/',
                f'{site_name}/stats/',
                f'analytics/{site_name}/',
                f'{site_name}/analytics/'
            ]
            
            all_files = []
            for pattern in patterns:
                files = self.list_files(prefix=pattern)
                all_files.extend(files)
            
            return all_files
        else:
            # List all stats files
            patterns = ['stats/', 'analytics/']
            all_files = []
            for pattern in patterns:
                files = self.list_files(prefix=pattern)
                all_files.extend(files)
            
            return all_files
    
    def fetch_site_statistics(self, site_name: str = None) -> List[Dict]:
        """
        Fetch and parse site statistics from S3.
        
        Args:
            site_name: Optional site name to filter by
            
        Returns:
            List of statistics data
        """
        stats_files = self.get_site_stats_files(site_name)
        
        if not stats_files:
            print(f"No statistics files found for {site_name or 'any site'}")
            return []
        
        all_stats = []
        
        for file_key in stats_files:
            # Determine file type and parse accordingly
            if file_key.endswith('.json'):
                data = self.read_json_file(file_key)
                if data:
                    all_stats.append({
                        'source_file': file_key,
                        'data': data,
                        'format': 'json'
                    })
            elif file_key.endswith('.csv'):
                data = self.read_csv_file(file_key)
                if data:
                    all_stats.append({
                        'source_file': file_key,
                        'data': data,
                        'format': 'csv'
                    })
        
        return all_stats
    
    def get_latest_stats_file(self, site_name: str = None) -> Optional[str]:
        """
        Get the most recent statistics file.
        
        Args:
            site_name: Optional site name to filter by
            
        Returns:
            File key of the latest stats file
        """
        files = self.get_site_stats_files(site_name)
        
        if not files:
            return None
        
        # Sort by key (assuming files have date in name)
        # This is a simple implementation - may need adjustment based on actual naming
        files.sort(reverse=True)
        
        return files[0] if files else None
