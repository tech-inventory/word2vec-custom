"""
    Wikipediaコーパスを読むためのモジュール
    - WikiExtractor の処理結果を読み込む

"""

import json
import os


class WikipediaCorpusReader(object):
    """
        WikiExtractor の出力結果を格納するディレクトリを指定し、そこからWikipedia抽出結果を1レコードずつ、
        ディレクトリ・ファイルを横断で読み込む。
    """
    def __init__(self, read_path):
        """
            コンストラクタ。
            WikiExtractor の出力結果を格納するディレクトリを指定する。
        :param read_path: WikiExtractor の出力結果を格納するディレクトリ
        """
        self._base_path = read_path

    def __iter__(self):
        """
            WikiExtractor の結果を1行ずつ読み込む。
        :return:
        """
        for _root, _dirs, _files in os.walk(self._base_path):
            if len(_files) > 0:
                for _file in _files:
                    _path = os.path.join(_root, _file)
                    print(f'Processing {_path} ...')
                    with open(_path, 'r') as fp:
                        while True:
                            _line = fp.readline()
                            if len(_line) == 0:
                                break
                            yield json.loads(_line)
