import psycopg2

conn = psycopg2.connect(
    dbname="cbde", 
    user="postgres", 
    password="1234", 
    host="localhost", 
    port="5432"
)
cur = conn.cursor()

consulta = "SELECT * FROM sentences LIMIT 10;"
cur.execute(consulta)
filas = cur.fetchall()

for fila in filas:
    print(fila)

cur.close()
conn.close()
