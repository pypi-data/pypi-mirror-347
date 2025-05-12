# Fiducia Mining Client

A Python package for mining Fiducia blockchain.

## Installation

### From PyPI

```bash
pip install fiducia-miner
```

### From Source

```bash
git clone https://github.com/yourusername/fiducia-miner.git
cd fiducia-miner
pip install -e .
```

## Requirements

- Python 3.6+
- Git
- Internet connection

## Quick Start

After installation, you can run the miner using the command:

```bash
fiducia-miner --repo-url https://github.com/username/fiducia.git --miner-address YOUR_WALLET_ADDRESS
```

## Usage

```
usage: fiducia-miner [-h] --repo-url REPO_URL --miner-address MINER_ADDRESS
                     [--db DB] [--p2p-port P2P_PORT] [--api-port API_PORT]
                     [--connect-to CONNECT_TO] [--mining-threads MINING_THREADS]
                     [--clean]

Fiducia Blockchain Mining Client

options:
  -h, --help            show this help message and exit
  --repo-url REPO_URL   URL of the Fiducia repository
  --miner-address MINER_ADDRESS
                        Address to receive mining rewards
  --db DB               Database filename (default: mining.db)
  --p2p-port P2P_PORT   P2P port (default: 8333)
  --api-port API_PORT   API port (default: 8545)
  --connect-to CONNECT_TO
                        Connect to an existing node (format: host:port)
  --mining-threads MINING_THREADS
                        Number of mining threads
  --clean               Clean existing installation before setup
```

## Features

- Automatically clones the Fiducia repository
- Sets up the environment with all required dependencies
- Configures and starts a mining node
- Handles clean shutdowns when interrupted
- Dashboard access via web browser
- Connect to existing nodes or run standalone

## Examples

### Basic Mining

```bash
fiducia-miner --repo-url https://github.com/username/fiducia.git --miner-address 1A2B3C4D5E6F7G8H9I0J
```

### Mine with Custom Settings

```bash
fiducia-miner --repo-url https://github.com/username/fiducia.git \
            --miner-address 1A2B3C4D5E6F7G8H9I0J \
            --db custom_blockchain.db \
            --p2p-port 9000 \
            --api-port 9001 \
            --mining-threads 4
```

### Connect to Existing Node

```bash
fiducia-miner --repo-url https://github.com/username/fiducia.git \
            --miner-address 1A2B3C4D5E6F7G8H9I0J \
            --connect-to 192.168.1.100:8333
```

### Clean Installation

```bash
fiducia-miner --repo-url https://github.com/username/fiducia.git \
            --miner-address 1A2B3C4D5E6F7G8H9I0J \
            --clean
```

## Dashboard Access

Once the miner is running, access the dashboard at:
```
http://localhost:8545/dashboard
```
(Or whichever API port you specified with --api-port)

## Notes

- All mining rewards will be sent to the address specified with --miner-address
- The miner runs in the foreground by default; use Ctrl+C to stop
- To run in the background, consider using tools like `nohup`, `screen`, or `tmux`

## Development

To develop on this package:

```bash
git clone https://github.com/yourusername/fiducia-miner.git
cd fiducia-miner
pip install -e .
```

## License

This project is licensed under the MIT License - see the LICENSE file for details. 