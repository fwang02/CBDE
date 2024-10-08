import time
import chromadb
import chromadb.utils.embedding_functions 
import numpy as np
from sentence_transformers import SentenceTransformer

# Inicializar el cliente de Chroma
chroma_client = chromadb.PersistentClient(path="./ChromaBD")


collection_euc = chroma_client.get_collection(name="cbde-euc")
collection_cos = chroma_client.get_collection(name="cbde-cos")
data = collection_euc.get()

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

times = []

for id, sentence in zip(data['ids'], data['documents']):
        aux = model.encode(sentence).tolist()
        start_time = time.time()
        collection_euc.update(
            ids=[id],
            embeddings = [aux]
        )
        collection_cos.update(
            ids=[id],
            embeddings = [aux]
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
