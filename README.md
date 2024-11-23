# PhantomFirewall

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Documentation Status](https://readthedocs.org/projects/phantomfirewall/badge/?version=latest)](https://phantomfirewall.readthedocs.io)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Coverage Status](https://coveralls.io/repos/github/yourusername/phantomfirewall/badge.svg?branch=main)](https://coveralls.io/github/yourusername/phantomfirewall?branch=main)

An intelligent, adaptive firewall system that leverages machine learning to provide dynamic traffic filtering based on user behavior patterns and real-time threat intelligence.

## 📋 Table of Contents

- [Features](#features)
- [System Architecture](#system-architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Dashboard](#dashboard)
- [Machine Learning](#machine-learning)
- [Threat Intelligence](#threat-intelligence)
- [Performance Tuning](#performance-tuning)
- [Security Considerations](#security-considerations)
- [Contributing](#contributing)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## 🚀 Features

### Core Features
- **Adaptive Traffic Analysis**: Real-time traffic pattern learning and anomaly detection
- **Machine Learning Integration**: Behavioral analysis and predictive blocking
- **Real-time Threat Intelligence**: Integration with multiple threat feeds
- **Custom Rule Engine**: Flexible rule creation with priority-based processing
- **Performance Optimization**: Minimal system impact with efficient packet processing
- **Web Dashboard**: Real-time monitoring and configuration interface
- **REST API**: Comprehensive API for integration and automation
- **Detailed Logging**: Customizable logging with multiple output formats

### Advanced Capabilities
- Automatic rule generation based on learned patterns
- Integration with popular threat intelligence platforms
- Custom ML model training for specific use cases
- Traffic pattern visualization and analysis
- Automated response to detected threats
- Role-based access control for multi-user environments

## 🏗 System Architecture

### Component Overview

```
PhantomFirewall/
├── core/
│   ├── engine.py         # Main firewall engine
│   ├── ml_module.py      # Machine learning components
│   ├── threat_intel.py   # Threat intelligence integration
│   └── config_manager.py # Configuration management
├── api/
│   └── server.py         # REST API implementation
├── dashboard/
│   └── src/             # Web dashboard interface
├── tests/               # Test suite
└── docs/               # Documentation
```

### Key Components

1. **Core Engine**: 
   - Packet interception and processing
   - Rule evaluation and enforcement
   - Traffic flow management

2. **ML Module**:
   - Traffic pattern analysis
   - Anomaly detection
   - Behavioral learning

3. **Threat Intelligence**:
   - Multiple feed integration
   - Real-time updates
   - Threat scoring

4. **API Server**:
   - RESTful endpoints
   - Authentication
   - Rate limiting

5. **Dashboard**:
   - Real-time monitoring
   - Configuration interface
   - Visualization

## 📥 Installation

### Prerequisites

- Python 3.8 or higher
- Linux operating system (Ubuntu 20.04+ recommended)
- NetFilter queue support
- Node.js 14+ (for dashboard)

### Quick Install

```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install -y python3-dev libnetfilter-queue-dev

# Clone the repository
git clone https://github.com/tejaschaudhari131/PhantomFirewall
cd PhantomFirewall

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -e .

# Install dashboard dependencies
cd dashboard
npm install
npm run build
cd ..
```

### Docker Installation

```bash
# Build Docker image
docker build -t phantomfirewall .

# Run container
docker run -d \
  --name phantomfirewall \
  --network host \
  --cap-add NET_ADMIN \
  -v /path/to/config:/app/config \
  phantomfirewall
```

## ⚙️ Configuration

### Basic Configuration

Create `config/config.yaml`:

```yaml
# Core Configuration
mode: adaptive
learning_rate: 0.01
update_interval: 3600
log_level: INFO

# Network Settings
api_port: 8080
dashboard_port: 3000

# ML Configuration
ml_settings:
  window_size: 1000
  contamination: 0.1
  feature_set: extended

# Threat Intelligence
threat_feeds:
  - name: alienvault
    enabled: true
    api_key: YOUR_API_KEY
    update_interval: 3600
  - name: abuseipdb
    enabled: true
    api_key: YOUR_API_KEY
    update_interval: 7200
```

### Rule Configuration

Example rules in `config/rules.yaml`:

```yaml
rules:
  - name: "Block Known Malicious"
    priority: 1
    action: DROP
    source: threat_intel

  - name: "Allow HTTPS"
    priority: 2
    protocol: TCP
    port: 443
    action: ACCEPT

  - name: "Rate Limit SSH"
    priority: 3
    protocol: TCP
    port: 22
    action: LIMIT
    rate: "10/minute"
```

## 🎮 Usage

### Command Line Interface

```bash
# Start the firewall
phantom-firewall start

# View status
phantom-firewall status

# Add a rule
phantom-firewall rule add \
  --name "Block IP" \
  --action DROP \
  --source-ip "192.168.1.100"

# Update configuration
phantom-firewall config set \
  --learning-rate 0.02 \
  --update-interval 1800

# View logs
phantom-firewall logs --level INFO
```

### API Usage

```python
import requests

# Create a new rule
response = requests.post(
    "http://localhost:8080/api/v1/rules",
    json={
        "name": "Block Range",
        "priority": 1,
        "action": "DROP",
        "source_ip": "192.168.1.0/24"
    }
)

# Get current status
status = requests.get("http://localhost:8080/api/v1/status").json()
```

## 🎯 API Reference

### Endpoints

#### Status
- `GET /api/v1/status` - Get firewall status
- `GET /api/v1/metrics` - Get performance metrics

#### Rules
- `GET /api/v1/rules` - List all rules
- `POST /api/v1/rules` - Create new rule
- `PUT /api/v1/rules/{id}` - Update rule
- `DELETE /api/v1/rules/{id}` - Delete rule

#### Threat Intelligence
- `GET /api/v1/threats` - Get threat data
- `POST /api/v1/threats/ip` - Add IP to blocklist

## 📊 Dashboard

### Features

- Real-time traffic monitoring
- Rule management interface
- Threat visualization
- Performance metrics
- Configuration management
- Log viewer

### Access

The dashboard is available at `http://localhost:3000` by default.

## 🧠 Machine Learning

### Model Architecture

- Isolation Forest for anomaly detection
- Feature extraction from packet headers
- Sliding window analysis
- Adaptive threshold adjustment

### Training Process

1. Initial data collection period
2. Feature extraction and normalization
3. Model training
4. Continuous learning from feedback

## 🛡 Threat Intelligence

### Supported Feeds

- AlienVault OTX
- AbuseIPDB
- Emerging Threats
- Custom feeds

### Integration

```python
from phantomfirewall import ThreatIntelligence

# Initialize threat intelligence
ti = ThreatIntelligence()

# Check IP
is_malicious = ti.check_ip("192.168.1.100")

# Add custom feed
ti.add_feed("custom_feed", "http://example.com/feed")
```

## ⚡ Performance Tuning

### Optimization Tips

1. Adjust window size for ML analysis
2. Configure appropriate update intervals
3. Use efficient rule ordering
4. Enable caching where appropriate
5. Optimize logging levels

### Resource Requirements

- CPU: 2+ cores recommended
- Memory: 2GB minimum
- Storage: 20GB+ for logs and ML data
- Network: Gigabit recommended

## 🔒 Security Considerations

### Best Practices

1. Regular updates of threat intelligence
2. Proper API authentication
3. Secure dashboard access
4. Regular log analysis
5. Backup of configurations

### Known Limitations

- Single node deployment
- Limited IPv6 support
- Resource intensive ML training

## 👥 Contributing

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Install development dependencies
4. Run tests
5. Submit pull request

### Testing

```bash
# Run unit tests
pytest tests/unit

# Run integration tests
pytest tests/integration

# Run performance tests
pytest tests/performance
```

## ❗ Troubleshooting

### Common Issues

1. **Connection Issues**
   ```bash
   # Check service status
   systemctl status phantomfirewall
   
   # View logs
   tail -f /var/log/phantomfirewall/error.log
   ```

2. **Performance Problems**
   ```bash
   # Monitor resource usage
   top -p $(pgrep -f phantomfirewall)
   
   # Check packet processing
   tcpdump -i any 'tcp port 8080'
   ```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📚 Additional Resources

- [Documentation](https://phantomfirewall.readthedocs.io/)
- [API Documentation](https://phantomfirewall.readthedocs.io/api/)
- [Contributing Guide](CONTRIBUTING.md)
- [Security Policy](SECURITY.md)
