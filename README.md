
# 🧠 Web Traffic Classification using ML - Human Clicks vs  Bot Clicks Detection

This project simulates, logs, processes, and classifies web traffic into **bot** and **human** using machine learning. It mimics how tools like AdScore detect spam, fraud, and real users.

---

## 🚀 What It Does

- Simulates realistic **bot** and **human** traffic to a Flask-based dummy server.
- Logs all traffic (`timestamp`, `IP`, `User-Agent`, `path`) to `access.log`.
- Processes logs into IP-level session features:
  - `total_hits`, `bot_hits`, `unique_paths`, `avg_interval`
- Labels sessions as **bot** or **human** based on user-agent and behavior.
- Trains 3 classifiers:
  - Logistic Regression ✅
  - Random Forest ✅
  - Isolation Forest (unsupervised ⚠️)
- Visualizes model performance with:
  - 📉 Confusion matrices
  - 📊 Classification reports
  - 🔬 Correlation matrix
  - 🔎 Pairplots of feature interactions

---

## 📁 Key Files

| File                | Purpose                                |
|---------------------|----------------------------------------|
| `dummy_server.py`   | Logs all requests (Flask app)          |
| `traffic_simulator.py` | Generates human & bot traffic         |
| `prepare_dataset.py`| Parses logs and builds labeled dataset |
| `train_models.py`   | Trains ML models & generates reports   |
| `labeled_sessions.csv` | Final ML training data                |
| `features.csv`      | Raw session features for clustering    |

---

## 📈 Sample Output

- ✅ Logistic Regression & Random Forest: 100% accuracy on clean data
- ⚠️ Isolation Forest struggled due to class imbalance
- 🔥 Correlation shows `total_hits` = `bot_hits` for most bots
- 📉 Humans show slower `avg_interval` and fewer hits

---

## ▶️ How to Run

```bash
# 1. Start Flask traffic logger
python3 dummy_server.py

# 2. Simulate mixed traffic (bots + humans)
python3 traffic_simulator.py

# 3. Build dataset from logs
python3 prepare_dataset.py

# 4. Train & visualize models
python3 train_models.py


