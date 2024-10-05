from datasets import load_dataset
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
    CREATE TABLE IF NOT EXISTS sentences (
        id SERIAL PRIMARY KEY,
        sentence TEXT NOT NULL,
        embedding FLOAT8[] DEFAULT '{}'
    );
''')
conn.commit()

#\pset pager off
# inserir frases a la base de dades PostgreSQL
for sentence in sentences:
    cur.execute("INSERT INTO sentences (sentence) VALUES (%s)", (sentence,))
conn.commit()


cur.close()
conn.close()
