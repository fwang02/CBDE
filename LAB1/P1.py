import sys
import psycopg2
from sentence_transformers import SentenceTransformer
from datasets import load_dataset

# connectar a la base de dades PostgreSQL
conn = psycopg2.connect(
    dbname="cbde", 
    user="postgres", 
    password="1234", 
    host="localhost", 
    port="5432"
)
cur = conn.cursor()

# transformador de sentències
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

consulta = "SELECT id,sentence FROM sentences where embedding = '{}';"
cur.execute(consulta)

# obtenir totes les files
rows = cur.fetchall()

if not rows:
    print("totes sentencies ja tenen embedding")
    sys.exit()
    
for row in rows:
    id = row[0]
    sentence = row[1]
    embedding = model.encode(sentence).tolist()
    cur.execute("UPDATE sentences SET embedding = %s WHERE id = %s", (embedding, id))

conn.commit()
cur.close()
conn.close()