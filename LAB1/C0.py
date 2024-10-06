import chromadb
from datasets import load_dataset
from chromadb.config import Settings


chroma_client = chromadb.PersistentClient(path="./ChromaBD")
collection = chroma_client.create_collection(name="cbde")

# carregar el conjunt de dades
dataset = load_dataset("bookcorpus.py", split='train',trust_remote_code=True)

# extreure frases (limitant a 10.000 frases)
sentences = dataset[:10000]['text']

for id, sentence in enumerate(sentences):
    collection.add(
        documents=[str(sentence)],
        ids=[str(id)] 
    )








