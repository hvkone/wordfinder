# encoding: utf-8
"""
@file: vector.py
@desc: This module is mainly used to get the embedding vector of word
@author: group3
@time: 2/25/2021
"""

import os
import gensim.models
from src.feature.postrain import UdpipeTrain
from src.config import language_list, corpus_language, udpipe_language
from src.logs import Log

log = Log()


class WordVector(object):
    def __init__(self, corpus_path, udpipe_model: UdpipeTrain):
        self.corpus_path = corpus_path
        self.udpipe_model = udpipe_model
        self._word_count, self._MAX_WORD_COUNT = 0, 500000

    def __iter__(self):
        for line in open(self.corpus_path):
            # assume there's one document per line, tokens separated by whitespace
            # processed_line = utils.simple_preprocess(line)
            # processed_line = " ".join(processed_line)
            words = self.udpipe_model.word_segmentation(line)
            self._word_count += len(words)
            if self._word_count > self._MAX_WORD_COUNT:
                return
            log.info(words)
            yield words


def train_model(language_name, corpus_path, save_path, udpipe_model: UdpipeTrain):
    """ feature and save word2vec model
    :param udpipe_model:
    :param language_name:
    :param corpus_path: file path for feature corpus
    :param save_path: vector model path after finishing word2vec
    name rule of save_path is
    'gensim-word2vec-model-' + language_name
    :return:
    """

    sentences = WordVector(corpus_path, udpipe_model)
    model = gensim.models.Word2Vec(sentences=sentences,
                                   size=150,
                                   window=8,
                                   min_count=2,
                                   workers=2,
                                   iter=10)
    save_file_name = save_path + language_name
    model.save(save_file_name)
    log.info('%s save succeed' % (save_file_name, ))


def load_model(word2vec_model_path) -> gensim.models.Word2Vec:
    """load model we have trained
    :param word2vec_model_path: filepath saved
    note: because we have ruled the name for word2vec model, so rember to follow it.
    :return: word2vec model we have trained
    """
    try:
        filename = word2vec_model_path
        model = gensim.models.Word2Vec.load(filename)
        log.info('word2vec model %s loads successfully' % (filename,))
    except FileNotFoundError:
        log.error('word2vec model %s not found!' % (word2vec_model_path,))
        return None
    # for index,word in enumerate(model.wv.index2word):
    #     if index == 5:
    #         break
    #     vec = ",".join(map(lambda i: str(i),model.wv[word]))
    #     print(f"word #{index}/{len(model.wv.index2word)} is {word}, vec = {vec}")
    return model


def batch():
    for lang in language_list:
        udpipe_pre_model_path = udpipe_language[lang]
        corpus_filepath = corpus_language[lang]
        # first loading udpipe to segement word for each sentence
        udt_lang = UdpipeTrain(lang, udpipe_pre_model_path, corpus_filepath)
        # second feature to get the word2vec model
        word2vec_result_file = 'input//word2vecmodel//gensim-word2vec-model-'
        train_model(lang, corpus_filepath, word2vec_result_file, udt_lang)


if __name__ == "__main__":
    batch()

    # languange_name = 'English'
    #
    # # input example
    # # # udpipe pre-feature model that we can download from a link in readme
    # # udpipe_pre_model_path = '/home/zglg/SLU/psd/pre-model/chinese-gsdsimp-ud-2.5-191206.udpipe'
    # # # corpus for @language_name
    # # corpus_filepath = '/home/zglg/SLU/psd/corpus/chinese/平凡的世界.txt'
    # # # there are rules for word2vec file_path, please following:
    # # file_path = '/home/zglg/SLU/psd/cluster_pre_train/gensim-word2vec-model-'
    #
    # parser = argparse.ArgumentParser(description='feature corpus to get our word2vec for multiple languages')
    # parser.add_argument('-udfp', help='udpipe pre-model filepath')
    # parser.add_argument('-cfp', help='corpus filepath for a specific language')
    # parser.add_argument('-wvfp', help='word vector filepath after finishing feature')
    # args = parser.parse_args()
    # if 'udfp' in args:
    #     udpipe_pre_model_path = args.udfp
    # else:
    #     print('please input udpipe pre-model filepath')
    # if 'cfp' in args:
    #     corpus_filepath = args.cfp
    # else:
    #     print('please input corpus filepath')
    # if 'wvfp' in args:
    #     file_path = args.wvfp
    # else:
    #     print('please input word vector filepath')
    #
    # # first loading udpipe to segement word for each sentence
    # udt_english = UdpipeTrain(languange_name, udpipe_pre_model_path, corpus_filepath)
    # # second feature to get the word2vec model
    # train_model(languange_name, corpus_filepath, file_path, udpipe_pre_model_path)
    # # finally, after feature we can load model to use directly
    # # load_model(file_path)
    # print('All done')
