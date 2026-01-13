import sqlite3

con = sqlite3.connect("TheLibrary.db")
cur = con.cursor()

# Create table if it does not exist
cur.execute("""
CREATE TABLE IF NOT EXISTS responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prompt TEXT NOT NULL,
    response TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
) 
""")
            
cur.execute("""
CREATE TABLE IF NOT EXISTS evaluations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    response_id INTEGER NOT NULL,
    evaluation TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (response_id) REFERENCES responses(id)
)

""")
con.commit()

def insert_response(prompt, response):
    """
    Insert a prompt and response into the database.
    """
    cur.execute(
        "INSERT INTO responses (prompt, response) VALUES (?, ?)",
        (prompt, response)
    )
    con.commit()
    #print(con)
    #print("Inserted prompt and response into database.")

def fetch_responses():
    """
    Fetch all responses from the database.
    """
    cur.execute("SELECT * FROM responses")
    return cur.fetchall()


def insert_evaluation(response_id, evaluation_json):
    """
    Insert an evaluated prompt and response into the database.
    """
    cur.execute(
        "INSERT INTO evaluations (response_id, evaluation) VALUES (?, ?)",
        (response_id, evaluation_json)
    )

    con.commit()
    #print("Inserted evaluated prompt and response into database.")

def get_recent_responses(limit=1):
    """
    Fetch recent evaluations from the database.
    """
    cur.execute("SELECT * FROM responses ORDER BY created_at DESC LIMIT ?", (limit,))
    return cur.fetchall()