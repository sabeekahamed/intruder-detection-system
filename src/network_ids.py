# network_ids.py
import pickle
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import os
import jinja2

class NetworkIDS:
    """Network Intrusion Detection System using machine learning."""
    
    def __init__(self, model_path=None):
        """Initialize the NetworkIDS.
        
        Args:
            model_path: Path to a pre-trained model file (optional)
        """
        self.model = None
        self.alert_log = []
        
        if model_path:
            self.load_model(model_path)
    
    def train(self, data_path, model_path=None):
        """Train the IDS model on the provided dataset.
        
        Args:
            data_path: Path to the training data CSV
            model_path: Path to save the trained model (optional)
        """
        print(f"Loading training data from {data_path}...")
        data = pd.read_csv(data_path)
        
        # Extract features (you may need to customize this)
        X = self._prepare_data(data)
        
        print("Training Isolation Forest model...")
        # Using Isolation Forest for anomaly detection
        self.model = IsolationForest(
            n_estimators=100,
            max_samples='auto',
            contamination=0.1,
            random_state=42
        )
        self.model.fit(X)
        
        if model_path:
            self._save_model(model_path)
            print(f"Model saved to {model_path}")
    
    def detect(self, data):
        """Detect anomalies in the provided data.
        
        Args:
            data: DataFrame containing network traffic data
            
        Returns:
            Tuple of (predictions, anomaly_scores)
        """
        if self.model is None:
            raise ValueError("Model not trained or loaded. Train or load a model first.")
        
        X = self._prepare_data(data)
        
        # Get anomaly scores (-1 for anomalies, 1 for normal)
        predictions_raw = self.model.predict(X)
        
        # Convert to binary classification (1 for anomaly, 0 for normal)
        predictions = np.where(predictions_raw == -1, 1, 0)
        
        # Get decision scores (higher is more anomalous)
        scores = self.model.decision_function(X)
        # Invert so higher score = more anomalous
        scores = -scores
        
        return predictions, scores
    
    def _prepare_data(self, data):
        """Prepare data for model training or prediction.
        
        This is a simplified version. In a real IDS, you would implement
        more sophisticated feature engineering.
        """
        # Get only numeric columns for this example
        numeric_data = data.select_dtypes(include=[np.number])
        
        # Fill missing values
        numeric_data = numeric_data.fillna(0)
        
        return numeric_data
    
    def _save_model(self, model_path):
        """Save the trained model to disk."""
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        with open(model_path, 'wb') as f:
            pickle.dump(self.model, f)
    
    def load_model(self, model_path):
        """Load a trained model from disk."""
        with open(model_path, 'rb') as f:
            self.model = pickle.load(f)
        print(f"Model loaded from {model_path}")
    
    def generate_report(self, output_path):
        """Generate an HTML report of detected intrusions."""
        # Simple Jinja2 template for the report
        template_str = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Intrusion Detection Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                h1 { color: #333; }
                table { border-collapse: collapse; width: 100%; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
                tr:nth-child(even) { background-color: #f9f9f9; }
                .alert-high { background-color: #ffcccc; }
                .alert-medium { background-color: #ffffcc; }
            </style>
        </head>
        <body>
            <h1>Intrusion Detection System Report</h1>
            <p>Generated on: {{ current_time }}</p>
            
            <h2>Alert Summary</h2>
            <p>Total alerts: {{ alerts|length }}</p>
            
            <h2>Alert Details</h2>
            <table>
                <tr>
                    <th>Timestamp</th>
                    <th>Type</th>
                    <th>Score</th>
                </tr>
                {% for alert in alerts %}
                <tr class="{{ 'alert-high' if alert.score > 0.9 else 'alert-medium' }}">
                    <td>{{ alert.timestamp }}</td>
                    <td>{{ alert.prediction }}</td>
                    <td>{{ "%.3f"|format(alert.score) }}</td>
                </tr>
                {% endfor %}
            </table>
        </body>
        </html>
        """
        
        # Create the report directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Render the template with data
        from datetime import datetime
        template = jinja2.Template(template_str)
        html_content = template.render(
            current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            alerts=self.alert_log
        )
        
        # Write the HTML report
        with open(output_path, 'w') as f:
            f.write(html_content)
        
        print(f"Report generated at {output_path}")