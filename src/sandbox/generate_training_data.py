"""
    WikiExtractor の出力結果を読み込み、学習用データを出力するプロトタイプ
    後に、コードを整理してパイプラインコードに昇格する予定。

"""

import argparse
import json
import pprint
from parser.mecab import Tagger
from tqdm import tqdm
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

    def __init__(self, corpus_reader, data_writer):
        """
        コンストラクタ
        学習データの出力先は data_writer の方で指定する。
        :param corpus_reader: コーパスを読み込むオブジェクト
        :param data_writer: 学習データの出力オブジェクト
        """
        self._reader = corpus_reader
        self._writer = data_writer

    def generate_training_data(self):
        """
        学習データ生成処理
        :return:
        """
        loop_count = 0
        for _corpus in tqdm(self._reader):
            _sentences = str(_corpus['text']).split("\n")
            for _sen in _sentences:
                if _sen.startswith('[[File:') and _sen.endswith(']]'):
                    # skipping image tag
                    continue

                _filtered = filter_token(text=_sen)
                if _filtered is not None:
                    self._writer.write(_filtered)
            loop_count += 1
        # 残っているバッファも書き出す
        self._writer.flush_buffer()



def get_options():
    parser = argparse.ArgumentParser()

    parser.add_argument('-o', '--output-training-data-path',
                        default='training_data/wikipedia')

    parser.add_argument('-i', '--input-corpus-path',
                        default='corpus/wikipedia/extracted')

    args = parser.parse_args()
    return vars(args)


def main():
    """
    WikiExtractor の抽出結果を読み込み、フィルタリングして、学習用データを出力する。
    :return:
    """
    options = get_options()
    print(options)
    wiki_reader = WikipediaCorpusReader(read_path=options['input_corpus_path'])
    data_writer = SentenceTrainingdataWriter(write_path=options['output_training_data_path'], buffer_size=(1024 * 1024 * 100))
    data_generator = TrainingDataGenerator(corpus_reader=wiki_reader, data_writer=data_writer)
    data_generator.generate_training_data()

if __name__ == '__main__':
    main()
