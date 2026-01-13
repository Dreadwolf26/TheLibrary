import sqlite3
from log_data import logger

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
logger.info("Responses table ensured in database.")

            
cur.execute("""
CREATE TABLE IF NOT EXISTS evaluations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    response_id INTEGER NOT NULL,
    evaluation TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (response_id) REFERENCES responses(id)
)

""")
logger.info("Evaluations table ensured in database.")

cur.execute("""
CREATE TABLE IF NOT EXISTS prompt_enhance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    response_id INTEGER NOT NULL,
    prompt_enhance TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (response_id) REFERENCES responses(id)
)

""")
logger.info("Prompt Enhance table ensured in database.")

con.commit()

def insert_response(prompt, response):
    """
    Insert a prompt and response into the database.
    """
    cur.execute(
        "INSERT INTO responses (prompt, response) VALUES (?, ?)",
        (prompt, response)
    )
    logger.info(f"Inserted response for prompt: {prompt}")
    con.commit()
    #print(con)
    #print("Inserted prompt and response into database.")

# def fetch_responses():
#     """
#     Fetch all responses from the database.
#     """
#     cur.execute("SELECT * FROM responses")
#     return cur.fetchall()


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

def insert_prompt_enhance(response_id, prompt_enhance_text):
    """
    Insert a prompt enhancement into the database.
    """
    cur.execute(
        "INSERT INTO prompt_enhance (response_id, prompt_enhance) VALUES (?, ?)",
        (response_id, prompt_enhance_text)
    )

    con.commit()
    #print("Inserted prompt enhancement into database.")

def get_recent_responses(limit=1):
    """
    Fetch recent evaluations from the database.
    """
    cur.execute("SELECT * FROM responses ORDER BY created_at DESC LIMIT ?", (limit,))
    return cur.fetchall()
