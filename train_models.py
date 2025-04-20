import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

# 1. Load the dataset
df = pd.read_csv("labeled_sessions.csv")

# 2. Select Features and Labels
X = df[["total_hits", "bot_hits", "unique_paths", "avg_interval"]]
y = df["label"]

# 3. Train-Test Split
if len(df) < 5:
    raise ValueError("⚠️ Not enough data. Please rerun simulator to collect more traffic!")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, stratify=y, test_size=0.3, random_state=42
)

# 4. Train Models
lr = LogisticRegression().fit(X_train, y_train)
rf = RandomForestClassifier(n_estimators=100, random_state=42).fit(X_train, y_train)
iso = IsolationForest(contamination=0.3, random_state=42).fit(X_train)
y_pred_iso = pd.Series(iso.predict(X_test)).map({1: "human", -1: "bot"})

# 5. Predict
y_pred_lr = lr.predict(X_test)
y_pred_rf = rf.predict(X_test)

# 6. Classification Reports
print("\n📊 Logistic Regression Report:\n", classification_report(y_test, y_pred_lr))
print("\n🌲 Random Forest Report:\n", classification_report(y_test, y_pred_rf))
print("\n🧪 Isolation Forest Report:\n", classification_report(y_test, y_pred_iso))

# 7. Visualize Confusion Matrices
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
ConfusionMatrixDisplay.from_predictions(y_test, y_pred_lr, ax=axes[0], display_labels=["human", "bot"], cmap="Blues")
axes[0].set_title("Logistic Regression")
ConfusionMatrixDisplay.from_predictions(y_test, y_pred_rf, ax=axes[1], display_labels=["human", "bot"], cmap="Greens")
axes[1].set_title("Random Forest")
ConfusionMatrixDisplay.from_predictions(y_test, y_pred_iso, ax=axes[2], display_labels=["human", "bot"], cmap="Purples")
axes[2].set_title("Isolation Forest")
plt.tight_layout()
plt.show()
