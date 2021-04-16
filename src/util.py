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
    'English',
    'Finnish',
    'French',
    'German',
    'Greek',
    'Hungarian',
    'Italian',
    'Japanese',
    'Korean',
    'Portuguese',
    'Russian'
]

language_dict = {
    '1': 'Chinese',
    '2': 'English',
    '3': 'Finnish',
    '4': 'French',
    '5': 'German',
    '6': 'Greek',
    '7': 'Hungarian',
    '8': 'Italian',
    '9': 'Japanese',
    '10': 'Korean',
    '11': 'Portuguese',
    '12': 'Russian'
}

# language and corresponding file path of corpus
corpus_language = {'Chinese': './/corpus//chinese//23825-0.txt',
                   'English': './/corpus//english//wiki_en.txt',
                   'French': './/corpus//french//wiki_fr.txt',
                   'Italian': './/corpus//italian//wiki_it.txt',
                   'Spanish': './/corpus//spanish//wiki_es.txt',
                   'Korean': './/corpus//korean//wiki_ko.txt',
                   'Russian': './/corpus//russian//wiki_ru.txt',
                   'Portuguese': './/corpus//portuguese//wiki_pt.txt'}

udpipe_language = {'Chinese': './/corpus//udpipemodel//chinese.udpipe',
                   'English': './/corpus//udpipemodel//english.udpipe',
                   'French': './/corpus//udpipemodel//french.udpipe',
                   'Italian': './/corpus//udpipemodel//italian.udpipe',
                   'Spanish': './/corpus//udpipemodel//spanish.udpipe',
                   'Korean': './/corpus//udpipemodel//korean.udpipe',
                   'Russian': './/corpus//udpipemodel//russian.udpipe',
                   'Portuguese': './/corpus//udpipemodel//portuguese.udpipe'}

word2vec_language = {'Chinese': './/corpus//word2vecmodel//gensim-word2vec-udpipemodel-Chinese',
                     'English': './/corpus//word2vecmodel//gensim-word2vec-udpipemodel-English',
                     'French': './/corpus//word2vecmodel//gensim-word2vec-udpipemodel-French',
                     'Italian': './/corpus//word2vecmodel//gensim-word2vec-udpipemodel-Italian',
                     'Spanish': './/corpus//word2vecmodel//gensim-word2vec-udpipemodel-Spanish',
                     'Korean': './/corpus//word2vecmodel//gensim-word2vec-udpipemodel-Korean',
                     'Russian': './/corpus//word2vecmodel//gensim-word2vec-udpipemodel-Russian',
                     'Portuguese': './/corpus//word2vecmodel//gensim-word2vec-udpipemodel-Portuguese'}


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