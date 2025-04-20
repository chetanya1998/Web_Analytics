import threading
import requests
import time
import random

# Server address (Flask)
TARGET = "http://localhost:5050"

# Simulated paths
paths = ["/", "/home", "/products", "/about", "/contact", "/search", "/login", "/admin", "/cart", "/checkout"]

# Fake user agents
human_uas = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (Linux; Android 10; SM-G973F)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X)",
]

bot_uas = [
    "Googlebot/2.1 (+http://www.google.com/bot.html)",
    "Bingbot/2.0 (+http://www.bing.com/bingbot.htm)",
    "AhrefsBot/7.0 (+http://ahrefs.com/robot/)",
    "SemrushBot/7.1 (+http://www.semrush.com/bot.html)"
]

# Random fake IPs
def generate_fake_ip():
    return f"{random.randint(11, 200)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"

# Human simulation: click around slowly, varied paths, delays
def simulate_human_session():
    session_length = random.randint(3, 8)  # number of pages per session
    ip = generate_fake_ip()
    ua = random.choice(human_uas)
    headers = {"User-Agent": ua, "X-Forwarded-For": ip}

    print(f"🧍 Human session from IP {ip}")
    for _ in range(session_length):
        path = random.choice(paths)
        try:
            requests.get(TARGET + path, headers=headers, timeout=5)
        except Exception as e:
            print(f"❌ Human request failed: {e}")
        time.sleep(random.uniform(1, 4))  # delay between clicks

# Bot simulation: short burst of hits, repeated or aggressive
def simulate_bot_session():
    burst_count = random.randint(10, 30)
    ip = generate_fake_ip()
    ua = random.choice(bot_uas)
    headers = {"User-Agent": ua, "X-Forwarded-For": ip}

    print(f"🤖 Bot burst from IP {ip}")
    for _ in range(burst_count):
        path = random.choice(paths[:4])  # bots often target root/admin/product
        try:
            requests.get(TARGET + path, headers=headers, timeout=2)
        except Exception as e:
            print(f"❌ Bot request failed: {e}")
        time.sleep(random.uniform(0.05, 0.25))  # very fast

# Launch N sessions of each type in parallel
def launch_sessions():
    total_humans = 20
    total_bots = 15

    for _ in range(total_humans):
        threading.Thread(target=simulate_human_session, daemon=True).start()
        time.sleep(random.uniform(0.1, 0.3))  # staggered start

    for _ in range(total_bots):
        threading.Thread(target=simulate_bot_session, daemon=True).start()
        time.sleep(random.uniform(0.05, 0.2))  # staggered burst bots

# Run for 3 minutes then exit
if __name__ == "__main__":
    print("🚦 Starting traffic simulation...")
    launch_sessions()
    time.sleep(180)
    print("✅ Simulation complete. Check access.log.")
