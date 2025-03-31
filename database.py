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

cursor.execute("CREATE EXTENSION IF NOT EXISTS vector")

cursor.execute('''
    CREATE TABLE IF NOT EXISTS memos (
        id SERIAL PRIMARY KEY,
        filename TEXT,
        transcript TEXT,
        date TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        embedding vector(384)
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
        VALUES (%s, %s, %s, %s)
    ''', (filename, transcript, datetime.now().strftime("%m/%d/%Y"), embedding))
    
    conn.commit()
    conn.close()

def queryMemos(query):
    queryEmbedded = model.encode(query)
    
    conn = getDatabase()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT id, filename, transcript, date, created_at
        , (1 - embedding <=> %s) * 0.7 +
        EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - created_at)) * -0.00001 * 0.3 AS score
        FROM memos
        ORDER BY score DESC
        LIMIT 1
    ''', (queryEmbedded,))

    result = cursor.fetchone()
    conn.close()

    if result:
        print(f"Most Relevant Memo (ID: {result[0]}):")
        print(f"File Name: {result[1]}")
        print(f"Date: {result[3]}")
        print(f"Created At: {result[4]}")
        print(f"Transcript:\n{result[2]}")
    else:
        print("No comparable .")

def deleteMemo(filename):
    conn = getDatabase()
    cursor = conn.cursor()
    
    cursor.execute('''
        DELETE FROM memos
        WHERE filename = %s
    ''', (filename,))
    
    conn.commit()
    conn.close()