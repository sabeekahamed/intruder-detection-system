import os
import requests
from tqdm import tqdm
import pandas as pd
def download_dataset(dataset_name, output_path='.'):
    """
    Download common network security datasets
    """
    datasets = {
        'nsl-kdd': {
            'train': 'https://raw.githubusercontent.com/defcom17/NSL_KDD/master/KDDTrain+.txt',
            'test': 'https://raw.githubusercontent.com/defcom17/NSL_KDD/master/KDDTest+.txt',
            'column_names': ['duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes',
                             'land', 'wrong_fragment', 'urgent', 'hot', 'num_failed_logins', 'logged_in',
                             'num_compromised', 'root_shell', 'su_attempted', 'num_root', 'num_file_creations',
                             'num_shells', 'num_access_files', 'num_outbound_cmds', 'is_host_login',
                             'is_guest_login', 'count', 'srv_count', 'serror_rate', 'srv_serror_rate',
                             'rerror_rate', 'srv_rerror_rate', 'same_srv_rate', 'diff_srv_rate',
                             'srv_diff_host_rate', 'dst_host_count', 'dst_host_srv_count',
                             'dst_host_same_srv_rate', 'dst_host_diff_srv_rate',
                             'dst_host_same_src_port_rate', 'dst_host_srv_diff_host_rate',
                             'dst_host_serror_rate', 'dst_host_srv_serror_rate',
                             'dst_host_rerror_rate', 'dst_host_srv_rerror_rate', 'label', 'difficulty']
        }
    }
    if dataset_name not in datasets:
        raise ValueError(f"Dataset {dataset_name} not found. Available datasets: {list(datasets.keys())}")
    dataset = datasets[dataset_name]
    # Create output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)
    # Download training data
    train_path = os.path.join(output_path, f"{dataset_name}_train.csv")
    test_path = os.path.join(output_path, f"{dataset_name}_test.csv")
    print(f"Downloading {dataset_name} training data...")
    response = requests.get(dataset['train'], stream=True)
    with open(train_path, 'wb') as f:
        for data in tqdm(response.iter_content(chunk_size=1024)):
            f.write(data)
    print(f"Downloading {dataset_name} test data...")
    response = requests.get(dataset['test'], stream=True)
    with open(test_path, 'wb') as f:
        for data in tqdm(response.iter_content(chunk_size=1024)):
            f.write(data)
    # Convert to CSV with column names
    train_df = pd.read_csv(train_path, header=None, names=dataset['column_names'])
    test_df = pd.read_csv(test_path, header=None, names=dataset['column_names'])
    # Save as CSV
    train_df.to_csv(train_path, index=False)
    test_df.to_csv(test_path, index=False)
    print(f"Dataset {dataset_name} downloaded and saved to {output_path}")
    return train_path, test_path
