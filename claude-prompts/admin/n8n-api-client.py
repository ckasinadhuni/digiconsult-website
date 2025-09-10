#!/usr/bin/env python3

"""
n8n API Client for CLI Workflow Management
Handles authentication and workflow deployment
"""

import requests
import json
import os
from pathlib import Path

class N8nAPIClient:
    def __init__(self, base_url="http://localhost:5678"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.authenticated = False
        
    def login(self, email=None, password=None):
        """Attempt to authenticate with n8n"""
        # Try without auth first (if n8n is in open mode)
        try:
            response = self.session.get(f"{self.base_url}/rest/login")
            if response.status_code == 200:
                self.authenticated = True
                return True
        except:
            pass
            
        # If credentials provided, try to login
        if email and password:
            try:
                login_data = {"email": email, "password": password}
                response = self.session.post(f"{self.base_url}/rest/login", json=login_data)
                if response.status_code == 200:
                    self.authenticated = True
                    return True
            except:
                pass
        
        return False
    
    def get_credentials(self):
        """Get existing credentials"""
        if not self.authenticated:
            return None
            
        try:
            response = self.session.get(f"{self.base_url}/rest/credentials")
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error getting credentials: {e}")
        return None
    
    def get_workflows(self):
        """Get existing workflows"""
        if not self.authenticated:
            return None
            
        try:
            response = self.session.get(f"{self.base_url}/rest/workflows")
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error getting workflows: {e}")
        return None
    
    def create_workflow(self, workflow_data):
        """Create a new workflow"""
        if not self.authenticated:
            return None
            
        try:
            response = self.session.post(f"{self.base_url}/rest/workflows", json=workflow_data)
            if response.status_code == 200 or response.status_code == 201:
                return response.json()
            else:
                print(f"Error creating workflow: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Error creating workflow: {e}")
        return None
    
    def update_workflow(self, workflow_id, workflow_data):
        """Update existing workflow"""
        if not self.authenticated:
            return None
            
        try:
            response = self.session.put(f"{self.base_url}/rest/workflows/{workflow_id}", json=workflow_data)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error updating workflow: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Error updating workflow: {e}")
        return None

def main():
    client = N8nAPIClient()
    
    # Try to authenticate
    if not client.login():
        print("⚠️  Could not authenticate with n8n")
        print("n8n might be in authentication mode or not accessible")
        return
    
    print("✅ Connected to n8n successfully!")
    
    # Get existing credentials
    credentials = client.get_credentials()
    if credentials:
        print(f"📋 Found {len(credentials)} credentials:")
        for cred in credentials:
            print(f"  - {cred.get('name', 'Unknown')}: {cred.get('type', 'Unknown type')}")
    
    # Get existing workflows
    workflows = client.get_workflows()
    if workflows:
        print(f"🔄 Found {len(workflows)} workflows:")
        for workflow in workflows:
            print(f"  - {workflow.get('name', 'Unnamed')}")
    
    return client

if __name__ == "__main__":
    client = main()