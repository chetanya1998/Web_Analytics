import streamlit as st
import pandas as pd
import numpy as np
import joblib
import time
import requests
from datetime import datetime
from collections import defaultdict, deque

# Load models
log_model = joblib.load("models/logistic_model.pkl")
rf_model = joblib.load("models/rf_model.pkl")
iso_model = joblib.load("models/isolation_forest.pkl")

LOG_FILE = "logs/access.log"
GEO_API = "http://ip-api.com/json/{}"

# Caching for faster geo lookup
geo_cache = {}

def geo_lookup(ip):
    if ip in geo_cache:
        return geo_cache[ip]
    try:
        response = requests.get(GEO_API.format(ip), timeout=2)
        data = response.json()
        geo_cache[ip] = f"{data.get('city', 'Unknown')}, {data.get('countryCode', 'N/A')}"
    except:
        geo_cache[ip] = "Unknown"
    return geo_cache[ip]

# Parse log line
def parse_log_line(line):
    try:
        timestamp_str, ip, user_agent, path = line.strip().split(" | ")
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        return timestamp, ip, user_agent, path
    except:
        return None

# Extract features
def extract_features(sessions):
    data = []
    for ip, logs in sessions.items():
        logs = sorted(logs, key=lambda x: x[0])
        times = [x[0] for x in logs]
        paths = [x[3] for x in logs]
        user_agents = list(set(x[2] for x in logs))
        avg_interval = np.mean([(times[i] - times[i-1]).total_seconds() for i in range(1, len(times))]) if len(times) > 1 else 0

        features = {
            "ip": ip,
            "total_hits": len(logs),
            "unique_paths": len(set(paths)),
            "avg_interval": avg_interval,
            "user_agent": user_agents[0],
            "location": geo_lookup(ip)
        }
        data.append(features)
    return pd.DataFrame(data)

# Classification
def classify_sessions(df):
    if df.empty:
        return df
    X = df[["total_hits", "unique_paths", "avg_interval"]]
    df["Logistic"] = log_model.predict(X)
    df["RandomForest"] = rf_model.predict(X)
    df["IsolationForest"] = iso_model.predict(X)
    return df

# Live log stream
def run_live_stream():
    last_pos = 0
    while True:
        sessions = defaultdict(list)
        with open(LOG_FILE, "r") as f:
            f.seek(last_pos)
            new_lines = f.readlines()
            last_pos = f.tell()

        for line in new_lines:
            parsed = parse_log_line(line)
            if parsed:
                timestamp, ip, user_agent, path = parsed
                sessions[ip].append((timestamp, ip, user_agent, path))

        df = extract_features(sessions)
        df = classify_sessions(df)
        yield df, len(new_lines)

        time.sleep(5)

# UI setup
st.set_page_config(page_title="Real-Time Traffic Classifier", layout="wide")
st.title("📡 Real-Time Bot vs Human Traffic Classifier")

# Sidebar filters
st.sidebar.header("🔍 Search & Filter")
search_ip = st.sidebar.text_input("Search by IP")
search_agent = st.sidebar.text_input("Search by User-Agent")

# Live content container
placeholder = st.empty()
trend_data = deque(maxlen=50)

# Stream and update
for df, new_count in run_live_stream():
    # Filter data
    if search_ip:
        df = df[df["ip"].str.contains(search_ip)]
    if search_agent:
        df = df[df["user_agent"].str.contains(search_agent, case=False)]

    bot_ratio = df["Logistic"].sum() / len(df) if len(df) > 0 else 0
    trend_data.append((datetime.now(), new_count))

    with placeholder.container():
        if bot_ratio > 0.5:
            st.error(f"⚠️ Alert: High bot activity detected! {bot_ratio:.2%} of current traffic.")
        else:
            st.success(f"✅ Bot activity normal. Only {bot_ratio:.2%} bots detected.")

        st.subheader("📊 Live Classified Traffic")
        st.dataframe(df[["ip", "location", "user_agent", "total_hits", "unique_paths", "avg_interval", "Logistic"]])

        st.subheader("📈 Traffic Trend (Hits Every 5s)")
        trend_df = pd.DataFrame(trend_data, columns=["timestamp", "hits"])
        trend_df.set_index("timestamp", inplace=True)
        st.line_chart(trend_df)
