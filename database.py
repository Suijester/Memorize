# sql database to hold all the memos
connector = sqlite3.connect("memos.db")
cursor = connector.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS memos (
    id INTEGER PRIMARY KEY,
    transcript TEXT,
    summary TEXT,
    date TEXT
    )
""")
connector.commit()

