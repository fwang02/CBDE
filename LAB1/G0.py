import time
from datasets import load_dataset
import numpy as np
import psycopg2

# carregar el conjunt de dades
dataset = load_dataset("bookcorpus.py", split='train',trust_remote_code=True)

# extreure frases (limitant a 10.000 frases)
sentences = dataset[:10000]['text']

# connectar a la base de dades PostgreSQL
conn = psycopg2.connect(
    dbname="cbde", 
    user="postgres", 
    password="1234", 
    host="localhost", 
    port="5432"
)
cur = conn.cursor()

# crear una taula per emmagatzemar frases y els seus embeddings
cur.execute('''
    CREATE TABLE IF NOT EXISTS sentences_pgv (
        id SERIAL PRIMARY KEY,
        sentence TEXT NOT NULL,
        embedding vector(384)
    );
''')
conn.commit()

times = []

# inserir frases a la base de dades PostgreSQL
for sentence in sentences:
    start_time = time.time()
    cur.execute("INSERT INTO sentences_pgv (sentence) VALUES (%s)", (sentence,))
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