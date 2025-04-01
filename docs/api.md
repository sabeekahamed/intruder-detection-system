# API Reference

This document provides detailed information about the API for the AI-Powered Intrusion Detection System.

## NetworkIDS Class

The main class for intrusion detection functionality.

### Initialization

```python
from ids import NetworkIDS

# Initialize with default settings
ids = NetworkIDS()

# Initialize with a pre-trained model
ids = NetworkIDS(model_path='models/ids_model.pkl')

# Initialize with custom settings
ids = NetworkIDS(
    model_path='models/custom_model.pkl',
    feature_set='extended',
    log_level='DEBUG'
)
```

### Methods

#### `train(data_path, model_output_path='models/ids_model.pkl')`

Train the IDS model using the provided dataset.

**Parameters:**
- `data_path` (str): Path to the training data CSV file
- `model_output_path` (str, optional): Path to save the trained model

**Returns:**
- `dict`: Training metrics including accuracy, precision, recall, and F1 score

**Example:**
```python
metrics = ids.train('datasets/training_data.csv', 'models/my_model.pkl')
print(f"Training accuracy: {metrics['accuracy']:.2f}")
```

#### `detect(data, threshold=0.8)`

Perform intrusion detection on the provided data.

**Parameters:**
- `data` (DataFrame): Pandas DataFrame containing network traffic data
- `threshold` (float, optional): Detection threshold (0.0 to 1.0)

**Returns:**
- `tuple`: (predictions, anomaly_scores)
  - `predictions` (array): Binary array indicating normal (0) or anomalous (1) traffic
  - `anomaly_scores` (array): Anomaly scores for each record

**Example:**
```python
import pandas as pd
traffic_data = pd.read_csv('datasets/traffic.csv')
predictions, scores = ids.detect(traffic_data, threshold=0.85)
```

#### `monitor_traffic(traffic_data, threshold=0.8)`

Monitor network traffic and generate alerts for detected intrusions.

**Parameters:**
- `traffic_data` (DataFrame): Pandas DataFrame containing network traffic data
- `threshold` (float, optional): Detection threshold (0.0 to 1.0)

**Returns:**
- `DataFrame`: DataFrame containing alert information

**Example:**
```python
alerts = ids.monitor_traffic(traffic_data, threshold=0.75)
if not alerts.empty:
    print(f"Found {len(alerts)} potential intrusions")
```

#### `generate_report(output_path)`

Generate an HTML report of detected intrusions.

**Parameters:**
- `output_path` (str): Path to save the generated report

**Returns:**
- `str`: Path to the generated report

**Example:**
```python
report_path = ids.generate_report('results/intrusion_report.html')
print(f"Report generated at {report_path}")
```

#### `load_model(model_path)`

Load a pre-trained model.

**Parameters:**
- `model_path` (str): Path to the model file

**Returns:**
- `bool`: True if successful, False otherwise

**Example:**
```python
success = ids.load_model('models/ids_model.pkl')
```

#### `save_model(model_path)`

Save the current model.

**Parameters:**
- `model_path` (str): Path to save the model

**Returns:**
- `bool`: True if successful, False otherwise

**Example:**
```python
success = ids.save_model('models/my_custom_model.pkl')
```

## Feature Engineering Module

Functions for extracting features from network traffic.

### `extract_features(pcap_path)`

Extract features from a PCAP file for intrusion detection.

**Parameters:**
- `pcap_path` (str): Path to the PCAP file

**Returns:**
- `DataFrame`: Pandas DataFrame containing extracted features

**Example:**
```python
from feature_engineering import extract_features
features_df = extract_features('captures/traffic.pcap')
```

### `normalize_features(features_df)`

Normalize features to improve model performance.

**Parameters:**
- `features_df` (DataFrame): DataFrame containing features

**Returns:**
- `DataFrame`: DataFrame with normalized features

**Example:**
```python
from feature_engineering import normalize_features
normalized_df = normalize_features(features_df)
```

## Visualization Module

Functions for visualizing detection results.

### `visualize_results(ids, results_df, output_path)`

Create visualizations of intrusion detection results.

**Parameters:**
- `ids` (NetworkIDS): IDS instance
- `results_df` (DataFrame): DataFrame containing detection results
- `output_path` (str): Directory to save visualizations

**Returns:**
- `list`: Paths to generated visualization files

**Example:**
```python
from visualization import visualize_results
viz_files = visualize_results(ids, results_df, 'results/visualizations')
```

### `generate_network_map(traffic_data, alerts, output_path)`

Generate a network topology map showing intrusion paths.

**Parameters:**
- `traffic_data` (DataFrame): Traffic data
- `alerts` (DataFrame): Alert data
- `output_path` (str): Path to save the network map

**Returns:**
- `str`: Path to the generated network map

**Example:**
```python
from visualization import generate_network_map
map_path = generate_network_map(traffic_data, alerts, 'results/network_map.html')
```

## Deep Learning Module

Functions for deep learning-based intrusion detection.

### `create_deep_learning_ids(data_path, model_output_path, output_path)`

Create and train a deep learning-based IDS.

**Parameters:**
- `data_path` (str): Path to the training data
- `model_output_path` (str): Path to save the model
- `output_path` (str): Path to save training results

**Returns:**
- `dict`: Training metrics and model information

**Example:**
```python
from deep_learning_model import create_deep_learning_ids
metrics = create_deep_learning_ids(
    'datasets/training_data.csv',
    'models/dl_model.h5',
    'results/dl_training'
)
```

## Data Loader Module

Functions for loading and preprocessing datasets.

### `download_dataset(dataset_name, output_dir)`

Download a dataset for training or testing.

**Parameters:**
- `dataset_name` (str): Name of the dataset ('nsl-kdd', 'cicids2017', etc.)
- `output_dir` (str): Directory to save the dataset

**Returns:**
- `tuple`: Paths to the training and testing datasets

**Example:**
```python
from data_loader import download_dataset
train_path, test_path = download_dataset('nsl-kdd', 'datasets')
```