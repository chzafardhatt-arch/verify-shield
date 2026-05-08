import sqlite3
import secrets
import hashlib
from datetime import datetime

DB_NAME = "verifyshield.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        api_key TEXT UNIQUE NOT NULL,
        plan TEXT DEFAULT 'starter',
        requests_used INTEGER DEFAULT 0,
        requests_limit INTEGER DEFAULT 1000,
        created_at TEXT,
        is_active INTEGER DEFAULT 1
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS usage_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        api_key TEXT,
        checked_email TEXT,
        status TEXT,
        score INTEGER,
        timestamp TEXT
    )''')
    
    conn.commit()
    conn.close()

def generate_api_key():
    return "vs_" + secrets.token_hex(24)

def create_client(name, email, plan="starter"):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    api_key = generate_api_key()
    created_at = datetime.now().isoformat()
    
    limits = {"starter": 1000, "growth": 10000, "enterprise": 999999}
    limit = limits.get(plan, 1000)
    
    c.execute('''INSERT INTO clients (name, email, api_key, plan, requests_limit, created_at)
                 VALUES (?, ?, ?, ?, ?, ?)''',
              (name, email, api_key, plan, limit, created_at))
    conn.commit()
    conn.close()
    return api_key

def validate_api_key(api_key):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM clients WHERE api_key=? AND is_active=1", (api_key,))
    client = c.fetchone()
    conn.close()
    return client

def increment_usage(api_key):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE clients SET requests_used = requests_used + 1 WHERE api_key=?", (api_key,))
    conn.commit()
    conn.close()

def log_usage(api_key, checked_email, status, score):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''INSERT INTO usage_log (api_key, checked_email, status, score, timestamp)
                 VALUES (?, ?, ?, ?, ?)''',
              (api_key, checked_email, status, score, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_all_clients():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, name, email, api_key, plan, requests_used, requests_limit, created_at, is_active FROM clients")
    clients = c.fetchall()
    conn.close()
    return clients

def get_usage_logs(api_key, limit=50):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM usage_log WHERE api_key=? ORDER BY timestamp DESC LIMIT ?", (api_key, limit))
    logs = c.fetchall()
    conn.close()
    return logs

# Initialize database on import
init_db()