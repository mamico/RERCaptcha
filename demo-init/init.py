#!/usr/bin/env python3
import sqlite3, json, os, time, base64, secrets
from argon2 import PasswordHasher

DB_PATH = os.environ.get("CAPJS_DB", "/data/db.sqlite")
KEYS_FILE = "/shared/keys.json"
SITE_NAME = "flask-test"

os.makedirs(os.path.dirname(KEYS_FILE), exist_ok=True)

print("⏳ Attendo che il database esista...")
for _ in range(30):
    if os.path.exists(DB_PATH):
        break
    time.sleep(1)
else:
    raise SystemExit("❌ Database non trovato: " + DB_PATH)

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

cur.execute("SELECT * FROM keys WHERE name=?", (SITE_NAME,))
row = cur.fetchone()

# TODO: se la chiava non è in key_files, ma sul db va cancellata dal db e
#       rigenerata
if row:
    print(f"✅ Chiave già presente per '{SITE_NAME}'")
    # data = {"siteKey": row["siteKey"], "secretKey": "(hidden)"}
    data = json.load(open(KEYS_FILE))
else:
    print(f"🆕 Creo nuova chiave per '{SITE_NAME}'")
    siteKey = secrets.token_hex(5)
    secretKey = base64.urlsafe_b64encode(secrets.token_bytes(30)).decode().rstrip("=")
    hasher = PasswordHasher()
    secretHash = hasher.hash(secretKey)

    config = json.dumps({
        "difficulty": 4,
        "challengeCount": 50,
        "saltSize": 32,
        "expiresMS": 60000,
        "tokenTTL": 120000,
    })

    cur.execute(
        "INSERT INTO keys (siteKey, name, secretHash, config, created) VALUES (?, ?, ?, ?, ?)",
        (siteKey, SITE_NAME, secretHash, config, int(time.time() * 1000))
    )
    conn.commit()

    data = {"siteKey": siteKey, "secretKey": secretKey}

    with open(KEYS_FILE, "w") as f:
        json.dump(data, f, indent=2)

print(f"💾 Chiavi salvate in {KEYS_FILE}")
print(json.dumps(data, indent=2))

