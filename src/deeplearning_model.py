import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib
import matplotlib.pyplot as plt
def create_deep_learning_ids(data_path, model_save_path='models/dl_ids_model.h5', output_path='results'):
"""
Create a deep learning based IDS using TensorFlow
"""
try:
    import tensorflow as tf
    from tensorflow.keras.models import Sequential, load_model
    from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
    from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
except ImportError:
    print("TensorFlow not installed. Install it using 'pip install tensorflow'")
    return None
print("Creating deep learning based IDS...")
# Load and preprocess data
data = pd.read_csv(data_path)
# Separate features and labels
if 'label' in data.columns:
    target_col = 'label'
elif 'class' in data.columns:
    target_col = 'class'
else:
    raise ValueError("No target column found in the dataset")
# Handle categorical features
categorical_cols = data.select_dtypes(include=['object']).columns
for col in categorical_cols:
    le = LabelEncoder()
    data[col] = le.fit_transform(data[col])
# Extract features and target
X = data.drop([target_col], axis=1)
y = data[target_col]
# Handle missing values
X = X.fillna(0)
# Apply feature scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
# Split data
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)
# Create directory for model if it doesn't exist
os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
# Build the model
input_dim = X_train.shape[1]
model = Sequential([
    Dense(256, activation='relu', input_dim=input_dim),
    BatchNormalization(),
    Dropout(0.3),
    Dense(128, activation='relu'),
    BatchNormalization(),
    Dropout(0.3),
    Dense(64, activation='relu'),
    BatchNormalization(),
    Dropout(0.3),
    Dense(32, activation='relu'),
    BatchNormalization(),
    Dense(1, activation='sigmoid')
])
# Compile the model
model.compile(optimizer='adam',
                loss='binary_crossentropy',
                metrics=['accuracy'])
# Set up callbacks
early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
model_checkpoint = ModelCheckpoint(model_save_path, save_best_only=True)
# Train the model
history = model.fit(
    X_train, y_train,
    epochs=50,
    batch_size=64,
    validation_split=0.2,
    callbacks=[early_stopping, model_checkpoint],
    verbose=1
)
# Evaluate the model
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f"Test accuracy: {test_accuracy:.4f}")
# Plot training history
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Model Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(output_path, 'dl_ids_training_history.png'))
plt.close()
# Save preprocessing components
preprocessing = {
    'scaler': scaler,
    'features': X.columns.tolist()
}
preprocessing_path = os.path.join(os.path.dirname(model_save_path), 'preprocessing.pkl')
joblib.dump(preprocessing, preprocessing_path)
print(f"Deep learning model saved to {model_save_path}")
print(f"Preprocessing components saved to {preprocessing_path}")
return model