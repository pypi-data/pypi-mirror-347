#!/usr/bin/env python3
"""
Fiducia Blockchain Mining Client - Core functionality
"""
import os
import sys
import time
import json
import hashlib
import socket
import threading
import random
import sqlite3
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('fiducia-miner')

class Block:
    """Represents a block in the blockchain"""
    def __init__(self, index, timestamp, transactions, previous_hash, difficulty=4):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.difficulty = difficulty
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """Calculate the hash of the block"""
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "difficulty": self.difficulty,
            "nonce": self.nonce
        }, sort_keys=True).encode()
        
        return hashlib.sha256(block_string).hexdigest()
    
    def mine_block(self):
        """Mine the block by finding a hash with the required difficulty"""
        target = '0' * self.difficulty
        
        while self.hash[:self.difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
            
        logger.info(f"Block mined: {self.hash}")
        return self

class Transaction:
    """Represents a transaction in the blockchain"""
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = datetime.now().isoformat()
        self.signature = ""
        
    def calculate_hash(self):
        """Calculate the hash of the transaction"""
        tx_string = json.dumps({
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "timestamp": self.timestamp
        }, sort_keys=True).encode()
        
        return hashlib.sha256(tx_string).hexdigest()

class Blockchain:
    """The core blockchain implementation"""
    def __init__(self, db_path, miner_address):
        self.chain = []
        self.mempool = []
        self.db_path = db_path
        self.miner_address = miner_address
        self.mining_reward = 50
        self.difficulty = 4
        self.init_db()
        self.load_chain()
        
        # Create genesis block if chain is empty
        if not self.chain:
            self.create_genesis_block()
    
    def init_db(self):
        """Initialize the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create blocks table - quote the 'index' column name to avoid reserved keyword issues
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS blocks (
            hash TEXT PRIMARY KEY,
            "index" INTEGER,
            timestamp TEXT,
            previous_hash TEXT,
            difficulty INTEGER,
            nonce INTEGER,
            transactions TEXT
        )
        ''')
        
        # Create transactions table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            hash TEXT PRIMARY KEY,
            sender TEXT,
            recipient TEXT,
            amount REAL,
            timestamp TEXT,
            block_hash TEXT
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def load_chain(self):
        """Load the blockchain from the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM blocks ORDER BY "index"')
        blocks = cursor.fetchall()
        
        for block_data in blocks:
            block = Block(
                index=block_data[1],
                timestamp=block_data[2],
                transactions=json.loads(block_data[6]),
                previous_hash=block_data[3]
            )
            block.difficulty = block_data[4]
            block.nonce = block_data[5]
            block.hash = block_data[0]
            self.chain.append(block)
        
        conn.close()
        
        logger.info(f"Loaded {len(self.chain)} blocks from database")
    
    def create_genesis_block(self):
        """Create the genesis block"""
        genesis_block = Block(0, datetime.now().isoformat(), [], "0")
        genesis_block.mine_block()
        self.chain.append(genesis_block)
        self.save_block(genesis_block)
        logger.info("Genesis block created")
        
    def save_block(self, block):
        """Save a block to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO blocks (hash, "index", timestamp, previous_hash, difficulty, nonce, transactions)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            block.hash,
            block.index,
            block.timestamp,
            block.previous_hash,
            block.difficulty,
            block.nonce,
            json.dumps(block.transactions)
        ))
        
        for tx in block.transactions:
            cursor.execute('''
            INSERT OR IGNORE INTO transactions (hash, sender, recipient, amount, timestamp, block_hash)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                tx.get('hash', hashlib.sha256(json.dumps(tx, sort_keys=True).encode()).hexdigest()),
                tx.get('sender', ''),
                tx.get('recipient', ''),
                tx.get('amount', 0),
                tx.get('timestamp', datetime.now().isoformat()),
                block.hash
            ))
        
        conn.commit()
        conn.close()
    
    def add_transaction(self, sender, recipient, amount):
        """Add a transaction to the mempool"""
        transaction = Transaction(sender, recipient, amount)
        transaction_hash = transaction.calculate_hash()
        
        tx_dict = {
            "hash": transaction_hash,
            "sender": transaction.sender,
            "recipient": transaction.recipient,
            "amount": transaction.amount,
            "timestamp": transaction.timestamp
        }
        
        self.mempool.append(tx_dict)
        logger.info(f"Transaction added to mempool: {transaction_hash}")
        return transaction_hash
    
    def mine_pending_transactions(self):
        """Mine pending transactions and add a reward transaction"""
        # Add reward transaction for the miner
        reward_tx = {
            "sender": "NETWORK",
            "recipient": self.miner_address,
            "amount": self.mining_reward,
            "timestamp": datetime.now().isoformat()
        }
        reward_tx["hash"] = hashlib.sha256(json.dumps(reward_tx, sort_keys=True).encode()).hexdigest()
        
        # Create transactions list including reward
        transactions = self.mempool[:10]  # Limit to 10 transactions per block
        transactions.insert(0, reward_tx)  # Reward transaction comes first
        
        # Create and mine the new block
        block = Block(
            index=len(self.chain),
            timestamp=datetime.now().isoformat(),
            transactions=transactions,
            previous_hash=self.chain[-1].hash,
            difficulty=self.difficulty
        )
        
        logger.info(f"Mining new block with {len(transactions)} transactions...")
        block.mine_block()
        
        # Add the mined block to the chain
        self.chain.append(block)
        self.save_block(block)
        
        # Remove the processed transactions from the mempool
        self.mempool = self.mempool[10:]
        
        logger.info(f"Block #{block.index} mined successfully: {block.hash}")
        logger.info(f"Mining reward of {self.mining_reward} FID sent to {self.miner_address}")
        
        return block
    
    def get_balance(self, address):
        """Get the balance for an address"""
        balance = 0
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get all transactions where the address is the recipient
        cursor.execute('SELECT amount FROM transactions WHERE recipient = ?', (address,))
        received = cursor.fetchall()
        
        # Get all transactions where the address is the sender
        cursor.execute('SELECT amount FROM transactions WHERE sender = ?', (address,))
        sent = cursor.fetchall()
        
        conn.close()
        
        # Calculate balance
        for amount in received:
            balance += amount[0]
            
        for amount in sent:
            balance -= amount[0]
        
        return balance

class FiduchiaNode:
    """A node in the Fiducia network"""
    def __init__(self, db_path, miner_address, p2p_port=8333, api_port=8545):
        self.db_path = db_path
        self.blockchain = Blockchain(db_path, miner_address)
        self.p2p_port = p2p_port
        self.api_port = api_port
        self.peers = set()
        self.mining = False
        self.mining_thread = None
        self.api_thread = None
    
    def start_mining(self, threads=1):
        """Start the mining process"""
        if self.mining:
            logger.warning("Mining is already running")
            return
        
        self.mining = True
        self.mining_thread = threading.Thread(target=self._mine_continuously)
        self.mining_thread.daemon = True
        self.mining_thread.start()
        
        logger.info(f"Mining started with {threads} threads")
    
    def stop_mining(self):
        """Stop the mining process"""
        self.mining = False
        if self.mining_thread:
            self.mining_thread.join(timeout=1)
            logger.info("Mining stopped")
    
    def _mine_continuously(self):
        """Mine blocks continuously"""
        while self.mining:
            # Add a test transaction if mempool is empty
            if len(self.blockchain.mempool) == 0:
                random_amount = round(random.uniform(0.1, 10.0), 2)
                self.blockchain.add_transaction(
                    "NETWORK",
                    "TestUser" + str(random.randint(1000, 9999)),
                    random_amount
                )
            
            # Mine the block
            block = self.blockchain.mine_pending_transactions()
            
            # Broadcast the new block to peers
            self._broadcast_new_block(block)
            
            # Small pause to prevent CPU overload
            time.sleep(0.1)
    
    def _broadcast_new_block(self, block):
        """Broadcast a newly mined block to all peers"""
        # In a real implementation, this would send the block to all peers
        # For now, we'll just log it
        logger.info(f"Broadcasting new block {block.hash} to {len(self.peers)} peers")
    
    def connect_to_peer(self, host, port):
        """Connect to a peer node"""
        peer_address = f"{host}:{port}"
        if peer_address not in self.peers:
            self.peers.add(peer_address)
            logger.info(f"Connected to peer: {peer_address}")
            return True
        return False
    
    def start_api_server(self):
        """Start the API server"""
        # In a real implementation, this would start a web server
        # For this simplified version, we'll just simulate it
        logger.info(f"API server started on port {self.api_port}")
        logger.info(f"Dashboard available at http://localhost:{self.api_port}/dashboard")
        
        self.api_thread = threading.Thread(target=self._api_server_loop)
        self.api_thread.daemon = True
        self.api_thread.start()
    
    def _api_server_loop(self):
        """Simple loop to simulate API server activity"""
        while True:
            time.sleep(60)
            # In a real implementation, this would handle API requests
    
    def stop(self):
        """Stop all services"""
        self.stop_mining()
        logger.info("Node stopped")

class FiduciaMiner:
    """Main miner class"""
    def __init__(self, miner_address, db_name="mining.db", p2p_port=8333,
                 api_port=8545, connect_to=None, mining_threads=1):
        self.miner_address = miner_address
        self.db_name = db_name
        self.p2p_port = p2p_port
        self.api_port = api_port
        self.connect_to = connect_to
        self.mining_threads = mining_threads or 1
        self.node = None
        self.base_dir = os.path.expanduser("~/fiducia-miner-data")
        
    def setup(self):
        """Set up the mining environment"""
        logger.info("Setting up Fiducia mining environment...")
        
        # Create base directory if it doesn't exist
        os.makedirs(self.base_dir, exist_ok=True)
        
        # Path to the database
        db_path = os.path.join(self.base_dir, self.db_name)
        
        return db_path
                
    def start_mining(self):
        """Start the Fiducia mining node"""
        logger.info(f"Starting Fiducia mining node with address: {self.miner_address}")
        
        # Set up the environment
        db_path = self.setup()
        
        # Create and start the node
        self.node = FiduchiaNode(
            db_path=db_path,
            miner_address=self.miner_address,
            p2p_port=self.p2p_port,
            api_port=self.api_port
        )
        
        # Connect to another node if specified
        if self.connect_to:
            try:
                host, port = self.connect_to.split(':')
                self.node.connect_to_peer(host, int(port))
            except Exception as e:
                logger.error(f"Failed to connect to peer: {e}")
        
        # Start the API server
        self.node.start_api_server()
        
        # Start mining
        self.node.start_mining(threads=self.mining_threads)
        
        logger.info(f"""
Mining node started!
    - Miner address: {self.miner_address}
    - Database: {self.db_name}
    - P2P Port: {self.p2p_port}
    - API Port: {self.api_port}
    - Dashboard URL: http://localhost:{self.api_port}/dashboard
        """)
        
    def stop(self):
        """Stop the mining process"""
        if self.node:
            logger.info("Stopping mining node...")
            self.node.stop()
            logger.info("Mining node stopped.") 