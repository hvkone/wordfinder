from cnx_mysql import *
from src.util import *

conn

conn_cur = conn.cursor()

table_query = "INSERT INTO english_sentences (id,sentence) VALUES(01,'This is a test.')"
conn_cur.execute(table_query)
conn.commit()
print(conn_cur.rowcount, "Record Inserted")