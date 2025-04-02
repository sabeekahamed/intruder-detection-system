import argparse
import pandas as pd
import os
from datetime import datetime

# Changed imports to avoid circular reference
# Import these modules only when needed, not at the top level
# from data_loader import download_dataset
# from feature_engineering import extract_features
# from visualization import visualize_results
# from deeplearning_model import create_deep_learning_ids

# This should be a separate file containing the NetworkIDS class
# NetworkIDS should NOT be imported from ids_module.py

def main():
    """Main function to run the AI-Powered Intrusion Detection System."""
    # Import needed modules here to avoid circular imports
    from network_ids import NetworkIDS  # Assuming NetworkIDS is now in network_ids.py
    from data_loader import download_dataset
    from feature_engineering import extract_features
    from visualization import visualize_results
    from deeplearning_model import create_deep_learning_ids
    
    parser = argparse.ArgumentParser(description='AI-Powered Intrusion Detection System')
    parser.add_argument('--mode', choices=['train', 'detect', 'demo', 'deep_learning'], default='demo',
                        help='Mode of operation: train, detect, demo, or deep_learning')
    parser.add_argument('--data', type=str, help='Path to the dataset or PCAP file')
    parser.add_argument('--model', type=str, default='models/ids_model.pkl', help='Path to the model file')
    parser.add_argument('--threshold', type=float, default=0.8, help='Alert threshold')
    parser.add_argument('--output_path', type=str, default='results', help='Path to save results (reports, visualizations)')
    args = parser.parse_args()
    
    # Create output directory
    os.makedirs(args.output_path, exist_ok=True)
    
    if args.mode == 'train':
        if not args.data:
            print("Error: --data parameter is required for training mode")
            return 1  # Use return instead of exit for better practice
        ids = NetworkIDS()
        ids.train(args.data, args.model)
    
    elif args.mode == 'detect':
        if not args.data:
            print("Error: --data parameter is required for detection mode")
            return 1
            
        ids = NetworkIDS(args.model)
        if args.data.endswith('.pcap') or args.data.endswith('.pcapng'):
            # Feature extraction from PCAP
            traffic_data = extract_features(args.data)
            if traffic_data is None:
                print("Error: Feature extraction failed. Ensure scapy is installed and the PCAP file is valid.")
                return 1
        elif args.data.endswith('.csv'):
            traffic_data = pd.read_csv(args.data)
        else:
            print("Error: Invalid data format. Must be CSV or PCAP.")
            return 1
            
        # Fixed: Call detect instead of monitor_traffic which isn't defined in NetworkIDS
        predictions, scores = ids.detect(traffic_data)
        
        # Create a dataframe with predictions to check for alerts
        alerts_df = pd.DataFrame({
            'prediction': predictions,
            'anomaly_score': scores
        })
        alerts = alerts_df[alerts_df['anomaly_score'] >= args.threshold]
        
        if not alerts.empty:
            print(f"Found {len(alerts)} alerts")
            # Add alerts to ids.alert_log for reporting
            for i in range(len(alerts)):
                alert_info = {
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'prediction': alerts.iloc[i]['prediction'],
                    'score': alerts.iloc[i]['anomaly_score'],
                    'details': {}  # Add relevant details if available
                }
                ids.alert_log.append(alert_info)
                
            report_path = os.path.join(args.output_path, 'intrusion_report.html')
            ids.generate_report(report_path)
        else:
            print("No alerts found")
    
    elif args.mode == 'demo':
        run_demo(args.output_path)
    
    elif args.mode == 'deep_learning':
        if not args.data:
            print("Error: --data parameter is required for deep learning mode")
            return 1
        create_deep_learning_ids(args.data, args.model, args.output_path)
    
    return 0  # Successful execution

def run_demo(output_path):
    """Run a demonstration of the IDS system."""
    # Import needed modules only when function is called
    from network_ids import NetworkIDS
    from data_loader import download_dataset
    from visualization import visualize_results
    
    print("=" * 50)
    print("AI-Powered Intrusion Detection System Demo")
    print("=" * 50)
    
    # Check if datasets directory exists
    if not os.path.exists('datasets'):
        os.makedirs('datasets')
    
    # Download dataset if not available
    nsl_kdd_train = 'datasets/nsl-kdd_train.csv'
    nsl_kdd_test = 'datasets/nsl-kdd_test.csv'
    
    if not (os.path.exists(nsl_kdd_train) and os.path.exists(nsl_kdd_test)):
        print("Downloading NSL-KDD dataset...")
        try:
            nsl_kdd_train, nsl_kdd_test = download_dataset('nsl-kdd', 'datasets')
        except Exception as e:
            print(f"Error downloading dataset: {e}")
            print("Please download the dataset manually and place it in the 'datasets' directory.")
            return
    
    # Create and train the IDS
    ids = NetworkIDS()
    
    # Check if model already exists
    model_path = 'models/ids_model.pkl'
    if not os.path.exists('models'):
        os.makedirs('models')
    
    if os.path.exists(model_path):
        print("Loading existing model...")
        ids.load_model(model_path)
    else:
        print("Training new model...")
        ids.train(nsl_kdd_train, model_path)
    
    # Run detection on test data
    print("\nRunning detection on test data...")
    test_data = pd.read_csv(nsl_kdd_test)
    predictions, scores = ids.detect(test_data)
    
    # Display results
    results_df = test_data.copy()
    results_df['prediction'] = predictions
    results_df['anomaly_score'] = scores
    
    print("\nTop 5 detected anomalies:")
    top_anomalies = results_df.sort_values('anomaly_score', ascending=False).head(5)
    print(top_anomalies[['prediction', 'anomaly_score']])
    
    # Visualize results
    print("\nVisualizing results...")
    visualize_results(ids, results_df, output_path)
    
    # Generate report
    print("\nGenerating report...")
    # Add some timestamps for the report
    for i in range(len(top_anomalies)):
        alert_info = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'prediction': top_anomalies.iloc[i]['prediction'],
            'score': top_anomalies.iloc[i]['anomaly_score'],
            'details': top_anomalies.iloc[i].to_dict()
        }
        ids.alert_log.append(alert_info)
    
    report_path = os.path.join(output_path, 'demo_report.html')
    ids.generate_report(report_path)
    
    print(f"\nDemo completed. Check the '{output_path}' directory for result visualizations and report.")

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)