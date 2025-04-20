import pandas as pd
import re
from datetime import datetime

# 1. Load the raw access log
log_file = "access.log"
entries = []
with open(log_file, 'r') as f:
    for line in f:
        try:
            parts = line.strip().split(' ')
            timestamp = ' '.join(parts[0:2])
            ip = parts[2]
            ua = parts[3]
            path = parts[4]
            entries.append([timestamp, ip, ua, path])
        except IndexError:
            continue  # Skip malformed lines

# 2. Create DataFrame
df = pd.DataFrame(entries, columns=['timestamp', 'ip', 'ua', 'path'])
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
df.dropna(subset=['timestamp'], inplace=True)

# 3. Feature: Detect bot user agents
df['is_bot_ua'] = df['ua'].str.contains(r'bot|crawl|spider', flags=re.I)

# 4. Group by IP for session-level features
agg = df.groupby('ip').agg(
    total_hits=('ua', 'size'),
    bot_hits=('is_bot_ua', 'sum'),
    unique_paths=('path', 'nunique'),
    avg_interval=('timestamp', lambda x: x.sort_values().diff().dt.total_seconds().mean())
).fillna(0).reset_index()

# 5. Label: classify as bot if more than 50% hits are bot-like
agg['label'] = agg['bot_hits'] / agg['total_hits'] > 0.5
agg['label'] = agg['label'].map({True: 'bot', False: 'human'})

# 6. Save outputs
agg.to_csv("labeled_sessions.csv", index=False)
agg[['total_hits', 'bot_hits', 'unique_paths', 'avg_interval']].to_csv("features.csv", index=False)

print("✅ Datasets created:\n- labeled_sessions.csv\n- features.csv")
