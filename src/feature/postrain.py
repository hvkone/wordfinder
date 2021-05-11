# encoding: utf-8
"""
@file: postrain.py
@desc: this module is mainly used to feature our corpus
to get the word, POS, and related sentence
according to udpipe pre-feature modules

@author: group3
@time: 2/25/2021
"""

import string
import re
from corpy.udpipe import Model
from typing import List

from src.feature.posbase import ITrain
from src.feature.pos import TResult
from src.feature.store import StoreData
from src.config import language_list, db_config, corpus_language, udpipe_language
from src.logs import Log

log = Log()


class UdpipeTrain(ITrain):
    def __init__(self, language_name, pre_model_name, our_corpus_name, db_conn=None):
        """
        The language of pre_model_name and our_corpus_name should be identical!
        :param language_name:
        :param pre_model_name: it's from udpipe
        :param our_corpus_name: it's our found
        :@param db_conn: database connection
        """
        self.language_name = language_name
        self.pre_model_name = pre_model_name
        self.our_corpus_name = our_corpus_name
        try:
            if db_conn is None:
                self.store_data = StoreData(db_config['user'],
                                            db_config['password'],
                                            db_host=db_config['host'],
                                            db_name=db_config['database'])
                self.cursor = self.store_data.db_connect().cursor()
            # second loading udpipe pre-feature model
            self.model = Model(self.pre_model_name)
            self._word_count, self.MAX_WORD_COUNT = 0, 500000
        except Exception as ex:
            log.error('logging in database error %s' % ex)

    def load_data(self) -> str:
        with open(self.our_corpus_name, 'r', encoding='utf-8') as f:
            for sent in f:
                log.info('loading one sentence: %s' % (sent,))
                yield sent

        log.info('loading done for our corpus')

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
        cleaned_data = re.compile(r"[\!\@\#\$\%\^\&\*\(\)\-\=\[\]\{\}\\\|;"
                                  r"\'\:\"\,\.\/\<\>\?\/\*\+"u"]+").sub('', data)
        return cleaned_data

    def do_train(self) -> List[TResult]:
        """
        By pre-feature modules of unpipe get the results for our corpus
        These udpipe modules can be download here:
        https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-3131
        :return:
        """
        # feature our corpus to get POS for each word
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
        log.info(' all written succeed for corpus of %s' % self.our_corpus_name)

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
            log.error('error: not find a sentence %s' % (e, ))
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
            words.extend([res.word for res in results][1:])
        return words


def batch_train():
    for lang in language_list:
        udpipe_pre_model_path = udpipe_language[lang]
        corpus_filepath = corpus_language[lang]
        train_model = UdpipeTrain(lang, udpipe_pre_model_path, corpus_filepath)
        log.info('begin feature %s corpus' % (lang,))
        train_model.do_train()
        log.info('done feature %s corpus' % (lang,))


if __name__ == '__main__':
    batch_train()
    # parser = argparse.ArgumentParser(description='feature corpus to get word, pos, and related sentence')
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
