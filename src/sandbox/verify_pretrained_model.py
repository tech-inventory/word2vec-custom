"""
    事前学習したモデルを読み込み、動作を検証する。

"""

import argparse
import json
import pprint
import pickle
from parser.mecab import Tagger
from tqdm import tqdm
from typing import List

from gensim.models.callbacks import CallbackAny2Vec
from gensim.models.word2vec import PathLineSentences
from gensim.models.keyedvectors import load_word2vec_format
from gensim.models.word2vec import Word2Vec
from gensim.models.word2vec import KeyedVectors
from gensim.models import keyedvectors

from encoder.vector.text import TextVectorEncoder
from filter.token import filter_token
from reader.corpus.wikipedia import WikipediaCorpusReader
from writer.training_data.sentence import SentenceTrainingdataWriter

MECAB_TAGGER = Tagger()

def get_options():
    parser = argparse.ArgumentParser()

    parser.add_argument('-m', '--model-path',
                        default='models/ja-wikipedia')

    args = parser.parse_args()
    return vars(args)

def load_model(model_path):
    """
    事前学習モデルの読み込み(TSV)
    :param model_path:
    :return:
    """
    wv = {}
    with open(model_path, 'r') as fp:
        while True:
            _line = fp.readline()
            if len(_line) > 0:
                _chunk = _line.split('\t')
                pprint.pprint(_chunk)
                _word = _chunk[1]
                _vector = json.loads(_chunk[2])
                wv[_word] = _vector
            else:
                break
    return wv


def load_pickle(model_path):
    """
    事前学習モデルの読み込み(TSV)
    :param model_path:
    :return:
    """
    model = None
    with open(model_path, 'r') as fp:
        model = pickle.load(fp)
    pprint(dir(model))
    


def main():
    """
    :return:
    """
    options = get_options()
    print(options)

    # 東北大学乾研究室謹製のモデルは、ちゃんと読み込めた。
    wv = load_word2vec_format(options['model_path'], binary=False)
    #model = Word2Vec.load(options['model_path'])
    # load_pickle(options['model_path'])
    #wv = load_model(options['model_path'])

    print('データサイエンス')
    pprint.pprint(wv.most_similar('データサイエンス', topn=10))

    print('機械学習')
    pprint.pprint(wv.most_similar('機械学習', topn=10))

    print('東京 - 日本 + フランス')
    pprint.pprint(wv.most_similar(positive=['東京', 'フランス'], negative=['日本'], topn=10))

    print('東京 - 日本 + 米国')
    pprint.pprint(wv.most_similar(positive=['東京', '米国'], negative=['日本'], topn=10))

    print('庶民 + お金')
    pprint.pprint(wv.most_similar(positive=['庶民', 'お金'], topn=10))

    print('庶民 + お金 + 勉強')
    pprint.pprint(wv.most_similar(positive=['庶民', 'お金', '勉強'], topn=10))

    print('スポーツ + ボール + バット')
    pprint.pprint(wv.most_similar(positive=['スポーツ', 'ボール', 'バット'], topn=10))

    print('ユーチューバー')
    pprint.pprint(wv.most_similar(positive=['ユーチューバー'], topn=10))

    print('YouTuber')
    pprint.pprint(wv.most_similar(positive=['YouTuber'], topn=10))

    print('ユーチューバー + 筋トレ')
    pprint.pprint(wv.most_similar(positive=['ユーチューバー', '筋トレ'], topn=10))

    print('筋トレ')
    pprint.pprint(wv.most_similar(positive=['筋トレ'], topn=10))

    print('YouTuber + 筋トレ')
    pprint.pprint(wv.most_similar(positive=['YouTuber', '筋トレ'], topn=10))

    print('深層学習')
    pprint.pprint(wv.most_similar(positive=['深層学習'], topn=10))

    # ベクトル変換試験
    tvencoder = TextVectorEncoder(wv=wv)
    vector_sample = tvencoder.encode('機械学習と深層学習の対応関係について考察してみる')
    print(vector_sample)

if __name__ == '__main__':
    main()
