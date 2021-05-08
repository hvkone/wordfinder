# encoding: utf-8
"""
@file: pos_model.py
@desc: this module is mainly used to train our corpus
to get the word, POS, and related sentence
according to udpipe pre-train modules

@author: group3
@time: 2/25/2021
"""

import string
import re
import argparse
from corpy.udpipe import Model
from typing import List

from src.train.base_model import ITrain
from src.train.result_model import TResult
from src.train.store_model import StoreData
from src.util import language_list, db_config, corpus_language, udpipe_language


class UdpipeTrain(ITrain):
    def __init__(self, language_name, pre_model_name, our_corpus_name):
        """
        The language of pre_model_name and our_corpus_name should be identical!
        :param language_name:
        :param pre_model_name: it's from udpipe
        :param our_corpus_name: it's our found
        """
        self.language_name = language_name
        self.pre_model_name = pre_model_name
        self.our_corpus_name = our_corpus_name
        try:
            self.store_data = StoreData(db_config['user'],
                                        db_config['password'],
                                        db_host=db_config['db_host'],
                                        db_name=db_config['db_name'])
            self.cursor = self.store_data.db_connect().cursor()
            # second loading udpipe pre-train model
            self.model = Model(self.pre_model_name)
            self._word_count, self.MAX_WORD_COUNT = 0, 500000
        except Exception as ex:
            print('logging in database error %s' % ex)

    def load_data(self) -> str:
        with open(self.our_corpus_name, 'r', encoding='utf-8') as f:
            for sent in f:
                print('loading one sentence: %s' % (sent,))
                yield sent

        print('loading done for our corpus')

    def clean_data(self, data: str) -> str:
        """
        data is one sentence we expected
        Our idea is to use regular expressions to match common words,
        and remove Unicode codes that are out of range.
        compile (U "[^common word range] +") after matching to non range characters
        reference: https://blog.csdn.net/qq_33282586/article/details/80643829
        :param data: raw data
        :return: data after cleaning
        """
        cleaned_data = re.compile(u"[^"u"\u4e00-\u9fa5"
                                  u"\u0041-\u005A"
                                  u"\u0061-\u007A"
                                  u"\u0030-\u0039"
                                  u"\u3002\uFF1F\uFF01\uFF0C\u3001\uFF1B\uFF1A\u300C\u300D"
                                  u"\u300E\u300F\u2018\u2019\u201C\u201D\uFF08\uFF09\u3014"
                                  u"\u3015\u3010\u3011\u2014\u2026\u2013\uFF0E\u300A\u300B\u3008\u3009"
                                  u"\!\@\#\$\%\^\&\*\(\)\-\=\[\]\{\}\\\|;"
                                  u"\'\:\"\,\.\/\<\>\?\/\*\+"u"]+").sub('', data)
        return cleaned_data

    def do_train(self) -> List[TResult]:
        """
        By pre-train modules of unpipe get the results for our corpus
        These udpipe modules can be download here:
        https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-3131
        :return:
        """
        # train our corpus to get POS for each word
        line_no = 1
        for sen in self.load_data():
            if self._word_count > self.MAX_WORD_COUNT:
                return
            sen_clean = self.clean_data(sen)
            if not sen_clean:
                continue
            word_pos = list(self.model.process(sen_clean))
            for i, one_sentence in enumerate(word_pos):
                sentence_text = self.extract_one_sentence(one_sentence)
                results = self.extract_one_word(one_sentence, sentence_text)
                self.store_data.insert_data(self.cursor, results, self.language_name)
                print('line %d, batch %d for %s written succeed' % (line_no, i, self.language_name))
            line_no += 1
        print(' all written succeed for corpus of %s' % self.our_corpus_name)

    def extract_one_sentence(self, sentence) -> str:
        """
       This private method is mainly used to extract the sentence text.
       an instance of udpipe Sentence:
       :param sentence: udpipe Sentence
       :return: str 黄土高原
       """
        comment = ''.join(sentence.comments)
        try:
            single_sentence = re.findall(r'text = (.*)', comment)[0]
            return single_sentence
        except Exception as e:
            # TODO: need to write warning log
            print('error: not find a sentence', e)
            return ''

    def extract_one_word(self, sentence, sentence_text: str) -> [TResult]:
        """
        This private method is mainly used to extract one word and it's POS
        :param sentence_text:
        :param sentence:
        :return: [TResult]
        """
        combined_words = []
        for word in sentence.words:
            if word.lemma and word.lemma not in string.punctuation:
                if word.lemma and word.upostag and sentence_text:
                    combined_words.append(TResult(word.lemma, word.upostag, sentence_text))
                    self._word_count += 1
        return combined_words

    def word_segmentation(self, sentence) -> List[str]:
        """
        :param sentence:
        :return: word list
        """
        sen_clean = self.clean_data(sentence)
        if not sen_clean:
            return []
        word_pos = list(self.model.process(sen_clean))
        words = []
        for i, one_sentence in enumerate(word_pos):
            sentence_text = self.extract_one_sentence(one_sentence)
            results = self.extract_one_word(one_sentence, sentence_text)
            words.extend([res.word for res in results])
        return words


def batch_train():
    for lang in language_list:
        udpipe_pre_model_path = udpipe_language[lang]
        corpus_filepath = corpus_language[lang]
        train_model = UdpipeTrain(lang, udpipe_pre_model_path, corpus_filepath)
        print('begin train %s corpus' % (lang,))
        train_model.do_train()
        print('done train %s corpus' % (lang,))


if __name__ == '__main__':
    batch_train()
    # parser = argparse.ArgumentParser(description='train corpus to get word, pos, and related sentence')
    # parser.add_argument('-udfp', help='udpipe pre-model filepath')
    # parser.add_argument('-cfp', help='corpus filepath for a specific language')
    # args = parser.parse_args()
    # if 'udfp' in args:
    #     udpipe_pre_model_path = args.udfp
    # else:
    #     print('please input udpipe pre-model filepath')
    # if 'cfp' in args:
    #     corpus_filepath = args.cfp
    # else:
    #     print('please input corpus filepath')
    #
    # udt_english = UdpipeTrain(language_list[0], udpipe_pre_model_path, corpus_filepath)
    # udt_english.do_train()
