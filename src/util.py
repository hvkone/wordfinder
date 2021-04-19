# util udpipemodel

from typing import List


# TODO: keeping update

# database config
# cofig for local database
db_config = {
    'host': 'psd-wordfinder.mysql.database.azure.com',
    'database': 'psd_project',
    'user': 'adminteam@psd-wordfinder',
    'password': 'jFq&T7bPJXmY',
    #'client_flags': [mysql.connector.ClientFlag.SSL],
    #'ssl_ca': './/src//train//DigiCertGlobalRootG2.crt.pem' #vscode
    'ssl_ca': 'DigiCertGlobalRootG2.crt.pem' #pycharm
}

language_list = [
    'Chinese',
    'Dutch',
    'English',
    'Finnish',
    'French',
    'German',
    'Greek',
    'Hungarian',
    'Italian',
    'Japanese',
    'Korean',
    'Latin',
    'Polish',
    'Portuguese',
    'Russian',
    'Spanish'
]

language_dict = {
    '1': 'Chinese',
    '2': 'Dutch',
    '3': 'English',
    '4': 'Finnish',
    '5': 'French',
    '6': 'German',
    '7': 'Greek',
    '8': 'Hungarian',
    '9': 'Italian',
    '10': 'Japanese',
    '11': 'Korean',
    '12': 'Latin',
    '13': 'Polish',
    '14': 'Portuguese',
    '15': 'Russian',
    '16': 'Spanish'
}

# language and corresponding file path of corpus
# need to read all files in each folder instead of individual text
corpus_language = {
    'Chinese': './/corpus//chinese//',
    'Dutch': './/corpus//dutch//21800-0.txt',
    'English': './/corpus//english//',
    'Finnish': './/corpus//finish//',
    'French': './/corpus//french//',
    'German': './/corpus//german//',
    'Greek': './/corpus//greek//',
    'Hungarian': './/corpus//hungarian//',
    'Italian': './/corpus//italian//',
    'Japanese': './/corpus//japanese//',
    'Korean': './/corpus//korean//',
    'Latin': './/corpus//latin//',
    'Polish': './/corpus//polish//',
    'Portuguese': './/corpus//portuguese//',
    'Russian': './/corpus//russian//',
    'Spanish': './/corpus//spanish//'
}

udpipe_language = {
    'Chinese': './/corpus//udpipemodel//chinese.udpipe',
    'Dutch': './/corpus//udpipemodel//dutch.udpipe',
    'English': './/corpus//udpipemodel//english.udpipe',
    'Finnish': './/corpus//udpipemodel//finnish.udpipe',
    'French': './/corpus//udpipemodel//french.udpipe',
    'German': './/corpus//udpipemodel//german.udpipe',
    'Greek': './/corpus//udpipemodel//greek.udpipe',
    'Hungarian': './/corpus//udpipemodel//hungarian.udpipe',
    'Italian': './/corpus//udpipemodel//italian.udpipe',
    'Japanese': './/corpus//udpipemodel//japanese.udpipe',
    'Korean': './/corpus//udpipemodel//korean.udpipe',
    'Latin': './/corpus//udpipemodel//latin.udpipe',
    'Polish': './/corpus//udpipemodel//polish.udpipe',
    'Portuguese': './/corpus//udpipemodel//portuguese.udpipe',
    'Russian': './/corpus//udpipemodel//russian.udpipe',
    'Spanish': './/corpus//udpipemodel//spanish.udpipe'
}

word2vec_language = {
    'Chinese': './/corpus//word2vecmodel//gensim-word2vec-udpipemodel-Chinese',
    'Dutch': './/corpus//word2vecmodel//gensim-word2vec-udpipemodel-Dutch',
    'English': './/corpus//word2vecmodel//gensim-word2vec-udpipemodel-English',
    'Finnish': './/corpus//word2vecmodel//gensim-word2vec-udpipemodel-Finnish',
    'French': './/corpus//word2vecmodel//gensim-word2vec-udpipemodel-French',
    'German': './/corpus//word2vecmodel//gensim-word2vec-udpipemodel-German',
    'Greek': './/corpus//word2vecmodel//gensim-word2vec-udpipemodel-Greek',
    'Hungarian': './/corpus//word2vecmodel//gensim-word2vec-udpipemodel-Hungarian',
    'Italian': './/corpus//word2vecmodel//gensim-word2vec-udpipemodel-Italian',
    'Japanese': './/corpus//word2vecmodel//gensim-word2vec-udpipemodel-Japanese',
    'Korean': './/corpus//word2vecmodel//gensim-word2vec-udpipemodel-Korean',
    'Latin': './/corpus//word2vecmodel//gensim-word2vec-udpipemodel-Latin',
    'Polish': './/corpus//word2vecmodel//gensim-word2vec-udpipemodel-Polish',
    'Portuguese': './/corpus//word2vecmodel//gensim-word2vec-udpipemodel-Portuguese',
    'Russian': './/corpus//word2vecmodel//gensim-word2vec-udpipemodel-Russian',
    'Spanish': './/corpus//word2vecmodel//gensim-word2vec-udpipemodel-Spanish'
}


def get_keyword_window(sel_word: str, words_of_sentence: List, length=5) -> List[str]:
    """
    find the index of sel_word at sentence, then decide words of @length size
    by backward and forward of it.
    For example: I am very happy to this course of psd if sel_word is happy, then
    returning: [am, very, happy, to, this]

    if length is even, then returning [very, happy, to, this]

    remember: sel_word is lemmatized
    """
    if length <= 0:
        return words_of_sentence
    index = words_of_sentence.index(sel_word)
    if index == -1:
        return words_of_sentence
    # backward is not enough
    if index < length // 2:
        back_slice = words_of_sentence[:index]
        # forward is also not enough,
        # showing the sentence is too short compared to length parameter
        if (length - index) >= len(words_of_sentence):
            return words_of_sentence
        else:
            return back_slice + words_of_sentence[index: index + length - len(back_slice)]
    # forward is not enough
    if (index + length // 2) >= len(words_of_sentence):
        forward_slice = words_of_sentence[index:len(words_of_sentence)]
        # backward is also not enough,
        # showing the sentence is too short compared to length parameter
        if index - length <= 0:
            return words_of_sentence
        else:
            return words_of_sentence[index - (length - len(forward_slice)):index] + forward_slice

    return words_of_sentence[index - length // 2: index + length // 2 + 1] if length % 2 \
        else words_of_sentence[index - length // 2 + 1: index + length // 2 + 1]