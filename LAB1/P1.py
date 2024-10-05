import psycopg2
from sentence_transformers import SentenceTransformer
from datasets import load_dataset

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

conn = psycopg2.connect(
    dbname="cbde", 
    user="postgres", 
    password="1234", 
    host="localhost", 
    port="5432"
)
cur = conn.cursor()

consulta = "SELECT id,sentence FROM sentences;"
cur.execute(consulta)
rows = cur.fetchall()

for row in rows:
    id = row[0]
    sentence = row[1]
    embedding = model.encode(sentence).tolist()
    cur.execute("UPDATE sentences SET embedding = %s WHERE id = %s", (embedding, id))

conn.commit()
cur.close()
conn.close()