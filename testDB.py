from imports import *
import database

def testDatabaseConnection():
    conn = None
    try:
        conn = database.getDatabase()
        if conn:
            print("Database connection successful!")
            return True
        else:
            print("Database connection failed.")
            return False
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return False
    finally:
        if conn:
            conn.close()

def testSaveMemos():
    try:
        filename = "testMemo.wav"
        transcript = "Today morning, I went outside, did a little bit of traveling. I don't remember what the last thing I did yesterday night was, but I put my keys on the front desk."
        print(f"\nSaving test memo: '{transcript}'")
        database.saveMemo(filename, transcript)

        print("\nRetrieving memo by filename:")
        database.getMemobyFilename(filename)
        return True
    except Exception as e:
        print(f"Error in testSaveMemos: {e}")
        return False

def testVectorSearch():
    try:
        query = "Where did I put my keys?"
        print(f"\nQuerying for similar memo: '{query}'")
        database.queryMemos(query)
        return True
    except Exception as e:
        print(f"Error in testVectorSearch: {e}")
        return False

def testDeleteMemos():
    try:
        filename = "testMemo.wav"
        print(f"\nDeleting memo with filename: {filename}")
        database.deleteMemo(filename)
        print("\nVerifying deletion:")
        database.getMemobyFilename(filename)
        
    except Exception as e:
        print(f"Error in testDeleteMemos: {e}")
        return False

if __name__ == "__main__":
    print("=== Testing PostgreSQL Database with pgvector ===")
    
    if testDatabaseConnection():
        print("\n=== Testing Save Functionality ===")
        testSaveMemos()

        print("\n=== Testing Vector Search Functionality ===")
        testVectorSearch()

        print("\n=== Testing Delete Functionality ===")
        testDeleteMemos()

        deleteAllMemos()
    
    print("\n=== Test Complete ===")