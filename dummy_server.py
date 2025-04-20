from flask import Flask, request
from datetime import datetime

app = Flask(__name__)
LOG_FILE = "access.log"

@app.before_request
def log_request():
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Prefer 'X-Forwarded-For' header if present
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    ua = request.headers.get("User-Agent", "-")
    path = request.path
    
    log_line = f"{timestamp} {ip} {ua} {path}\n"
    
    # Append to access.log
    with open(LOG_FILE, "a") as f:
        f.write(log_line)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return f"You visited: /{path}", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)  # Adjust port if needed
