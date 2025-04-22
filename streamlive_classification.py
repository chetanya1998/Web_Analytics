import time
import joblib
import pandas as pd
from sklearn.ensemble import IsolationForest
from datetime import datetime
from collections import defaultdict

# Load pre-trained models
logistic_model = joblib.load("models/logistic_model.pkl")
rf_model = joblib.load("models/rf_model.pkl")
iso_model = joblib.load("models/isolation_forest.pkl")

LOG_FILE = "logs/access.log"
SEEN_IPS = set()
INTERVAL = 5  # check every 5 seconds

def parse_log_line(line):
    try:
        timestamp_str, ip, user_agent, path = line.strip().split(" | ")
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        return timestamp, ip, user_agent, path
    except ValueError:
        return None

def extract_features(sessions):
    data = []
    for ip, logs in sessions.items():
        logs = sorted(logs, key=lambda x: x[0])
        times = [x[0] for x in logs]
        paths = [x[3] for x in logs]
        user_agents = list(set(x[2] for x in logs))

        intervals = [(times[i] - times[i-1]).total_seconds() for i in range(1, len(times))]
        avg_interval = sum(intervals)/len(intervals) if intervals else 0

        features = {
            "ip": ip,
            "total_hits": len(logs),
            "unique_paths": len(set(paths)),
            "avg_interval": avg_interval,
            "user_agent": user_agents[0] if user_agents else ""
        }
        data.append(features)

    return pd.DataFrame(data)

def classify_and_display(df):
    if df.empty:
        return
    df_for_model = df[["total_hits", "unique_paths", "avg_interval"]]
    
    df["LogisticPrediction"] = logistic_model.predict(df_for_model)
    df["RandomForestPrediction"] = rf_model.predict(df_for_model)
    df["IsolationForest"] = iso_model.predict(df_for_model)

    print("\n📊 Live Classification Results")
    print(df[["ip", "LogisticPrediction", "RandomForestPrediction", "IsolationForest"]])
    print("-" * 60)

def stream_log():
    print("📡 Starting live log classification...")
    sessions = defaultdict(list)
    last_position = 0

    while True:
        with open(LOG_FILE, "r") as f:
            f.seek(last_position)
            new_lines = f.readlines()
            last_position = f.tell()
            print(f"📥 Read {len(new_lines)} new log entries...")
        for line in new_lines:
            parsed = parse_log_line(line)
            if parsed:
                timestamp, ip, user_agent, path = parsed
                sessions[ip].append((timestamp, ip, user_agent, path))

        df_features = extract_features(sessions)
        classify_and_display(df_features)
        print("🔍 Classifying current session features...")

        time.sleep(INTERVAL)

if __name__ == "__main__":
    stream_log()
