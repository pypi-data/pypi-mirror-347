#!/usr/bin/env python3
"""
Fiducia Blockchain Mining Client - Core functionality
"""
import os
import sys
import subprocess
import time
import signal
import platform
import shutil

class FiduciaMiner:
    def __init__(self, repo_url, miner_address, db_name="mining.db", p2p_port=8333, 
                 api_port=8545, connect_to=None, mining_threads=None):
        self.repo_url = repo_url
        self.miner_address = miner_address
        self.db_name = db_name
        self.p2p_port = p2p_port
        self.api_port = api_port
        self.connect_to = connect_to
        self.mining_threads = mining_threads
        self.process = None
        self.base_dir = os.path.expanduser("~/fiducia-miner")
        self.fiducia_dir = os.path.join(self.base_dir, "fiducia")
        
    def setup(self):
        """Clone the repository and install dependencies"""
        print("[+] Setting up Fiducia mining environment...")
        
        # Create base directory if it doesn't exist
        os.makedirs(self.base_dir, exist_ok=True)
        
        # Check if repo already cloned
        if not os.path.exists(self.fiducia_dir):
            print(f"[+] Cloning Fiducia repository from {self.repo_url}...")
            subprocess.run(["git", "clone", self.repo_url, self.fiducia_dir], check=True)
        else:
            print(f"[+] Fiducia repository already exists at {self.fiducia_dir}")
            
        # Navigate to the fiducia directory
        os.chdir(self.fiducia_dir)
        
        # Setup virtual environment
        venv_path = os.path.join(self.fiducia_dir, ".venv")
        if not os.path.exists(venv_path):
            print("[+] Creating Python virtual environment...")
            subprocess.run([sys.executable, "-m", "venv", ".venv"], check=True)
        
        # Determine how to activate the virtual environment based on the OS
        if platform.system() == "Windows":
            activate_script = os.path.join(venv_path, "Scripts", "activate")
            python_path = os.path.join(venv_path, "Scripts", "python")
            pip_path = os.path.join(venv_path, "Scripts", "pip")
        else:
            activate_script = os.path.join(venv_path, "bin", "activate")
            python_path = os.path.join(venv_path, "bin", "python")
            pip_path = os.path.join(venv_path, "bin", "pip")
        
        # Install dependencies
        print("[+] Installing dependencies...")
        subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)
        
        # Run tests to ensure everything is working
        print("[+] Running tests to verify the installation...")
        try:
            subprocess.run(["./run_tests.sh"], check=True)
            print("[+] All tests passed!")
        except subprocess.CalledProcessError:
            print("[!] Warning: Some tests failed. The miner might not work correctly.")
            response = input("Do you want to continue anyway? (y/n): ")
            if response.lower() != 'y':
                sys.exit(1)
                
        return python_path
                
    def start_mining(self, python_path):
        """Start the Fiducia node with mining enabled"""
        print(f"[+] Starting Fiducia mining node with address: {self.miner_address}")
        
        # Change to the repository directory
        os.chdir(self.fiducia_dir)
        
        # Build the command with required arguments
        cmd = [
            python_path,
            "src/main.py",
            "--db", self.db_name,
            "--p2p-port", str(self.p2p_port),
            "--api-port", str(self.api_port),
            "--miner-address", self.miner_address,
            "--enable-mining"
        ]
        
        # Add optional connect-to argument if provided
        if self.connect_to:
            cmd.extend(["--connect-to", self.connect_to])
            
        # Add mining threads if specified
        if self.mining_threads:
            cmd.extend(["--mining-threads", str(self.mining_threads)])
            
        # Set the PYTHONPATH environment variable
        env = os.environ.copy()
        env["PYTHONPATH"] = "src"
        
        print(f"[+] Running command: {' '.join(cmd)}")
        self.process = subprocess.Popen(cmd, env=env)
        
        print(f"""
[+] Mining node started!
    - Miner address: {self.miner_address}
    - Database: {self.db_name}
    - P2P Port: {self.p2p_port}
    - API Port: {self.api_port}
    - Dashboard URL: http://localhost:{self.api_port}/dashboard
        """)
        
    def stop(self):
        """Stop the mining process"""
        if self.process:
            print("[+] Stopping mining node...")
            self.process.send_signal(signal.SIGINT)
            self.process.wait()
            print("[+] Mining node stopped.") 