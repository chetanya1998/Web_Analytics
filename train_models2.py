import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import os

# Create dummy data simulating traffic sessions
def generate_dummy_data(n=500):
    np.random.seed(42)
    data = {
        "total_hits": np.random.poisson(10, n),
        "unique_paths": np.random.randint(1, 10, n),
        "avg_interval": np.random.uniform(0.5, 20.0, n),
        "label": np.random.randint(0, 2, n)  # 0 = Human, 1 = Bot
    }
    return pd.DataFrame(data)

# Train and save models
def train_and_save_models():
    df = generate_dummy_data()

    # Features and labels
    X = df[["total_hits", "unique_paths", "avg_interval"]]
    y = df["label"]

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Logistic Regression
    log_model = LogisticRegression()
    log_model.fit(X_train, y_train)
    print("Logistic Regression:\n", classification_report(y_test, log_model.predict(X_test)))

    # Random Forest
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    print("Random Forest:\n", classification_report(y_test, rf_model.predict(X_test)))

    # Isolation Forest (unsupervised, fit only on 'normal' = human = label 0)
    X_unsup = df[df["label"] == 0][["total_hits", "unique_paths", "avg_interval"]]
    iso_model = IsolationForest(contamination=0.1, random_state=42)
    iso_model.fit(X_unsup)

    # Create models directory if not exists
    os.makedirs("models", exist_ok=True)

    # Save models
    joblib.dump(log_model, "models/logistic_model.pkl")
    joblib.dump(rf_model, "models/rf_model.pkl")
    joblib.dump(iso_model, "models/isolation_forest.pkl")

    print("\n✅ Models saved in /models folder!")

if __name__ == "__main__":
    train_and_save_models()
