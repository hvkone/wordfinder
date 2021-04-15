# util model

# TODO: keeping update
language_list = ['Chinese',
                 'English',
                 'French',
                 'Italian',
                 'Japanese',
                 'Korean',
                 'Russian'
                 ]

language_dict = {'1': 'Chinese',
                 '2': 'English',
                 '3': 'French',
                 '4': 'Italian',
                 '5': 'Japanese',
                 '6': 'Korean',
                 '7': 'Russian'
                 }

db_config = {
    'host': 'psd-wordfinder.mysql.database.azure.com',
    'database': 'psd_project',
    'user': 'adminteam@psd-wordfinder',
    'password': 'jFq&T7bPJXmY',
    'client_flags': '[mysql.connector.ClientFlag.SSL]',
    'ssl_ca': '/train/DigiCertGlobalRootG2.crt.pem'
}

cluster_model_file = {'Chinese': r'C:\Users\haris\Desktop\wordFinder\word2vecChinese',
                      'English': r'C:\Users\haris\Desktop\wordFinder\word2vecEnglish'}

