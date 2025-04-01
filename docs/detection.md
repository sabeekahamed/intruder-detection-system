# Detection Capabilities

This document outlines the various types of network intrusions that the AI-Powered IDS can detect.

## Attack Categories

### 1. Denial of Service (DoS) Attacks

The system can detect various DoS attacks that attempt to overwhelm network resources:

#### Neptune SYN Flood
- **Description**: TCP SYN flooding attack that exhausts server connection resources
- **Detection Method**: Identifies abnormal patterns of SYN packets without corresponding ACK packets
- **Example Alert**:
  ```
  CRITICAL: DoS attack detected (Neptune SYN Flood)
  Source: 23.45.67.89, Target: 192.168.1.10, Score: 0.97
  ```

#### UDP Flood
- **Description**: Overwhelming the target with UDP packets
- **Detection Method**: Volumetric analysis of UDP traffic to identify abnormal patterns

#### ICMP Flood
- **Description**: Ping-based flood attack
- **Detection Method**: Statistical analysis of ICMP packet frequency and size

### 2. Probe and Reconnaissance

Detection of network scanning and information gathering:

#### Port Scanning
- **Description**: Systematic probing of port ranges to identify services
- **Detection Method**: Detection of sequential or distributed port connection attempts
- **Example Alert**:
  ```
  HIGH: Port scanning detected
  Source: 183.76.129.42, Target: 192.168.1.0/24, Score: 0.89
  ```

#### Host Discovery
- **Description**: Attempts to identify active hosts on the network
- **Detection Method**: Pattern recognition of ping sweeps and ARP scans

#### Service Enumeration
- **Description**: Attempts to identify running services and versions
- **Detection Method**: Detection of banner grabbing and version probing

### 3. Unauthorized Access

Detection of attempts to gain unauthorized access to systems:

#### Brute Force Attacks
- **Description**: Multiple login attempts with different credentials
- **Detection Method**: Statistical analysis of authentication failures
- **Example Alert**:
  ```
  HIGH: Brute Force SSH Attack Detected
  Source: 45.67.89.12, Target: 192.168.1.15:22, Score: 0.86
  ```

#### Password Spraying
- **Description**: Testing a common password against many accounts
- **Detection Method**: Correlation of authentication attempts across accounts

#### Session Hijacking
- **Description**: Stealing or manipulating session tokens
- **Detection Method**: Detection of abnormal session behavior

### 4. Malware and Exploitation

Detection of malicious code execution attempts:

#### Shellcode Injection
- **Description**: Injection of executable code into vulnerable processes
- **Detection Method**: Deep packet inspection and payload analysis
- **Example Alert**:
  ```
  CRITICAL: Shellcode injection attempt detected
  Source: 183.76.129.42, Target: 192.168.1.25:8080, Score: 0.95
  ```

#### Buffer Overflow
- **Description**: Exploits that overflow memory buffers to execute code
- **Detection Method**: Pattern matching and anomaly detection in packet payloads

#### Command Injection
- **Description**: Insertion of OS commands into application parameters
- **Detection Method**: Detection of suspicious command patterns

### 5. Data Exfiltration

Detection of unauthorized data transfer:

#### DNS Tunneling
- **Description**: Using DNS queries for covert data transfer
- **Detection Method**: Statistical analysis of DNS query patterns
- **Example Alert**:
  ```
  MEDIUM: Possible DNS tunneling detected
  Source: 192.168.1.50, Target: external DNS, Score: 0.82
  ```

#### Unusual Data Transfers
- **Description**: Abnormal volume or timing of data transfers
- **Detection Method**: Baseline comparison of data transfer patterns

#### Encrypted Channel Misuse
- **Description**: Using encrypted channels to hide data exfiltration
- **Detection Method**: Traffic analysis and behavioral indicators

## Detection Methods

### 1. Signature-Based Detection

Used for known attack patterns:
- Pre-defined signatures for common attacks
- Regular expression matching
- Protocol violation detection

### 2. Anomaly-Based Detection

Used for unknown or variant attacks:
- Statistical deviation from normal behavior
- Outlier detection algorithms
- Time-series analysis

### 3. Machine Learning Techniques

Specific ML approaches employed:
- **Random Forest**: For general classification of network traffic
- **Isolation Forest**: For detecting outliers in network behavior
- **LSTM Networks**: For analyzing temporal patterns in traffic
- **Autoencoders**: For unsupervised anomaly detection

## Alert Severity Levels

The system categorizes alerts by severity:

| Level | Score Range | Description |
|-------|------------|-------------|
| CRITICAL | 0.90 - 1.00 | Immediate threat requiring urgent action |
| HIGH | 0.80 - 0.89 | Significant threat requiring prompt attention |
| MEDIUM | 0.70 - 0.79 | Potential threat requiring investigation |
| LOW | 0.60 - 0.69 | Suspicious activity warranting monitoring |
| INFO | < 0.60 | Informational, possibly benign anomaly |

## False Positive Mitigation

Techniques used to reduce false positives:

1. **Context-aware classification**: Considering network context before alerting
2. **Alert correlation**: Grouping related alerts to identify true threats
3. **Baseline adaptation**: Adjusting to normal network behavior over time
4. **Threshold tuning**: Customizing detection thresholds by network segment
