import time
import chromadb
from datasets import load_dataset
import numpy as np

chroma_client = chromadb.PersistentClient(path="./ChromaBD")

collection_euc = chroma_client.create_collection(name="cbde-euc", metadata={"hnsw:space": "l2"})
collection_cos = chroma_client.create_collection(name="cbde-cos", metadata={"hnsw:space": "cosine"})

# carregar el conjunt de dades
dataset = load_dataset("bookcorpus.py", split='train',trust_remote_code=True)

# extreure frases (limitant a 10.000 frases)
sentences = dataset[:10000]['text']

ids = [f"{id}" for id in range(1, 10001)]

times = []

for id, sentence in zip(ids, sentences):
    start_time = time.time()
    collection_euc.add(
            documents=[sentence],
            ids=[id],
            embeddings=None
        )
    collection_cos.add(
            documents=[sentence],
            ids=[id],
            embeddings=None
        )
    end_time = time.time()

    times.append(end_time - start_time)

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



