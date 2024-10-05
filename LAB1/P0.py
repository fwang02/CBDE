from datasets import load_dataset
import psycopg2

# Step 1: Load the dataset
dataset = load_dataset("bookcorpus.py", split='train',trust_remote_code=True)

# Step 2: Extract sentences (limiting to 10,000 sentences)
sentences = dataset[:10000]['text']

# Step 3: Connect to PostgreSQL database

conn = psycopg2.connect(
    dbname="cbde", 
    user="postgres", 
    password="1234", 
    host="localhost", 
    port="5432"
)
cur = conn.cursor()

# Step 4: Create a table for storing sentences
cur.execute('''
    CREATE TABLE IF NOT EXISTS sentences (
        id SERIAL PRIMARY KEY,
        sentence TEXT NOT NULL,
        embedding FLOAT8[] DEFAULT '{}'
    );
''')
conn.commit()

#\pset pager off
# Step 5: Insert sentences into the PostgreSQL database
for sentence in sentences:
    cur.execute("INSERT INTO sentences (sentence) VALUES (%s)", (sentence,))
conn.commit()


cur.close()
conn.close()
