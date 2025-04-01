# Deployment Guide

This guide provides instructions for deploying the AI-Powered Intrusion Detection System in various environments.

## System Requirements

### Minimum Requirements
- Python 3.8 or higher
- 4GB RAM
- 2 CPU cores
- 10GB disk space

### Recommended Requirements
- Python 3.9 or higher
- 8GB RAM
- 4 CPU cores
- 20GB disk space
- GPU support for deep learning models

## Installation Options

### Standard Installation

```bash
# Clone the repository
git clone https://github.com/sabeekahamed/intruder-detection-system.git
cd ai-powered-ids

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Docker Installation

```bash
# Build the Docker image
docker build -t ai-powered-ids .

# Run the container
docker run -p 8050:8050 -v /path/to/pcaps:/app/data ai-powered-ids
```

## Deployment Scenarios

### 1. Standalone Monitoring Station

Ideal for small networks or testing environments.

```bash
# Run in detection mode with a PCAP file
aipids --mode detect --data /path/to/capture.pcap --output_path results

# Run in live monitoring mode
aipids --mode detect --live --interface eth0 --output_path results
```

### 2. Integration with Existing SIEM

```bash
# Run with SIEM integration
aipids --mode detect --live --interface eth0 --siem-forward --siem-url http://siem.example.com/api/events --siem-token YOUR_API_TOKEN
```

### 3. Distributed Deployment

For large-scale networks, deploy multiple sensors feeding into a central analysis server.

#### Sensor Configuration
```bash
# Run in sensor mode
aipids --mode sensor --interface eth0 --server http://central.example.com:5000
```

#### Central Server Configuration
```bash
# Run in server mode
aipids --mode server --port 5000 --output_path /var/log/ids
```

## Network Configuration

### Packet Capture Requirements

- For inline detection: Configure port mirroring/SPAN on your network switch
- For passive monitoring: Connect to a network TAP device

### Network Access Control

Ensure the system has permission to:
1. Read network traffic from specified interfaces
2. Send alerts (email, HTTP, etc.)
3. Execute automatic responses if configured

## Tuning and Optimization

### Detection Threshold

Adjust the detection threshold based on your environment's needs:
- Lower threshold (e.g., 0.6): More sensitive, higher false positive rate
- Higher threshold (e.g., 0.9): Less sensitive, lower false positive rate

```bash
# Example with adjusted threshold
aipids --mode detect --data capture.pcap --threshold 0.75
```

### Model Selection

Choose the appropriate model based on your requirements:
- Standard model: Balanced performance
- Deep learning model: Higher accuracy but more resource-intensive

```bash
# Using the deep learning model
aipids --mode deep_learning --data capture.pcap
```

## Maintenance

### Model Updates

Regularly update the detection models with new training data:

```bash
# Retrain model with new data
aipids --mode train --data new_training_data.csv --model models/updated_model.pkl
```

### Log Rotation

Configure log rotation to manage disk space:

```bash
# Example logrotate configuration
cat > /etc/logrotate.d/ai-powered-ids << EOF
/var/log/ai-powered-ids/*.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    create 640 root adm
}
EOF
```

## Security Considerations

1. **System Access**: Secure the IDS platform with proper authentication
2. **API Protection**: Use API keys/tokens for integrations
3. **Data Protection**: Encrypt sensitive data at rest
4. **Update Management**: Keep the system and dependencies updated

## Troubleshooting

### Common Issues

1. **Missing Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Permission Issues**:
   ```bash
   # For network capture issues
   sudo setcap cap_net_raw,cap_net_admin=eip /path/to/python
   ```

3. **Performance Problems**:
   - Reduce capture resolution
   - Increase sampling rate
   - Upgrade hardware or optimize code

### Logging

Enable detailed logging for troubleshooting:

```bash
aipids --mode detect --data capture.pcap --log-level DEBUG
```

## Backup and Recovery

### Configuration Backup

Regularly back up your configuration and models:

```bash
# Backup script example
backup_dir="/backup/ai-powered-ids/$(date +%Y%m%d)"
mkdir -p "$backup_dir"
cp -r models/ "$backup_dir/"
cp -r config/ "$backup_dir/"
```

### Disaster Recovery

In case of system failure:
1. Reinstall the application
2. Restore models and configuration from backup
3. Verify system functionality with test data