"""
@file: util.py
@desc: utility model
@author: group3
@time: 2/28/2021
"""

from typing import List
import re
import base64

pwd = base64.b64decode(b'TGh4R3oxMDIyMzE=')

language_list = ['Chinese',
                 'English',
                 'French',
                 'Italian',
                 'Spanish',
                 'Korean',
                 'Russian',
                 'Portuguese']

language_dict = {'1': 'Chinese',
                 '2': 'English',
                 '3': 'French',
                 '4': 'Italian',
                 '5': 'Spanish',
                 '6': 'Korean',
                 '7': 'Russian',
                 '8': 'Portuguese'}

# database config, remote mysql
db_config = {'user': 'root',
             'password': pwd.decode("utf-8"),
             'db_host': '192.144.171.233',
             'db_name': 'psd_project'}

# language and corresponding file path of corpus
corpus_language = {'Chinese': 'input//corpus//result//zh.txt',
                   'English': 'input//corpus//result//wiki_en.txt',
                   'French': 'input//corpus//result//wiki_fr.txt',
                   'Italian': 'input//corpus//result//wiki_it.txt',
                   'Spanish': 'input//corpus//result//wiki_es.txt',
                   'Korean': 'input//corpus//result//wiki_ko.txt',
                   'Russian': 'input//corpus//result//wiki_ru.txt',
                   'Portuguese': 'input//corpus//result//wiki_pt.txt'}

udpipe_language = {'Chinese': 'input//udpipemodel//chinese-gsdsimp-ud-2.5-191206.udpipe',
                   'English': 'input//udpipemodel//english-ewt-ud-2.5-191206.udpipe',
                   'French': 'input//udpipemodel//french-gsd-ud-2.5-191206.udpipe',
                   'Italian': 'input//udpipemodel//italian-isdt-ud-2.5-191206.udpipe',
                   'Spanish': 'input//udpipemodel//spanish-gsd-ud-2.5-191206.udpipe',
                   'Korean': 'input//udpipemodel//korean-gsd-ud-2.5-191206.udpipe',
                   'Russian': 'input//udpipemodel//russian-gsd-ud-2.5-191206.udpipe',
                   'Portuguese': 'input//udpipemodel//portuguese-gsd-ud-2.5-191206.udpipe'}

word2vec_language = {'Chinese': 'input//word2vecmodel//gensim-word2vec-model-Chinese',
                     'English': 'input//word2vecmodel//gensim-word2vec-model-English',
                     'French': 'input//word2vecmodel//gensim-word2vec-model-French',
                     'Italian': 'input//word2vecmodel//gensim-word2vec-model-Italian',
                     'Spanish': 'input//word2vecmodel//gensim-word2vec-model-Spanish',
                     'Korean': 'input//word2vecmodel//gensim-word2vec-model-Korean',
                     'Russian': 'input//word2vecmodel//gensim-word2vec-model-Russian',
                     'Portuguese': 'input//word2vecmodel//gensim-word2vec-model-Portuguese'}


def get_keyword_window(sel_word: str, words_of_sentence: List, length=5) -> List[str]:
    """
    find the index of sel_word at sentence, then decide words of @length size
    by backward and forward of it.
    For example: I am very happy to this course of psd if sel_word is happy, then
    returning: [am, very, happy, to, this]

    if length is even, then returning [very, happy, to, this]

    remember: sel_word is lemmatized
    """
    if length <= 0 or len(words_of_sentence) <= length:
        return words_of_sentence
    index = -1
    for iw, word in enumerate(words_of_sentence):
        word = word.lower()
        if len(re.findall(sel_word, word)) > 0:
            index = iw

    if index == -1:
        print("warning: cannot find %s in sentence: %s" % (sel_word, words_of_sentence))
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


def kwic_show(words_of_sentence, sel_word, sum_sent_length=60, key_word_space=1):
    """
    TODO: need to more test
    """
    sent = ' '.join(words_of_sentence)
    key_index = sent.lower().index(sel_word.lower())
    if key_index != -1:
        pre_kwic = sent[:key_index].rjust(sum_sent_length//2)
        key_kwic = key_word_space*' ' + sel_word + key_word_space*' '
        post_kwic = sent[key_index+len(sel_word):]
        sel_word_kwic = pre_kwic + key_kwic + post_kwic
        return sel_word_kwic
    return None
