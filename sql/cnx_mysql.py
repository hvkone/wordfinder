import mysql.connector
from mysql.connector import errorcode
from mysql.connector.constants import ClientFlag

# Obtain connection string information from the portal
db_config = {
    'host': 'psd-wordfinder.mysql.database.azure.com',
    'database': 'psd_project',
    'user': 'adminteam@psd-wordfinder',
    'password': 'jFq&T7bPJXmY',
    'client_flags': [mysql.connector.ClientFlag.SSL],
    'ssl_ca': './sql/DigiCertGlobalRootG2.crt.pem'
}

# Construct connection string
try:
    conn = mysql.connector.connect(**db_config)
    if conn:
        print("Database psd_project was located.")
        
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with the user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
