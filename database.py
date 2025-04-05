from imports import * 
import getpass

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def getDatabase():
    try:
        username = getpass.getuser()
        conn = psycopg2.connect(
            user = username,
            host = "localhost",
            port = "5432",
            dbname = "memos"
        )
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

conn = getDatabase()
if conn is not None:
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
    embeddingList = embedding.tolist()
    
    conn = getDatabase()
    if conn is not None:
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO memos (filename, transcript, date, embedding)
            VALUES (%s, %s, %s, %s)
        ''', (filename, transcript, datetime.now().strftime("%m/%d/%Y"), embeddingList))
        
        conn.commit()
        conn.close()

def getMemobyFilename(filename):
    conn = getDatabase()
    if conn is not None:
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM memos
            WHERE filename = %s
        ''', (filename,))

        result = cursor.fetchone()
        conn.close()

        if result:
            print(f"Most Relevant Memo (ID: {result[0]}):")
            print(f"File Name: {result[1]}")
            print(f"Date: {result[3]}")
            print(f"Created At: {result[4]}")
            print(f"Transcript:\n{result[2]}")
        else:
            print(f"No memo named {filename} as such found.")    

def queryMemos(query):
    queryEmbedded = model.encode(query)
    queryEmbeddedList = queryEmbedded.tolist()
    
    conn = getDatabase()
    if conn is not None:
        cursor = conn.cursor()

        cursor.execute('''
            WITH memo_distances AS (
                SELECT 
                    id, 
                    filename, 
                    transcript, 
                    date, 
                    created_at,
                    embedding <=> %s::vector AS distance,
                    EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - created_at)) AS timeDistance
                FROM memos
            )
            SELECT * FROM memo_distances
            ORDER BY ((0.7 * distance) + (0.3 * timeDistance)) ASC
            LIMIT 1
        ''', (queryEmbeddedList,))

        result = cursor.fetchone()
        conn.close()

        if result:
            print(f"Date: {result[3]}")
            print(f"Similarity Distance: {result[5]:.4f} (lower is better)")
            print(f"Transcript: {result[2]}\n")
        else:
            print("No memo that's similar by vector search.")

def deleteMemo(filename):
    conn = getDatabase()
    if conn is not None:
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM memos
            WHERE filename = %s
        ''', (filename,))
        
        conn.commit()
        conn.close()

def deleteAllMemos():
    conn = getDatabase()
    if conn is not None:
        cursor = conn.cursor()

        cursor.execute('''SELECT * FROM memos''')
        results = cursor.fetchall()

        if results:
            for result in results:
                if os.path.exists(result[1]):
                    os.remove(result[1])

        cursor.execute('''
            DELETE FROM memos
        ''')

        conn.commit()
        conn.close()

def printAllMemos():
    conn = getDatabase()
    if conn is not None:
        cursor = conn.cursor()

        cursor.execute('''SELECT * FROM memos''')
        results = cursor.fetchall()
        conn.close()

        if results:
            for result in results:
                print(f"File Name: {result[1]}")
                print(f"Transcript: {result[2]}\n")
                
        else:
            print("No memos found.")