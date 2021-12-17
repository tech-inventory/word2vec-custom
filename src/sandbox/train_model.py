"""
    学習用データを読み込み、モデルの学習をするプロトタイプコード
    後に、コードを整理してパイプラインコードに昇格する予定。

"""

import argparse
import json
import pprint
from datetime import datetime
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


class TrainingCallback(CallbackAny2Vec):
    """
    word2vec 学習時のコールバッククラス
    """

    def __init__(self, model_path):
        """
        コンストラクタ
        :param model_path: 学習モデルの出力先パス（拡張子は含まないこと）
        """
        self._model_path = model_path
        self._epoch = 0

    def on_epoch_begin(self, model: Word2Vec):
        """
        各学習エポック開始時の処理
        :param model:
        :return:
        """
        _dt = datetime.now()
        print(f'{str(_dt)} [Training] epoch = {self._epoch} start')
        pass

    def on_epoch_end(self, model: Word2Vec):
        """
        各学習エポック完了時の処理
        :param model:
        :return:
        """
        _dt = datetime.now()
        print(f'{str(_dt)} [Training] epoch = {self._epoch} end')

        # 各エポックごとのモデルを保存する
        _epoch_save_path = f'{self._model_path}_epoch{self._epoch}.model'
        model.save(_epoch_save_path)
        print(f'[Training] saved {_epoch_save_path}')
        self._epoch += 1

    def on_train_begin(self, model):
        """
        学習開始時の処理
        :param model:
        :return:
        """
        _dt = datetime.now()
        print(f'{str(_dt)} training start')

    def on_train_end(self, model):
        """
        学習完了時の処理
        :param model:
        :return:
        """
        # モデル完了時
        _save_path = f'{self._model_path}.model'
        model.save(_save_path)
        _dt = datetime.now()
        print(f'{str(_dt)} [Training] saved {_save_path}')



def get_options():
    parser = argparse.ArgumentParser()

    parser.add_argument('-o', '--output-model-path',
                        default='models/ja-wikipedia')

    parser.add_argument('-i', '--input-training-data',
                        default='training_data/wikipedia')

    args = parser.parse_args()
    return vars(args)


def main():
    """
    WikiExtractor の抽出結果を読み込み、フィルタリングして、学習用データを出力する。
    :return:
    """
    options = get_options()
    print(options)
    training_data_reader = PathLineSentences(source=options['input_training_data'])
    training_callback = TrainingCallback(model_path=options['output_model_path'])

    model = Word2Vec(sentences=training_data_reader,
                     vector_size=100, # 500 は時間がかかりすぎる
                     window=10,  # 20 は、やりすぎ
                     sg=1,
                     min_count=20,
                     hs=0,
                     negative=5,
                     callbacks=[training_callback],
                     epochs=20
                     )

if __name__ == '__main__':
    main()
