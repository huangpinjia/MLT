import sqlite3

def init_db():
    conn = sqlite3.connect('vocabia.db')
    c = conn.cursor()
    # Scores 表
    c.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            score INTEGER,
            total INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # 收藏單字表
    c.execute('''
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT UNIQUE,
            definition TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_favorite(word, definition):
    conn = sqlite3.connect('vocabia.db')
    c = conn.cursor()
    try:
        c.execute('INSERT OR IGNORE INTO favorites (word, definition) VALUES (?, ?)', (word, definition))
        conn.commit()
    finally:
        conn.close()

def get_favorites():
    conn = sqlite3.connect('vocabia.db')
    c = conn.cursor()
    c.execute('SELECT word, definition FROM favorites')
    data = c.fetchall()
    conn.close()
    return data
