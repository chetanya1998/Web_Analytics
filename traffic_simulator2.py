import time
import random
from datetime import datetime

# Output file
LOG_FILE = "logs/access.log"

# Sample data pools
HUMAN_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (Linux; Android 11; Pixel 4)"
]

BOT_USER_AGENTS = [
    "Googlebot/2.1 (+http://www.google.com/bot.html)",
    "Bingbot/2.0 (+http://www.bing.com/bingbot.htm)",
    "Mozilla/5.0 (compatible; AhrefsBot/6.1)",
    "python-requests/2.28.1"
]

HUMAN_PATHS = ["/home", "/about", "/products", "/contact", "/blog/post-1", "/blog/post-2"]
BOT_PATHS = ["/", "/.env", "/admin", "/wp-login.php", "/login", "/robots.txt"]

HUMAN_IPS = [f"192.168.1.{i}" for i in range(10, 50)]
BOT_IPS = [f"10.0.0.{i}" for i in range(1, 20)]

def write_log_entry(ip, user_agent, path):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{timestamp} | {ip} | {user_agent} | {path}\n"
    with open(LOG_FILE, "a") as log_file:
        log_file.write(line)

def simulate_traffic():
    print("🚦 Simulating live web traffic... (CTRL+C to stop)")
    while True:
        # Decide whether this is a human or a bot
        traffic_type = random.choices(["human", "bot"], weights=[0.7, 0.3])[0]

        if traffic_type == "human":
            ip = random.choice(HUMAN_IPS)
            user_agent = random.choice(HUMAN_USER_AGENTS)
            path = random.choice(HUMAN_PATHS)
        else:
            ip = random.choice(BOT_IPS)
            user_agent = random.choice(BOT_USER_AGENTS)
            path = random.choice(BOT_PATHS)

        # Write the log
        write_log_entry(ip, user_agent, path)

        # Sleep to simulate request interval
        time.sleep(random.uniform(0.2, 1.5))  # Faster for bots, slower for humans

if __name__ == "__main__":
    simulate_traffic()
