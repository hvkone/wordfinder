# encoding: utf-8
"""
@file: pos.py
@desc: This module mainly supports result models
after executing postrain.py
@author: group3
@time: 3/25/2021
"""


class TResult(object):
    def __init__(self, word: str, pos_tag: str, sentence: str):
        """
        Construction function for result after training(postrain.py module)
        :param word: word
        :param pos_tag: tag info
        :param sentence: sentence with this word
        """
        self.word = word
        self.pos_tag = pos_tag
        self.sentence = sentence

