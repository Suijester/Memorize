from imports import * 

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def getDatabase():
    conn = psycopg2.connect(
        user = "postgres",
        password = "password",
        host = "localhost",
        port = "5432",
        dbname = "memos"
    )
    return conn

conn = getDatabase()
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS memos (
        id SERIAL PRIMARY KEY,
        filename TEXT,
        transcript TEXT,
        date TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        embedding vector(768)
    )
''')

conn.commit()
conn.close()


def saveMemo(filename, transcript):
    embedding = model.encode(transcript)
    conn = getDatabase()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO memos (filename, transcript, date, embedding)
        VALUES ($1, $2, $3, $4)
    ''', (filename, transcript, datetime.datetime.now().strftime("%m/%d/%Y"), embedding))
    
    conn.commit()
    conn.close()

