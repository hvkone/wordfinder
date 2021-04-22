from gensim.models import Word2Vec
import gensim, logging
import os

from src.util import *

'''
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

sentences = [['first',
              'Although this detail has no connection whatever with the real substance of what we are about to relate,',
              'it will not be superfluous, if merely for the sake of exactness in all points, to mention here the various',
              'rumors and remarks which had been in circulation about him from the very moment when he arrived in the diocese.'],
             ['second',
              'True or false, that which is said of men often occupies as important a place in their lives, and above',
              'all in their destinies, as that which they do.']]
# train word2vec on the two sentences
model = gensim.models.Word2Vec(sentences, min_count=1)
'''


class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname)):
                yield line.split()


for lang in language_list:
    if lang in [
        'Latin'
    ]:
        file = 'corpus/latin/'
        ex_str = ',encoding="utf8"'

        sentences = MySentences(file)  # a memory-friendly iterator
        #str_com = sentences + ex_str
        model = gensim.models.Word2Vec(sentences)
        save_path = './corpus/word2vecmodel/%s' % lang
        # save(save_path)
