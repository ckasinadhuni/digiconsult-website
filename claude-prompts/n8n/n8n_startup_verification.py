#!/usr/bin/env python3

"""
Automated n8n Startup Verification Script
Validates n8n service health, API access, and core functionality
"""

import json
import requests
import time
import subprocess
import sys
from pathlib import Path

class N8nStartupVerifier:
    def __init__(self):
        self.config_path = Path(__file__).parent / "config.json"
        self.load_config()
        
    def load_config(self):
        """Load configuration"""
        try:
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
            self.headers = {
                "X-N8N-API-KEY": self.config["api_key"],
                "Content-Type": "application/json"
            }
            self.base_url = self.config["base_url"]
        except Exception as e:
            print(f"❌ Config load failed: {e}")
            sys.exit(1)
    
    def log(self, message, level="INFO"):
        """Formatted logging"""
        icons = {"INFO": "🔄", "SUCCESS": "✅", "ERROR": "❌", "WARNING": "⚠️"}
        print(f"{icons.get(level, '•')} {message}")
    
    def check_docker_container(self):
        """Verify n8n container is running"""
        self.log("Checking n8n Docker container status...")
        try:
            result = subprocess.run(
                ["docker", "ps", "--filter", "name=n8n", "--format", "{{.Status}}"],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0 and "Up" in result.stdout:
                self.log("n8n container is running", "SUCCESS")
                return True
            else:
                self.log("n8n container not running or not found", "ERROR")
                return False
        except Exception as e:
            self.log(f"Container check failed: {e}", "ERROR")
            return False
    
    def check_api_health(self):
        """Check n8n API health"""
        self.log("Checking n8n API health...")
        try:
            response = requests.get(f"{self.base_url}/healthz", timeout=10)
            if response.status_code == 200:
                self.log("n8n API health check passed", "SUCCESS")
                return True
            else:
                self.log(f"API health check failed: {response.status_code}", "ERROR")
                return False
        except Exception as e:
            self.log(f"API health check error: {e}", "ERROR")
            return False
    
    def check_api_authentication(self):
        """Verify API key authentication"""
        self.log("Checking API key authentication...")
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/workflows",
                headers=self.headers,
                timeout=10
            )
            if response.status_code == 200:
                workflow_count = len(response.json().get('data', []))
                self.log(f"API authentication successful ({workflow_count} workflows found)", "SUCCESS")
                return True
            else:
                self.log(f"API authentication failed: {response.status_code}", "ERROR")
                return False
        except Exception as e:
            self.log(f"API authentication error: {e}", "ERROR")
            return False
    
    def check_node_types(self):
        """Verify essential node types are available"""
        self.log("Checking essential node types...")
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/node-types",
                headers=self.headers,
                timeout=10
            )
            if response.status_code == 200:
                available_nodes = [node['name'] for node in response.json()]
                
                essential_nodes = [
                    "@n8n/n8n-nodes-base.manualTrigger",
                    "@n8n/n8n-nodes-base.code",
                    "@n8n/n8n-nodes-base.httpRequest",
                    "@n8n/n8n-nodes-base.set"
                ]
                
                missing_nodes = []
                for node in essential_nodes:
                    if node not in available_nodes:
                        missing_nodes.append(node)
                
                if not missing_nodes:
                    self.log(f"All essential node types available ({len(available_nodes)} total)", "SUCCESS")
                    
                    # Check for LangChain availability
                    langchain_count = len([n for n in available_nodes if 'langchain' in n.lower()])
                    if langchain_count > 0:
                        self.log(f"LangChain nodes available ({langchain_count} found)", "SUCCESS")
                    else:
                        self.log("LangChain nodes not available (use ai-beta image for LangChain)", "WARNING")
                    
                    return True
                else:
                    self.log(f"Missing essential nodes: {missing_nodes}", "ERROR")
                    return False
            else:
                self.log(f"Node types check failed: {response.status_code}", "ERROR")
                return False
        except Exception as e:
            self.log(f"Node types check error: {e}", "ERROR")
            return False
    
    def check_credentials(self):
        """Verify credentials are accessible"""
        self.log("Checking credentials access...")
        try:
            response = requests.get(
                f"{self.base_url}/api/credentials",
                headers=self.headers,
                timeout=10
            )
            if response.status_code == 200:
                credentials = response.json().get('data', [])
                cred_types = {}
                for cred in credentials:
                    cred_type = cred.get('type', 'unknown')
                    cred_types[cred_type] = cred_types.get(cred_type, 0) + 1
                
                self.log(f"Credentials accessible ({len(credentials)} total)", "SUCCESS")
                for cred_type, count in cred_types.items():
                    self.log(f"  • {cred_type}: {count}", "INFO")
                return True
            else:
                self.log(f"Credentials check failed: {response.status_code}", "ERROR")
                return False
        except Exception as e:
            self.log(f"Credentials check error: {e}", "ERROR")
            return False
    
    def check_external_services(self):
        """Check external service connectivity"""
        self.log("Checking external service connectivity...")
        results = {}
        
        # Check Ollama
        try:
            response = requests.get(f"{self.config['local_services']['ollama']}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                self.log(f"Ollama service accessible ({len(models)} models)", "SUCCESS")
                results['ollama'] = True
            else:
                self.log(f"Ollama service error: {response.status_code}", "WARNING")
                results['ollama'] = False
        except Exception as e:
            self.log(f"Ollama service unavailable: {e}", "WARNING")
            results['ollama'] = False
        
        # Check Faster-Whisper
        try:
            response = requests.get(f"{self.config['local_services']['whisper']}/health", timeout=5)
            if response.status_code == 200:
                self.log("Faster-Whisper service accessible", "SUCCESS")
                results['whisper'] = True
            else:
                self.log(f"Faster-Whisper service error: {response.status_code}", "WARNING")
                results['whisper'] = False
        except Exception as e:
            self.log(f"Faster-Whisper service unavailable: {e}", "WARNING")
            results['whisper'] = False
        
        return results
    
    def get_version_info(self):
        """Get n8n version information"""
        self.log("Getting version information...")
        try:
            result = subprocess.run(
                ["docker", "exec", "n8n", "n8n", "--version"],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                version = result.stdout.strip()
                self.log(f"n8n version: {version}", "SUCCESS")
                return version
            else:
                self.log("Could not retrieve version", "WARNING")
                return None
        except Exception as e:
            self.log(f"Version check error: {e}", "WARNING")
            return None
    
    def run_full_verification(self):
        """Run complete startup verification"""
        self.log("=" * 60)
        self.log("N8N STARTUP VERIFICATION")
        self.log("=" * 60)
        
        checks = [
            ("Docker Container", self.check_docker_container),
            ("API Health", self.check_api_health),
            ("API Authentication", self.check_api_authentication), 
            ("Node Types", self.check_node_types),
            ("Credentials", self.check_credentials)
        ]
        
        results = {}
        for check_name, check_func in checks:
            results[check_name] = check_func()
        
        # External services (non-critical)
        service_results = self.check_external_services()
        version = self.get_version_info()
        
        # Summary
        self.log("=" * 60)
        self.log("VERIFICATION SUMMARY")
        self.log("=" * 60)
        
        critical_passed = all(results.values())
        
        for check_name, passed in results.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            self.log(f"{check_name}: {status}")
        
        self.log("=" * 30)
        self.log("EXTERNAL SERVICES:")
        for service, status in service_results.items():
            status_icon = "✅" if status else "⚠️"
            self.log(f"{service.upper()}: {status_icon}")
        
        if version:
            self.log(f"VERSION: {version}")
        
        self.log("=" * 60)
        
        if critical_passed:
            self.log("🎉 ALL CRITICAL CHECKS PASSED - N8N IS READY!", "SUCCESS")
            return True
        else:
            self.log("💥 CRITICAL CHECKS FAILED - N8N NOT READY", "ERROR")
            return False

def main():
    """Main entry point"""
    verifier = N8nStartupVerifier()
    success = verifier.run_full_verification()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()