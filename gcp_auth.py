#!/usr/bin/env python3
"""
Google Cloud Authentication Helper
This script handles Google Cloud authentication using environment variables.
"""

import os
import json
import tempfile
from google.auth import default
from google.cloud import storage


def setup_gcp_credentials():
    """Setup Google Cloud credentials from environment variables."""
    
    # Get credentials content from environment variable
    creds_content = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_CONTENT')
    
    if creds_content:
        # Parse JSON credentials
        try:
            creds_dict = json.loads(creds_content)
            
            # Create temporary credentials file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                json.dump(creds_dict, f)
                temp_creds_path = f.name
            
            # Set environment variable for Google Cloud SDK
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = temp_creds_path
            
            print(f"✅ Google Cloud credentials configured successfully")
            print(f"📁 Project ID: {creds_dict.get('project_id', 'N/A')}")
            print(f"📧 Client Email: {creds_dict.get('client_email', 'N/A')}")
            
            return temp_creds_path
            
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing Google Cloud credentials: {e}")
            return None
    else:
        print("⚠️  No Google Cloud credentials found in environment variables")
        return None


def test_gcp_connection():
    """Test Google Cloud connection."""
    try:
        # Test authentication
        credentials, project = default()
        print(f"✅ Google Cloud authentication successful")
        print(f"📁 Project: {project}")
        
        # Test Cloud Storage access
        client = storage.Client()
        buckets = list(client.list_buckets())
        print(f"📦 Found {len(buckets)} storage buckets")
        
        return True
    except Exception as e:
        print(f"❌ Google Cloud connection test failed: {e}")
        return False


if __name__ == "__main__":
    # Setup credentials
    creds_path = setup_gcp_credentials()
    
    if creds_path:
        # Test connection
        test_gcp_connection()
    else:
        print("❌ Failed to setup Google Cloud credentials")
