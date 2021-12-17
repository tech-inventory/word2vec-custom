"""
    学習したモデルを読み込み、動作を検証する。

"""

import argparse
import json
import pprint
from parser.mecab import Tagger
from tqdm import tqdm
from typing import List

from gensim.models.callbacks import CallbackAny2Vec
from gensim.models.word2vec import PathLineSentences
from gensim.models.word2vec import Word2Vec

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


def main():
    """
    :return:
    """
    options = get_options()
    print(options)

    model = Word2Vec.load(options['model_path'])
    print('データサイエンス')
    pprint.pprint(model.wv.most_similar('データサイエンス', topn=10))

    print('機械学習')
    pprint.pprint(model.wv.most_similar('機械学習', topn=10))

    print('東京 - 日本 + フランス')
    pprint.pprint(model.wv.most_similar(positive=['東京', 'フランス'], negative=['日本'], topn=10))

    print('東京 - 日本 + 米国')
    pprint.pprint(model.wv.most_similar(positive=['東京', '米国'], negative=['日本'], topn=10))

    print('庶民 + お金')
    pprint.pprint(model.wv.most_similar(positive=['庶民', 'お金'], topn=10))

    print('庶民 + お金 + 勉強')
    pprint.pprint(model.wv.most_similar(positive=['庶民', 'お金', '勉強'], topn=10))

    print('スポーツ + ボール + バット')
    pprint.pprint(model.wv.most_similar(positive=['スポーツ', 'ボール', 'バット'], topn=10))

    print('ユーチューバー')
    pprint.pprint(model.wv.most_similar(positive=['ユーチューバー'], topn=10))

    print('YouTuber')
    pprint.pprint(model.wv.most_similar(positive=['YouTuber'], topn=10))

    print('ユーチューバー + 筋トレ')
    pprint.pprint(model.wv.most_similar(positive=['ユーチューバー', '筋トレ'], topn=10))

    print('筋トレ')
    pprint.pprint(model.wv.most_similar(positive=['筋トレ'], topn=10))

    print('YouTuber + 筋トレ')
    pprint.pprint(model.wv.most_similar(positive=['YouTuber', '筋トレ'], topn=10))

    print('深層学習')
    pprint.pprint(model.wv.most_similar(positive=['深層学習'], topn=10))


if __name__ == '__main__':
    main()
