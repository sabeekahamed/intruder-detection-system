import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os
def visualize_results(ids, results_df, output_path='visualization'):
    """
    Visualize the results of the IDS
    """
    os.makedirs(output_path, exist_ok=True)
    # Set up the style
    plt.style.use('ggplot')
    # Visualize attack distribution
    plt.figure(figsize=(12, 6))
    attack_counts = results_df['prediction'].value_counts()
    attack_counts.plot(kind='bar', color='darkred')
    plt.title('Distribution of Detected Attacks')
    plt.xlabel('Attack Type')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, 'attack_distribution.png'))
    plt.close()
    # Visualize anomaly scores
    plt.figure(figsize=(12, 6))
    sns.histplot(results_df['anomaly_score'], bins=50, kde=True)
    plt.title('Distribution of Anomaly Scores')
    plt.xlabel('Anomaly Score')
    plt.ylabel('Count')
    plt.axvline(0.8, color='red', linestyle='--', label='Alert Threshold')
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, 'anomaly_scores.png'))
    plt.close()
    # Time series of alerts
    if 'timestamp' in results_df.columns:
        plt.figure(figsize=(14, 7))
        results_df['timestamp'] = pd.to_datetime(results_df['timestamp'])
        results_df.set_index('timestamp', inplace=True)
        # Resample to hourly data
        hourly_alerts = results_df['anomaly_score'].resample('H').count()
        hourly_alerts.plot(marker='o', color='darkblue')
        plt.title('Alerts Over Time')
        plt.xlabel('Time')
        plt.ylabel('Number of Alerts')
        plt.tight_layout()
        plt.savefig(os.path.join(output_path, 'alerts_timeline.png'))
        plt.close()
    # Feature importance
    if ids.model and hasattr(ids.model, 'feature_importances_'):
        plt.figure(figsize=(12, 10))
        importances = ids.model.feature_importances_
        if ids.features:
            indices = np.argsort(importances)[::-1]
            feature_names = np.array(ids.features)[indices]
            importances = importances[indices]
            plt.barh(range(len(indices)), importances, align='center')
            plt.yticks(range(len(indices)), feature_names)
            plt.title('Feature Importance')
            plt.xlabel('Relative Importance')
            plt.tight_layout()
            plt.savefig(os.path.join(output_path, 'feature_importance.png'))
            plt.close()
    print(f"Visualizations saved to {output_path}")