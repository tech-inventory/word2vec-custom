"""
    WikiExtractor の出力結果を読み込み、学習用データを出力するプロトタイプ
    後に、コードを整理してパイプラインコードに昇格する予定。

"""

import argparse
import json
import pprint
from parser.mecab import Tagger
from typing import List

from filter.token import filter_token
from reader.corpus.wikipedia import WikipediaCorpusReader
from writer.training_data.sentence import SentenceTrainingdataWriter

MECAB_TAGGER = Tagger()


class TrainingDataGenerator(object):
    """
    学習データ生成処理のクラス。
    reader, writer を受け取ることで、処理を汎用化できるんじゃなかろうか。
    """

    def __init__(self, output_path : str, corpus_reader, data_writer):
        """
        コンストラクタ
        :param output_path: 生成した学習データの出力先のパス
        :param corpus_reader: コーパスを読み込むオブジェクト
        :param data_writer: 学習データの出力オブジェクト
        """
        self.output_path = output_path
        self._reader = corpus_reader
        self._writer = data_writer

    def generate_training_data(self):
        """
        学習データ生成処理
        :return:
        """
        for _corpus in self._reader:
            _sentences = str(_corpus['text']).split("\n")
            for _sen in _sentences:
                if _sen.startswith('[[File:') and _sen.endswith(']]'):
                    # skipping image tag
                    continue

                _filtered = filter_token(text=_sen)
                if _filtered is not None:
                    self._writer.write(_filtered)

        # 残っているバッファも書き出す
        self._writer.flush_buffer()



def get_options():
    parser = argparse.ArgumentParser()

    parser.add_argument('-o', '--output-training-data-path',
                        default='training_data/wikipedia')

    parser.add_argument('-i', '--input-corpus-path',
                        default='corpus/wikipedia/extracted')

    parser.add_argument('--size', type=int, default=100)

    args = parser.parse_args()
    return vars(args)


def main():
    """
    WikiExtractor の抽出結果を読み込み、フィルタリングして、学習用データを出力する。
    :return:
    """
    options = get_options()
    token_aggregator = TokenAggregator()

    # コーパスの一部をサンプリング
    corpus_files = ['../corpus/wikipedia/extracted/AA/wiki_00',
                    '../corpus/wikipedia/extracted/AA/wiki_01',
                    '../corpus/wikipedia/extracted/AA/wiki_02',
                    '../corpus/wikipedia/extracted/AA/wiki_03',
                    '../corpus/wikipedia/extracted/AA/wiki_04',
                    '../corpus/wikipedia/extracted/AA/wiki_05',
                    '../corpus/wikipedia/extracted/AA/wiki_06',
                    '../corpus/wikipedia/extracted/AA/wiki_07',
                    '../corpus/wikipedia/extracted/AA/wiki_08',
                    '../corpus/wikipedia/extracted/AA/wiki_09'
                    ]

    # extract_path = "../corpus/wikipedia/extracted/AA/wiki_00"
    for _extract_path in corpus_files:
        print(f'Processing {_extract_path} ...')
        with open(_extract_path, 'r') as fp:
            view_count = 0
            while True:
                _line = fp.readline()
                if len(_line) == 0:
                    break

                _parsed = json.loads(_line)
                token_aggregator.parse(_parsed['text'])
    token_aggregator.pickup_frequent_ones(n=100)

if __name__ == '__main__':
    main()
