"""
    テキストベクトルエンコーダーモジュール
    与えられたテキストを word2vec モデルを使って埋め込みベクトル表現に変換する。
"""
import numpy as np

from gensim.models.keyedvectors import KeyedVectors
from parser.mecab import Tagger

MECAB_TAGGER = Tagger()


class TextVectorEncoder(object):
    """
    テキストをベクトルに変換するクラス
    """
    _wv = None

    def __init__(self, wv):
        """
        コンストラクタ
        WordVector インスタンスを指定する。
        :param wv: word2vec モデルの WordVector インスタンス
        """
        self._wv = wv  # type: KeyedVectors

    def encode(self, text, use_prototype=False):
        """
        テキストを受け取り、埋め込みベクトル表現に変換する。
        :param text: テキスト
        :param use_prototype: 基本形（原形）を使用するかどうか
        :return:
        """
        tokens = MECAB_TAGGER.parse(text)
        vector_buffer = []
        for _token in tokens:
            _word = _token['token']

            # 基本形を使う場合
            if use_prototype is True:
                if _token['prototype'] == '*':
                    _word = _token['token']
                else:
                    _word = _token['prototype']

            if self._wv.has_index_for(_word) is True:
                vector_buffer.append(self._wv.get_vector(_word))

        if len(vector_buffer) > 0:
            return np.mean(np.array(vector_buffer), axis=0)
        else:
            # 該当する単語が一つもなかったらゼロベクトルを返す
            return np.zeros(self._wv.vector_size)
