"""
    ライブドアコーパスを扱うモジュール

"""

import os


class LivedoorCorpusReader(object):
    """
        ライブドアコーパスを読み込むためのクラス
    """
    def __init__(self, base_path):
        """
        ライブドアコーパスを展開したディレクトリのパスを指定する。
        :param base_path: ライブドアコーパスを展開したディレクトリのパス
        """
        self._base_path = base_path
        self._category_map = {}
        self.generate_category_map()

    def generate_category_map(self):
        """
        ディレクトリ（＝カテゴリ）の対応関係を生成する。
        :return:
        """
        category_list = []
        for _dir in os.listdir(self._base_path):
            if os.path.isdir(f'{self._base_path}/{_dir}'):
                category_list.append(_dir)

        for _category_id, _category_name in enumerate(category_list):
            self._category_map[_category_name] = _category_id

    def __iter__(self):
        """
            ライブドアコーパスを1件ずつ読み込む。
        :return:
        """
        for _dir, _category_id in self._category_map.items():
            _scan_path = f'{self._base_path}/{_dir}'
            for _root, _dirs, _files in os.walk(_scan_path):
                if len(_files) > 0:
                    for _file in _files:
                        _path = os.path.join(_root, _file)
                        with open(_path, 'r') as fp:
                            _body = fp.read()
                            _lines = _body.split('\n')[3:]
                        yield _category_id, '\n'.join(_lines)
