#!/usr/bin/env python3
"""
Fiducia Blockchain Mining Client - Command Line Interface
"""
import argparse
import time
import shutil
import os
import sys
import signal

from .miner import FiduciaMiner

def main():
    parser = argparse.ArgumentParser(description="Fiducia Blockchain Mining Client")
    parser.add_argument("--repo-url", required=True, help="URL of the Fiducia repository")
    parser.add_argument("--miner-address", required=True, help="Address to receive mining rewards")
    parser.add_argument("--db", default="mining.db", help="Database filename (default: mining.db)")
    parser.add_argument("--p2p-port", type=int, default=8333, help="P2P port (default: 8333)")
    parser.add_argument("--api-port", type=int, default=8545, help="API port (default: 8545)")
    parser.add_argument("--connect-to", help="Connect to an existing node (format: host:port)")
    parser.add_argument("--mining-threads", type=int, help="Number of mining threads")
    parser.add_argument("--clean", action="store_true", help="Clean existing installation before setup")
    
    args = parser.parse_args()
    
    # Clean if requested
    if args.clean:
        base_dir = os.path.expanduser("~/fiducia-miner")
        if os.path.exists(base_dir):
            print(f"[+] Cleaning existing installation at {base_dir}")
            shutil.rmtree(base_dir)
    
    # Initialize and start the miner
    miner = FiduciaMiner(
        repo_url=args.repo_url,
        miner_address=args.miner_address,
        db_name=args.db,
        p2p_port=args.p2p_port,
        api_port=args.api_port,
        connect_to=args.connect_to,
        mining_threads=args.mining_threads
    )
    
    try:
        python_path = miner.setup()
        miner.start_mining(python_path)
        
        print("[+] Press Ctrl+C to stop mining...")
        # Keep the script running until interrupted
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[+] Interrupt received, shutting down...")
    finally:
        miner.stop()
        print("[+] Fiducia miner has been shut down.")

if __name__ == "__main__":
    main() 