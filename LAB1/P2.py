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

def euclidean_distance(embedding1, embedding2):
    return np.linalg.norm(np.array(embedding1) - np.array(embedding2))

cur.execute("SELECT id, embedding FROM sentences WHERE id BETWEEN 1 AND 10;")
rows = cur.fetchall()

cur.execute("SELECT id, embedding FROM sentences;")
allRows = cur.fetchall()

times = []

for row in rows:
    id = row[0]
    embedding = row[1]
    top1_cos, top2_cos  = float('-inf'), float('-inf')
    top1_euc, top2_euc = float('inf'), float('inf')
    top1_cos_id, top2_cos_id = -1, -1
    top1_euc_id, top2_euc_id = -1, -1

    cur.execute("SELECT sentence FROM sentences WHERE id = %s;", (id,))
    sentence = cur.fetchone()[0]

    start_time = time.time()
    for row2 in allRows:
        id2 = row2[0]
        if id != id2:
            embedding2 = row2[1]
            sim_cos = util.cos_sim(embedding, embedding2)
            sim_euc = euclidean_distance(embedding, embedding2) 

            if sim_cos > top1_cos:
                top2_cos = top1_cos
                top2_cos_id = top1_cos_id
                top1_cos = sim_cos
                top1_cos_id = id2
            elif sim_cos > top2_cos:
                top2_cos = sim_cos
                top2_cos_id = id2

            if sim_euc < top1_euc:
                top2_euc = top1_euc
                top2_euc_id = top1_euc_id
                top1_euc = sim_euc
                top1_euc_id = id2
            elif sim_euc < top2_euc:
                top2_euc = sim_euc
                top2_euc_id = id2

    end_time = time.time()
    times.append(end_time - start_time)

    cur.execute("SELECT sentence FROM sentences WHERE id = %s;", (top1_cos_id,))
    top1_cos_sentence = cur.fetchone()[0]
    cur.execute("SELECT sentence FROM sentences WHERE id = %s;", (top2_cos_id,))
    top2_cos_sentence = cur.fetchone()[0]
    cur.execute("SELECT sentence FROM sentences WHERE id = %s;", (top1_euc_id,))
    top1_euc_sentence = cur.fetchone()[0]
    cur.execute("SELECT sentence FROM sentences WHERE id = %s;", (top2_euc_id,))
    top2_euc_sentence = cur.fetchone()[0]
    
    print('Sentence: ' + sentence + '\n')
    print('Top 1 cosine sentence: ' + top1_cos_sentence + ', ' + 'similarity: ' + str(top1_cos) + '\n')
    print('Top 2 cosine sentence: ' + top2_cos_sentence + ', ' + 'similarity: ' + str(top2_cos) + '\n')
    print('Top 1 euclidean sentence: ' + top1_euc_sentence + ', ' + 'similarity: ' + str(top1_euc) + '\n')
    print('Top 2 euclidean sentence: ' + top2_euc_sentence + ', ' + 'similarity: ' + str(top2_euc) + '\n')
    print('------------------------------------------------------------\n')

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
    
        