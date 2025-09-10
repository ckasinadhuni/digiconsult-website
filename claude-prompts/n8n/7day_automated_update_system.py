#!/usr/bin/env python3

"""
7-Day Automated Update System with Data Protection
Comprehensive automated update strategy for n8n infrastructure
"""

import json
import subprocess
import requests
import time
import logging
from datetime import datetime, timedelta
from pathlib import Path
import docker
import schedule

class AutomatedUpdateSystem:
    def __init__(self):
        self.config_path = Path(__file__).parent / "config.json"
        self.load_config()
        self.setup_logging()
        self.docker_client = docker.from_env()
        
    def load_config(self):
        """Load system configuration"""
        with open(self.config_path, 'r') as f:
            self.config = json.load(f)
        
        self.services = {
            'caddy': {'risk': 'low', 'update_freq': 'weekly'},
            'faster-whisper': {'risk': 'low', 'update_freq': 'weekly'}, 
            'ollama': {'risk': 'medium', 'update_freq': 'bi-weekly'},
            'qdrant': {'risk': 'medium', 'update_freq': 'bi-weekly'},
            'n8n': {'risk': 'high', 'update_freq': 'monthly'}
        }
        
    def setup_logging(self):
        """Configure logging"""
        log_path = Path(__file__).parent / "logs"
        log_path.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_path / 'automated_updates.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def create_backup(self, service_name):
        """Create backup before update"""
        self.logger.info(f"Creating backup for {service_name}")
        
        backup_dir = Path(__file__).parent / "backups" / datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            # Backup volumes
            volumes = self.docker_client.volumes.list()
            service_volumes = [v for v in volumes if service_name in v.name.lower()]
            
            for volume in service_volumes:
                backup_file = backup_dir / f"{volume.name}.tar"
                cmd = [
                    "docker", "run", "--rm",
                    "-v", f"{volume.name}:/data",
                    "-v", f"{backup_dir}:/backup",
                    "alpine:latest",
                    "tar", "czf", f"/backup/{volume.name}.tar.gz", "/data"
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    self.logger.info(f"Backup created: {backup_file}")
                else:
                    self.logger.error(f"Backup failed for {volume.name}: {result.stderr}")
                    return False
                    
            return True
            
        except Exception as e:
            self.logger.error(f"Backup creation failed: {e}")
            return False
    
    def health_check(self, service_name):
        """Perform health check on service"""
        self.logger.info(f"Health check for {service_name}")
        
        try:
            container = self.docker_client.containers.get(service_name)
            if container.status != 'running':
                self.logger.error(f"{service_name} container not running")
                return False
                
            # Service-specific health checks
            if service_name == 'n8n':
                response = requests.get(f"{self.config['base_url']}/healthz", timeout=10)
                return response.status_code == 200
                
            elif service_name == 'ollama':
                response = requests.get(f"{self.config['local_services']['ollama']}/api/tags", timeout=10)
                return response.status_code == 200
                
            elif service_name == 'caddy':
                response = requests.get("https://n8n.digiconsult.ca", timeout=10, verify=False)
                return response.status_code in [200, 401, 403]  # Any response means proxy working
                
            else:
                return container.status == 'running'
                
        except Exception as e:
            self.logger.error(f"Health check failed for {service_name}: {e}")
            return False
    
    def update_service(self, service_name, dry_run=False):
        """Update specific service with safety measures"""
        self.logger.info(f"{'DRY RUN: ' if dry_run else ''}Updating {service_name}")
        
        if dry_run:
            self.logger.info(f"Would update {service_name} (dry run mode)")
            return True
            
        try:
            # 1. Pre-update health check
            if not self.health_check(service_name):
                self.logger.error(f"Pre-update health check failed for {service_name}")
                return False
            
            # 2. Create backup for high-risk services
            if self.services[service_name]['risk'] in ['high', 'medium']:
                if not self.create_backup(service_name):
                    self.logger.error(f"Backup failed for {service_name}, aborting update")
                    return False
            
            # 3. Pull latest image
            container = self.docker_client.containers.get(service_name)
            image_name = container.image.tags[0] if container.image.tags else container.image.id
            
            self.logger.info(f"Pulling latest image for {image_name}")
            self.docker_client.images.pull(image_name)
            
            # 4. Recreate container (preserve volumes and networks)
            container_config = container.attrs
            volumes = container_config['Mounts']
            networks = list(container_config['NetworkSettings']['Networks'].keys())
            env_vars = container_config['Config']['Env']
            
            self.logger.info(f"Stopping {service_name}")
            container.stop()
            container.remove()
            
            # 5. Start updated container
            self.logger.info(f"Starting updated {service_name}")
            volume_binds = {}
            for mount in volumes:
                if mount['Type'] == 'volume':
                    volume_binds[mount['Name']] = {'bind': mount['Destination']}
                elif mount['Type'] == 'bind':
                    volume_binds[mount['Source']] = {'bind': mount['Destination']}
            
            new_container = self.docker_client.containers.run(
                image_name,
                name=service_name,
                detach=True,
                restart_policy={"Name": "unless-stopped"},
                volumes=volume_binds,
                environment=env_vars,
                network=networks[0] if networks else None
            )
            
            # 6. Post-update health check
            time.sleep(10)  # Allow service to start
            if self.health_check(service_name):
                self.logger.info(f"✅ {service_name} updated successfully")
                return True
            else:
                self.logger.error(f"❌ Post-update health check failed for {service_name}")
                # TODO: Implement rollback logic
                return False
                
        except Exception as e:
            self.logger.error(f"Update failed for {service_name}: {e}")
            return False
    
    def system_health_report(self):
        """Generate system health report"""
        self.logger.info("Generating system health report")
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'services': {},
            'volumes': {},
            'system': {}
        }
        
        # Service status
        for service_name in self.services.keys():
            report['services'][service_name] = {
                'healthy': self.health_check(service_name),
                'last_checked': datetime.now().isoformat()
            }
        
        # Volume usage
        volumes = self.docker_client.volumes.list()
        for volume in volumes:
            if any(svc in volume.name.lower() for svc in self.services.keys()):
                # Get volume size (requires privileged container)
                report['volumes'][volume.name] = {
                    'name': volume.name,
                    'created': volume.attrs.get('CreatedAt', 'unknown')
                }
        
        # System info
        info = self.docker_client.info()
        report['system'] = {
            'docker_version': info.get('ServerVersion'),
            'containers_running': info.get('ContainersRunning'),
            'images_count': info.get('Images')
        }
        
        return report
    
    def daily_tasks(self):
        """Daily maintenance tasks"""
        self.logger.info("Running daily maintenance tasks")
        
        # Health checks
        report = self.system_health_report()
        
        # Log cleanup (keep 30 days)
        log_dir = Path(__file__).parent / "logs"
        if log_dir.exists():
            cutoff = datetime.now() - timedelta(days=30)
            for log_file in log_dir.glob("*.log*"):
                if log_file.stat().st_mtime < cutoff.timestamp():
                    log_file.unlink()
                    self.logger.info(f"Cleaned up old log: {log_file}")
        
        # Docker system cleanup
        self.docker_client.containers.prune()
        self.docker_client.images.prune(filters={'dangling': True})
        
    def weekly_tasks(self):
        """Weekly update tasks (low risk)"""
        self.logger.info("Running weekly update tasks")
        
        low_risk_services = [name for name, config in self.services.items() 
                           if config['risk'] == 'low']
        
        for service in low_risk_services:
            self.update_service(service)
    
    def bi_weekly_tasks(self):
        """Bi-weekly update tasks (medium risk)"""
        self.logger.info("Running bi-weekly update tasks")
        
        medium_risk_services = [name for name, config in self.services.items() 
                              if config['risk'] == 'medium']
        
        for service in medium_risk_services:
            self.update_service(service)
    
    def monthly_tasks(self):
        """Monthly update tasks (high risk)"""
        self.logger.info("Running monthly update tasks")
        
        high_risk_services = [name for name, config in self.services.items() 
                            if config['risk'] == 'high']
        
        for service in high_risk_services:
            # Extra validation for high-risk updates
            if service == 'n8n':
                # Check for workflow compatibility issues
                # Validate API endpoints
                # Ensure backup is recent
                pass
                
            self.update_service(service)
    
    def schedule_tasks(self):
        """Schedule all automated tasks"""
        self.logger.info("Setting up automated update schedule")
        
        # Daily tasks
        schedule.every().day.at("02:00").do(self.daily_tasks)
        
        # Weekly tasks (Sundays at 3 AM)
        schedule.every().sunday.at("03:00").do(self.weekly_tasks)
        
        # Bi-weekly tasks (1st and 15th at 4 AM)
        schedule.every().month.do(lambda: self.bi_weekly_tasks() if datetime.now().day in [1, 15] else None).at("04:00")
        
        # Monthly tasks (1st of month at 5 AM)
        schedule.every().month.do(lambda: self.monthly_tasks() if datetime.now().day == 1 else None).at("05:00")
    
    def run_scheduler(self):
        """Run the scheduler"""
        self.logger.info("🚀 Starting 7-Day Automated Update System")
        self.schedule_tasks()
        
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="7-Day Automated Update System")
    parser.add_argument('--dry-run', action='store_true', help='Run in dry-run mode')
    parser.add_argument('--task', choices=['daily', 'weekly', 'bi-weekly', 'monthly', 'schedule'], 
                       help='Run specific task')
    parser.add_argument('--service', help='Update specific service')
    
    args = parser.parse_args()
    
    system = AutomatedUpdateSystem()
    
    if args.service:
        system.update_service(args.service, dry_run=args.dry_run)
    elif args.task == 'daily':
        system.daily_tasks()
    elif args.task == 'weekly':
        system.weekly_tasks()
    elif args.task == 'bi-weekly':
        system.bi_weekly_tasks()
    elif args.task == 'monthly':
        system.monthly_tasks()
    elif args.task == 'schedule':
        system.run_scheduler()
    else:
        print("7-Day Automated Update System")
        print("Usage examples:")
        print("  python 7day_automated_update_system.py --task schedule")
        print("  python 7day_automated_update_system.py --service n8n --dry-run")
        print("  python 7day_automated_update_system.py --task weekly")

if __name__ == "__main__":
    main()