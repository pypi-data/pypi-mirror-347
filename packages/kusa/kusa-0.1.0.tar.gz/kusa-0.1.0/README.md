
# Kusa SDK 🛡️

**Securely access, preprocess, and train machine learning models on datasets from the Kusa platform.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) <!-- Ensure you have an MIT LICENSE file -->
<!-- [![PyPI version](https://badge.fury.io/py/kusa.svg)](https://badge.fury.io/py/kusa) -->
<!-- [![Python Version](https://img.shields.io/pypi/pyversions/kusa.svg)](https://pypi.org/project/kusa/) -->
<!-- Add above badges once published to PyPI and update links -->

The Kusa SDK empowers users of the Kusa dataset platform to leverage purchased or proprietary datasets for machine learning tasks. It provides a secure mechanism for data transfer and allows for client-side preprocessing and model training using popular frameworks like Scikit-learn, TensorFlow, and PyTorch. The SDK fetches data in encrypted batches, with decryption handled client-side.

**Current Status: Beta**
This SDK is currently in Beta, developed as a university final project. We appreciate your feedback and bug reports to help us improve!

## ✨ Features

*   **Secure Data Access:** Authenticate with your Kusa platform credentials (`PUBLIC_ID` and `SECRET_KEY`).
*   **Automated Full Dataset Fetching:** Retrieves the entire dataset by making batched, encrypted transfers. The SDK internally uses a portion of your `SECRET_KEY` to manage the decryption of these batches.
*   **Flexible Preprocessing:** Configure a comprehensive preprocessing pipeline including tokenization (NLTK, spaCy), stopword removal, lemmatization, numerical scaling, and dimensionality reduction (TF-IDF, PCA).
*   **Multi-Framework Training:** Bring your own training logic! The SDK seamlessly integrates with Scikit-learn, TensorFlow, and PyTorch.
*   **Model Management:** Save your trained models (which include preprocessing transformers) and load them later for inference.
*   **Client-Side Privacy Focus:** Data is decrypted in client memory for processing. The SDK attempts to clear raw data references after preprocessing to minimize exposure during the training phase. (See "Security Considerations" for more details).

## ⚙️ Installation

Ensure you have Python 3.7+ installed.

1.  **Install the Kusa SDK:**
    ```bash
    pip install kusa
    ```
    *(Once published. For now, you might install from a local wheel or source).*

2.  **Install ML Frameworks & Core Libraries:**
    The SDK has core dependencies. For ML model training, you'll need to install your chosen framework(s).

    *   **Core Libraries (Installed with `kusa` via `setup.py`):**
        `requests`, `pandas`, `cryptography`, `numpy`, `nltk`, `joblib`, `scikit-learn`, `python-dotenv`
    *   **For TensorFlow support (Optional):**
        ```bash
        pip install 'kusa[tensorflow]'
        # or simply: pip install tensorflow
        ```
    *   **For PyTorch support (Optional):**
        ```bash
        pip install 'kusa[pytorch]'
        # or simply: pip install torch torchvision
        ```
    *   **To install all supported ML extras with Kusa:**
        ```bash
        pip install 'kusa[all_ml]'
        ```
    *   For running the example visualization code, you'll also need:
        ```bash
        pip install seaborn matplotlib
        ```

## 🚀 Quick Start: Training a Model

Here's a typical workflow for training a model using the Kusa SDK.

**1. Setup Environment Variables:**

Create a `.env` file in your project's root directory:

```ini
# .env
PUBLIC_ID="your_dataset_public_id_from_kusa_platform"
SECRET_KEY="your_personal_secret_key_from_kusa_platform" 
# Ensure your SECRET_KEY is sufficiently long (e.g., at least 32 characters if the SDK uses the first 32 bytes for encryption).
# Keep this secure!

# Optional: If your SDK's Config class uses BASE_URL from env
# BASE_URL="http://your_kusa_server_api_endpoint" 
```

*   **`PUBLIC_ID`**: The public identifier for the dataset you wish to access.
*   **`SECRET_KEY`**: Your personal secret API key. The Kusa SDK will internally use a portion of this key for cryptographic operations related to batch decryption. **It is paramount that you keep your `SECRET_KEY` confidential.**

Load these variables in your Python script:

```python
# At the beginning of your script (e.g., main.py)
import os
from dotenv import load_dotenv

load_dotenv(override=True) # Loads variables from .env
```

**2. Example Training Script (`main.py`):**

This script demonstrates initializing the SDK, fetching the entire dataset, preprocessing, training a model, evaluating, and saving it.

```python
import os
from dotenv import load_dotenv
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
from inspect import signature
from sklearn.metrics import classification_report, confusion_matrix, precision_recall_curve, average_precision_score, f1_score
from sklearn.ensemble import RandomForestClassifier 
from kusa.client import SecureDatasetClient 
import tensorflow as tf
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader
import numpy as np

# --- Configuration ---
TRAINING_FRAMEWORK = "sklearn"  # Options: "sklearn", "tensorflow", "pytorch"
TARGET_COLUMN = "RainTomorrow"    # Replace with your dataset's target column

# --- Load Environment Variables ---
load_dotenv(override=True)
PUBLIC_ID = os.getenv("PUBLIC_ID")
SECRET_KEY = os.getenv("SECRET_KEY")

# --- Framework-aware training factory (Helper Function) ---
# (This function helps create model training functions for different frameworks)
def train_model_factory(framework="sklearn", model_class=None, fixed_params=None):
    fixed_params = fixed_params or {}
    if framework == "sklearn":
        def train_model(X, y, X_val=None, y_val=None, **params):
            sig = signature(model_class.__init__)
            accepted = set(sig.parameters.keys())
            valid_params = {k: v for k, v in {**fixed_params, **params}.items() if k in accepted}
            model = model_class(**valid_params)
            model.fit(X, y) # Sklearn fit doesn't typically use X_val, y_val directly
            return model
        return train_model

    elif framework == "tensorflow":
        def train_model(X, y, X_val=None, y_val=None, **params):
            model = tf.keras.Sequential([
                tf.keras.layers.Input(shape=(X.shape[1],)),
                tf.keras.layers.Dense(64, activation='relu'),
                tf.keras.layers.Dense(1, activation='sigmoid') # Assuming binary classification
            ])
            model.compile(
                loss='binary_crossentropy',
                optimizer=params.get("optimizer", "adam"),
                metrics=['accuracy']
            )
            validation_data_tf = (X_val, y_val) if (X_val is not None and y_val is not None and len(X_val) > 0) else None
            model.fit(
                X, y,
                validation_data=validation_data_tf,
                epochs=params.get("epochs", 10),
                verbose=1 # Set to 0 for less output, 1 or 2 for more
            )
            return model
        return train_model

    elif framework == "pytorch":
        class SimpleNN(nn.Module):
            def __init__(self, input_dim):
                super().__init__()
                self.net = nn.Sequential(
                    nn.Linear(input_dim, 64), nn.ReLU(),
                    nn.Linear(64, 1), nn.Sigmoid() # Assuming binary classification
                )
            def forward(self, x): return self.net(x)

        def train_model(X, y, X_val=None, y_val=None, **params):
            input_dim = X.shape[1]
            model = SimpleNN(input_dim)
            loss_fn = nn.BCELoss()
            optimizer = torch.optim.Adam(model.parameters(), lr=params.get("lr", 0.001))
            
            # Convert pandas DataFrames/Series to PyTorch Tensors
            # This should ideally happen before calling this function, or ModelManager should handle it.
            # For this example, we assume X and y might still be numpy/pandas.
            if not isinstance(X, torch.Tensor): X_tensor = torch.tensor(X.values if hasattr(X, 'values') else X, dtype=torch.float32)
            else: X_tensor = X
            if not isinstance(y, torch.Tensor): y_tensor = torch.tensor(y.values if hasattr(y, 'values') else y, dtype=torch.float32).unsqueeze(1)
            else: y_tensor = y.unsqueeze(1) if len(y.shape) == 1 else y


            loader = DataLoader(TensorDataset(X_tensor, y_tensor), batch_size=params.get("batch_size_torch", 32), shuffle=True)

            for epoch in range(params.get("epochs", 10)):
                model.train()
                for xb, yb in loader:
                    optimizer.zero_grad()
                    pred = model(xb)
                    loss = loss_fn(pred, yb)
                    loss.backward()
                    optimizer.step()
                # Optional: print epoch loss
                # print(f"Epoch {epoch+1}/{params.get('epochs', 10)}, Loss: {loss.item():.4f}")
            return model
        return train_model
    else:
        raise ValueError(f"Unsupported framework selected in factory: {framework}")

# --- Plotting Helper Functions ---
def plot_confusion_matrix(y_true, y_pred, framework_name, title="Confusion Matrix"):
    cm = confusion_matrix(y_true, y_pred)
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=["No", "Yes"], yticklabels=["No", "Yes"])
    plt.title(f"{framework_name} - {title}"); plt.xlabel("Predicted"); plt.ylabel("Actual"); plt.tight_layout(); plt.show()

def plot_precision_recall_curve(y_true, y_proba, framework_name, title="Precision-Recall Curve"):
    precision, recall, _ = precision_recall_curve(y_true, y_proba)
    avg_precision = average_precision_score(y_true, y_proba)
    plt.figure(); plt.plot(recall, precision, label=f"AP={avg_precision:.2f}"); plt.xlabel("Recall")
    plt.ylabel("Precision"); plt.title(f"{framework_name} - {title}"); plt.legend(); plt.grid(True); plt.tight_layout(); plt.show()

def plot_threshold_analysis(y_true, y_proba, framework_name, title="Threshold Analysis"):
    thresholds = np.linspace(0, 1, 100); precisions = []; recalls = []; f1s = []
    for t in thresholds:
        preds = (y_proba >= t).astype(int)
        if np.sum(preds) > 0 and np.sum(y_true) > 0:
            p_val, r_val, _ = precision_recall_curve(y_true, preds, pos_label=1)
            precisions.append(p_val[1] if len(p_val) > 1 else 0.0) 
            recalls.append(r_val[1] if len(r_val) > 1 else 0.0)
        else: 
            precisions.append(0.0)
            recalls.append(0.0)
        f1s.append(f1_score(y_true, preds, zero_division=0))
    plt.figure(figsize=(8, 5)); plt.plot(thresholds, precisions, label="Precision", color="blue")
    plt.plot(thresholds, recalls, label="Recall", color="green"); plt.plot(thresholds, f1s, label="F1 Score", color="red")
    plt.axvline(x=0.5, linestyle='--', color='gray', label="Threshold = 0.5"); plt.xlabel("Threshold")
    plt.ylabel("Score"); plt.title(f"{framework_name} - {title}"); plt.legend(); plt.grid(True); plt.tight_layout(); plt.show()

# --- Main SDK Workflow Execution ---
def main_sdk_workflow():
    print(" Kusa SDK: Starting Workflow ")

    # 1. Initialize Client
    print(" Authenticating and Initializing SDK Client...")
    client = SecureDatasetClient(public_id=PUBLIC_ID, secret_key=SECRET_KEY)
    init_info = client.initialize()
    print(f" SDK Initialized. Total data rows: {init_info['metadata']['totalDataRows']}")
    # print("Data Preview:\n", init_info["preview"])

    # 2. Fetch Entire Dataset (SDK handles batching internally)
    print(f" Fetching entire dataset (SDK manages batches based on total rows)...")
    # The method name client.fetch_and_decrypt_batch now fetches the *entire* dataset by looping internally.
    # User specifies a batch_size for the underlying transfer operations.
    client.fetch_and_decrypt_batch(batch_size=5000) # Example transfer batch size

    # 3. Configure and Run Preprocessing
    print("⚙️ Configuring and Running Preprocessing...")
    client.configure_preprocessing({ 
        "tokenizer": "nltk",             # Example: "spacy", "split", "none"
        "stopwords": True,               # Default: True
        "reduction": "tfidf",            # Example: "pca", "tfidf_pca", "none"
        "n_components": 10,              # For PCA if used
        "tfidf_max_features": 1000,      # For TF-IDF if used
        "target_column": TARGET_COLUMN,
        "target_encoding": "auto"        # Example: {"Yes": 1, "No": 0}
    })
    client.run_preprocessing() # Operates on the full dataset fetched above
                               # Raw data reference is cleared internally after this.

    # 4. Define Training Function
    print(f"🎯 Building training function for {TRAINING_FRAMEWORK}...")
    train_model_func = None
    hyperparams = {}
    if TRAINING_FRAMEWORK == "sklearn":
        train_model_func = train_model_factory(TRAINING_FRAMEWORK, model_class=RandomForestClassifier)
        hyperparams = {"n_estimators": 100, "class_weight": "balanced"} 
    elif TRAINING_FRAMEWORK == "tensorflow":
        train_model_func = train_model_factory(TRAINING_FRAMEWORK)
        hyperparams = {"epochs": 5, "optimizer": "adam"} 
    elif TRAINING_FRAMEWORK == "pytorch":
        train_model_func = train_model_factory(TRAINING_FRAMEWORK)
        hyperparams = {"epochs": 5, "lr": 0.001, "batch_size_torch": 64} 
    
    if train_model_func is None:
        raise ValueError(f"Training function not created for framework: {TRAINING_FRAMEWORK}")

    # 5. Train Model
    print("🚀 Training model...")
    client.train(
         user_train_func=train_model_func, 
         hyperparams=hyperparams, 
         target_column=TARGET_COLUMN,
         task_type="classification", 
         framework=TRAINING_FRAMEWORK 
    )

    # 6. Evaluate Model
    print("📈 Evaluating model...")
    results = client.evaluate() 
    print("\nEvaluation Accuracy:", results.get("accuracy", "N/A"))
    print("Classification Report:\n", results.get("report", "N/A"))

    # 7. Visualizations 
    # For robust visualization, ensure ModelManager provides clean access to validation data.
    print("📉 Visualizing model performance...")
    try:
        # Attempt to get validation data from ModelManager (preferred way)
        y_true_val = client.model_manager.get_y_val() 
        X_val_processed = client.model_manager.get_x_val()

        if y_true_val is not None and X_val_processed is not None and not X_val_processed.empty:
            y_pred_val_classes = client.predict(X_val_processed) # Predicts classes

            plot_confusion_matrix(y_true_val, y_pred_val_classes, TRAINING_FRAMEWORK)

            y_pred_val_proba = None
            trained_model_internal = client.model_manager.get_model()
            if trained_model_internal:
                if TRAINING_FRAMEWORK == "sklearn" and hasattr(trained_model_internal, "predict_proba"):
                    y_pred_val_proba = trained_model_internal.predict_proba(X_val_processed)[:, 1]
                elif TRAINING_FRAMEWORK == "tensorflow":
                    y_pred_val_proba = trained_model_internal.predict(X_val_processed).flatten()
                elif TRAINING_FRAMEWORK == "pytorch":
                    trained_model_internal.eval()
                    with torch.no_grad():
                        if not isinstance(X_val_processed, torch.Tensor):
                            inputs = torch.tensor(X_val_processed.values, dtype=torch.float32)
                        else:
                            inputs = X_val_processed
                        y_pred_val_proba = trained_model_internal(inputs).numpy().flatten()
            
            if y_pred_val_proba is not None:
                plot_precision_recall_curve(y_true_val, y_pred_val_proba, TRAINING_FRAMEWORK)
                plot_threshold_analysis(y_true_val, y_pred_val_proba, TRAINING_FRAMEWORK)
        else:
            print("   Skipping detailed visualizations: Validation data (X_val, y_val) not available from ModelManager.")
    except Exception as e:
        print(f"   Error during visualization: {e}")

    # 8. Save Model
    model_filename = f"kusa_trained_model_{TRAINING_FRAMEWORK}.ksmodel" 
    print(f"💾 Saving trained model to {model_filename}...")
    client.save_model(model_filename)

    print("\n✅ Workflow Complete!")

if __name__ == "__main__":
    main_sdk_workflow()
```

### 🛠️ Making Predictions with a Saved Model (`predict.py`)

```python
import os
from dotenv import load_dotenv
import pandas as pd
from kusa.client import SecureDatasetClient

# --- Configuration ---
MODEL_FILENAME = "kusa_trained_model_sklearn.ksmodel" # Path to your saved model
MODEL_TRAINING_FRAMEWORK = "sklearn" # Framework the model was trained with
TARGET_COLUMN = "RainTomorrow" # Define for context if needed for output mapping

# --- Load Environment Variables ---
load_dotenv()
PUBLIC_ID = os.getenv("PUBLIC_ID") 
SECRET_KEY = os.getenv("SECRET_KEY")


def make_prediction_with_sdk(new_input_data_dict):
    print(" Kusa SDK: Prediction Workflow ")

    # 1. Initialize Client
    client = SecureDatasetClient(public_id=PUBLIC_ID, secret_key=SECRET_KEY)
    print(" Initializing SDK client for prediction context...")
    client.initialize() 

    # 2. Load Model (this also loads associated preprocessing transformers)
    print(f"📦 Loading model '{MODEL_FILENAME}' trained with {MODEL_TRAINING_FRAMEWORK}...")
    client.load_model(MODEL_FILENAME, training_framework=MODEL_TRAINING_FRAMEWORK)

    # 3. Prepare Input Data for Prediction
    # New input data must be a Pandas DataFrame with the same raw column structure 
    # as the data used for training (before preprocessing).
    new_input_df = pd.DataFrame([new_input_data_dict])
    print(" Input data for prediction:\n", new_input_df.to_string()) # .to_string() for better console output

    # 4. Make Prediction
    # The SDK's predict method will internally apply the saved preprocessing steps.
    print("🔮 Making prediction...")
    predictions = client.predict(new_input_df) # client.predict handles preprocessing
    
    predicted_class_value = predictions[0] # Assuming single prediction, binary output
    predicted_label = "Yes" if predicted_class_value == 1 else "No" 

    print(f" Raw Prediction Output: {predicted_class_value}")
    print(f" Predicted '{TARGET_COLUMN}': {predicted_label}")
    return predicted_label

if __name__ == "__main__":
    # Example new data (must match the raw feature names and types of training data)
    example_input_data = {
        'Date': '2024-01-15', 'Location': 'Melbourneairport', 'MinTemp': 15.0, 
        'MaxTemp': 25.0, 'Rainfall': 0.0, 'Evaporation': 5.0, 'Sunshine': 9.0,
        'WindGustDir': 'N', 'WindGustSpeed': 40.0, 
        'WindDir9am': 'NE', 'WindDir3pm': 'NNE',
        'WindSpeed9am': 15.0, 'WindSpeed3pm': 20.0, 
        'Humidity9am': 60.0, 'Humidity3pm': 40.0,
        'Pressure9am': 1015.0, 'Pressure3pm': 1012.0, 
        'Cloud9am': 3.0, 'Cloud3pm': 4.0, 
        'Temp9am': 18.0, 'Temp3pm': 23.0, 
        'RainToday': 'No'
        # The target column ('RainTomorrow') should NOT be in the input for prediction
    }
    make_prediction_with_sdk(example_input_data)
```

### ⚙️ Preprocessing Configuration Options

When calling `client.configure_preprocessing(config_dict)`, the `config_dict` can include:

*   `"tokenizer"`: `str` - Method for splitting text.
    *   `"nltk"` (default): Uses NLTK's `word_tokenize`.
    *   `"spacy"`: Uses spaCy for tokenization. Requires `spacy` and a model like `en_core_web_sm` to be installed (`pip install kusa[all_ml]` or `pip install spacy && python -m spacy download en_core_web_sm`).
    *   `"split"`: Simple whitespace splitting.
    *   `"none"`: Treats entire text field as a single token.
*   `"stopwords"`: `bool` - If `True` (default), removes common English stopwords.
*   `"lowercase"`: `bool` - If `True` (default), converts text to lowercase.
*   `"remove_punctuation"`: `bool` - If `True` (default), removes punctuation.
*   `"lemmatize"`: `bool` - If `True` (default `False`), performs lemmatization. Currently most effective if `tokenizer` is `"spacy"`.
*   `"reduction"`: `str` - Dimensionality reduction or feature extraction method.
    *   `"none"` (default): Numeric columns are passed as is. Text columns become space-joined strings of tokens/lemmas.
    *   `"tfidf"`: Applies TF-IDF vectorization to text columns. Original numeric columns are kept as is and concatenated.
    *   `"pca"`: Applies PCA to original numeric columns. Text columns are first converted to TF-IDF, then these TF-IDF features are concatenated with the PCA components from numeric features.
    *   `"tfidf_pca"`: Text columns are converted to TF-IDF. PCA is then applied *only* to these combined TF-IDF features. Original numeric columns are kept as is and concatenated with the PCA-reduced TF-IDF features.
*   `"n_components"`: `int` - Number of principal components for PCA (default `2`). Used if `reduction` involves `pca`.
*   `"tfidf_max_features"`: `int` - Maximum number of features for TF-IDF vectorizer (default `500`).
*   `"target_column"`: `str` - Name of the target variable column in your dataset. **Required for training.**
*   `"target_encoding"`: `str` or `dict` - How to encode the target column if it's categorical.
    *   `"auto"` (default): For binary classification with string targets, automatically maps the two unique values to `0` and `1`.
    *   `"none"`: No encoding applied to the target.
    *   `dict`: A custom mapping, e.g., `{"Yes": 1, "No": 0}`.

### 🛡️ SDK Data Handling and Security Considerations (University Final Project)

The Kusa SDK, developed as a university final project, aims to provide a platform for users to train machine learning models on datasets while exploring data security mechanisms.

**Current Data Flow & Client-Side Processing:**
*   **Authentication & Key Derivation:** The SDK uses your `PUBLIC_ID` and `SECRET_KEY` for authentication. Internally, a portion of your `SECRET_KEY` (e.g., the first 32 bytes) is used as the common encryption key (K\_common) necessary for the client-side decryption process. **Therefore, the security of your `SECRET_KEY` is paramount.**
*   **Encrypted Batch Transfer:** Datasets are fetched in encrypted batches. Each data batch is encrypted on the server using a temporary, batch-specific key. This batch-specific key is itself encrypted using the K\_common derived from your `SECRET_KEY`.
*   **Client-Side Decryption:** All decryption of batch keys and batch data occurs on the user's machine using this derived K\_common.
*   **Data Accumulation & Client-Side Preprocessing:** Decrypted batches are combined in the client's memory to form the complete dataset, which is then preprocessed locally.
*   **Raw Data Clearing (Attempted):** Post-preprocessing, the SDK attempts to remove references to the raw, decrypted dataset from memory and suggests garbage collection.
*   **Model Training:** Model training occurs on the user's machine.

**Security Consideration in the Current Project Implementation:**
*   **Temporary Exposure of Raw Data in Client Memory:** During the interval between data decryption into client memory and its subsequent processing and clearing, the raw, unencrypted data exists temporarily on the user's machine.
*   **Theoretical Vulnerability:** It's theoretically possible for a user with advanced technical skills and local machine access to use memory inspection tools during this window to potentially view portions of the raw dataset.
*   **`SECRET_KEY` Sensitivity:** Since a part of your `SECRET_KEY` is used directly in cryptographic operations on the client-side, protecting your `SECRET_KEY` (e.g., in your `.env` file, not committing it to version control) is critically important. If your `SECRET_KEY` is compromised, the security of the batch key encryption mechanism for your account could be affected.

This aspect was noted during development. Given the time constraints and scope of a final university project, the current implementation focuses on demonstrating the core functionalities.

**Proposed Future Enhancement: Server-Side Preprocessing for Improved Security**
To address the identified vulnerability and demonstrate a more advanced security posture, a future enhancement would involve:
1.  **Server-Side Preprocessing:** All data decryption and preprocessing would be moved to the backend. The raw dataset would never be decrypted on the user's local machine.
2.  **Backend Adaptation:** This would likely involve integrating a dedicated Python execution environment with the existing Node.js server (or migrating relevant services) to efficiently handle Python-based data science tasks.
3.  **Transfer of Processed Features:** Only the processed, feature-engineered data would be sent from the server to the client SDK.
4.  **Client-Side Model Training:** Model training would continue on the user's machine with these processed features.

While implementing this advanced server-side preprocessing was beyond the feasible timeframe for this university final project, it outlines a clear path for future development.

### 📄 License

This Kusa SDK is licensed under the **MIT License**. Please see the `LICENSE` file in the repository for more details.
*(Ensure you have an MIT LICENSE file in your project root).*

### 🤝 Contributing & Support

*   **Issues & Bug Reports:** [https://github.com/Nesril/kusaSdk/issues](https://github.com/Nesril/kusaSdk/issues)
*   **Source Code:** [https://github.com/Nesril/kusaSdk](https://github.com/Nesril/kusaSdk)
*   **Full Documentation Website:** [http://kuusa.netlify.app/docs](http://kuusa.netlify.app/docs)

---
```