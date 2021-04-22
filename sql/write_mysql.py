import os
import re
from src.util import *
from cnx_mysql import *

conn
conn_cur = conn.cursor()


for lang in language_list:
    if lang in [
        'Latin'
    ]:
        file_dir = corpus_language[lang]
        path = os.getcwd()+file_dir

org_file = open(path,'r+')
ready_file = open(path,'w')
# prepare your ready file

for line in org_file:
    # substitute useless information this also creates some formatting for the actually loading into mysql
    line = re.sub('latin_sentences|', '\n', line)
    line = re.sub('latin_sentences|', '', line)
    ready_file.write(line)

# load your ready file into db

# close file
ready_file.close()

table_query = "LOAD DATA LOCAL INFILE %s INSERT INTO latin_sentences field terminated by '|' lines terminated by '\n'" % ready_file
conn_cur.execute(table_query)

conn.commit()
print(conn_cur.rowcount, "Record Inserted")
