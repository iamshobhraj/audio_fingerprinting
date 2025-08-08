import sqlite3

DB_NAME = "fingerprints.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS fingerprints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS hashes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fingerprint_id INTEGER,
            hash TEXT,
            offset INTEGER,
            FOREIGN KEY(fingerprint_id) REFERENCES fingerprints(id)
        )
    """)
    conn.commit()
    conn.close()

def store_fingerprint(filename, hashes):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Insert or ignore file
    c.execute("INSERT INTO fingerprints (filename) VALUES (?)", (filename,))
    fingerprint_id = c.lastrowid
    # Insert hashes
    for hash_val, offset in hashes:
        c.execute("INSERT INTO hashes (fingerprint_id, hash, offset) VALUES (?, ?, ?)", (fingerprint_id, hash_val, offset))
    conn.commit()
    conn.close()
    return fingerprint_id

def find_match(hashes, threshold=10):
    """
    Given a list of (hash, offset) tuples, find the best matching filename and score.
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    hash_values = [h[0] for h in hashes]
    best_match = None
    best_count = 0
    if not hash_values:
        return None
    # Find all matching hashes in DB
    q = "SELECT fingerprint_id, COUNT(*) as count FROM hashes WHERE hash IN ({}) GROUP BY fingerprint_id ORDER BY count DESC LIMIT 1".format(
        ",".join("?"*len(hash_values))
    )
    c.execute(q, hash_values)
    row = c.fetchone()
    if row and row[1] >= threshold:
        fingerprint_id = row[0]
        c.execute("SELECT filename FROM fingerprints WHERE id=?", (fingerprint_id,))
        fname = c.fetchone()
        if fname:
            best_match = fname[0]
            best_count = row[1]
    conn.close()
    if best_match:
        return {"filename": best_match, "score": best_count}
    return None