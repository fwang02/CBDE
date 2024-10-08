import time
import numpy as np
import chromadb

chroma_client = chromadb.PersistentClient(path="./ChromaBD")
collection_euc = chroma_client.get_collection(name="cbde-euc")
collection_cos = chroma_client.get_collection(name="cbde-cos")

ids = [f"{id}" for id in range(1, 11)]
data_euc = collection_euc.get(ids=ids, include=['documents','embeddings'])
data_cos = collection_cos.get(ids=ids, include=['documents','embeddings'])

embeddings_euc = [embedding.tolist() for embedding in data_euc['embeddings']]
embeddings_cos = [embedding.tolist() for embedding in data_cos['embeddings']]

start_time = time.time()
results_euc = collection_euc.query(
    query_embeddings=embeddings_euc,
    n_results=3
)
results_cos = collection_cos.query(
    query_embeddings=embeddings_cos,
    n_results=3
)
end_time = time.time()

print("Resultados de la consulta (euclidiana):")
for i, result in enumerate(results_euc['documents']):
    print(f"Frase: {data_euc['documents'][i]}:")
    print("\n")
    print("Euclidean distance:")
    j = 1
    for doc_id, doc_text, distance in zip(results_euc['ids'][i][1:], result[1:], results_euc['distances'][i][1:]):
        print(f"top{j}: {doc_text}, similarity: {distance} ")
        j += 1
    print(f"--------------------")
        
print("\n")
print(f"--------------------")
print("Resultados de la consulta (cosinus):")

for i, result in enumerate(results_cos['documents']):
    print(f"Frase: {data_cos['documents'][i]}:")
    print("\n")
    print("Cosine similarity:")
    j = 1
    for doc_id, doc_text, distance in zip(results_cos['ids'][i][1:], result[1:], results_cos['distances'][i][1:]):
        print(f"top{j}: {doc_text}, similarity: {distance} ")
        j += 1
    print(f"--------------------")

print("Time: " + str(end_time - start_time))













