import sys
import time
import numpy as np
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
    
times = []
for row in rows:
    id = row[0]
    sentence = row[1]
    embedding = model.encode(sentence).tolist()
    start_time = time.time()
    cur.execute("UPDATE sentences SET embedding = %s WHERE id = %s", (embedding, id))
    end_time = time.time()
    times.append(end_time - start_time)

conn.commit()
cur.close()
conn.close()

times_array = np.array(times)
min_time = np.min(times_array)
max_time = np.max(times_array)
std_time = np.std(times_array)
avg_time = np.mean(times_array)
sum_time = np.sum(times_array)

print(f"Minimum time: {min_time} seconds")
print(f"Maximum time: {max_time} seconds")
print(f"Standard deviation: {std_time} seconds")
print(f"Average time: {avg_time} seconds")
print(f"Total time: {sum_time} seconds")