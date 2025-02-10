import sqlite3

def init_db():
    conn = sqlite3.connect('config/streams.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS streams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            tableId TEXT,
            picked_for_yolo BOOLEAN NOT NULL DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
