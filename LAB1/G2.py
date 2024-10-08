import time
import numpy as np
import psycopg2
from sentence_transformers import util

# connectar a la base de dades PostgreSQL
conn = psycopg2.connect(
    dbname="cbde", 
    user="postgres", 
    password="1234", 
    host="localhost", 
    port="5432"
)
cur = conn.cursor()

cur.execute("SELECT * FROM sentences_pgv WHERE id BETWEEN 1 AND 10;")
rows = cur.fetchall()

times = []

for row in rows:
    start_time = time.time()

    embedding = row[2]
    print(f"Frase: {row[1]}")
    print("\nCosine similarity:")
    cur.execute('''SELECT *, 1 - (embedding <=> %s) AS cosine_similarity 
                FROM sentences_pgv 
                ORDER BY embedding <=> %s 
                LIMIT 3;''', (embedding,embedding))
    
    cos_result = cur.fetchall()
    for i in range(1,len(cos_result)):
        print(f"top{i}: {cos_result[i][1]}, similarity: {cos_result[i][3]}")
    
    print("\nEuclidean distance:")
    cur.execute('''SELECT *, embedding <-> %s AS distance 
                FROM sentences_pgv 
                ORDER BY embedding <=> %s 
                LIMIT 3;''', (embedding,embedding))
    
    euc_result = cur.fetchall()
    for i in range(1,len(euc_result)):
        print(f"top{i}: {euc_result[i][1]}, similarity: {euc_result[i][3]}")
    print("------------------------------------------------------------\n")
    end_time = time.time()
    times.append(end_time - start_time)

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
    
        