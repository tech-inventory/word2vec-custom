"""
    Wikipedia の抽出結果を形態素に分割し、高頻度で出現するトークンの情報を表示する。

"""

import json
import pprint
from parser.mecab import Tagger
from typing import List

MECAB_TAGGER = Tagger()

class TokenAggregator:
    """
    トークンの出現頻度を計上する為のクラス。
    トークンの属性情報も保持するのがポイント（後で、トークンのトリミング処理の設定として参照する等の用途あり）
    """

    def __init__(self):
        """
        コンストラクタ
        """

        # トークンの出現頻度を記録する
        # キーは、トークンの基本形(無い場合は トークン) + 品詞種別
        self.aggregation_map = {}

        # トークンの属性情報を保持する。
        # キーは、トークンの基本形(無い場合は トークン) + 品詞種別
        self.token_attributions = {}

    def _get_key(self, token:dict):
        """
        トークンを受け取り、集計用のキーを返す。
        トークンの構造は parser.mecab を参照。
        :param token:
        :return: 集計用のキー
        """
        _token = token.get('token')
        _prototype = token.get('prototype')
        _pos_type = token.get('pos_type')
        if _token is not None:
            _agg_key = token.get('token')
            if _prototype is not None:
                _agg_key = _prototype

            if _pos_type is not None:
                _agg_key += f'_{_pos_type}'
            return _agg_key
        else:
            return None

    def aggregate(self, tokens: List[dict]):
        """
        複数のトークンを受け取り集計作業を行う
        :param tokens:
        :return:
        """
        if len(tokens) > 0:
            for _token in tokens:
                _agg_key = self._get_key(_token)
                if _agg_key is not None:
                    if self.aggregation_map.get(_agg_key) is None:
                        self.aggregation_map[_agg_key] = 1
                        self.token_attributions[_agg_key] = _token
                    else:
                        self.aggregation_map[_agg_key] += 1


    def parse(self, text: str):
        """
        テキストを受け取り、形態素に分割し、集計する
        :param text:
        :return:
        """
        parse_results = MECAB_TAGGER.parse(text)
        self.aggregate(parse_results)


    def pickup_frequent_ones(self, n=10):
        """
        出現頻度上位N件をピックアップ
        :return:
        """
        _sorted_index = sorted(self.aggregation_map.items(), key=lambda x:x[1], reverse=True)
        _ranked_index = _sorted_index[0:n]
        for _ranked in _ranked_index:
            print(f'{_ranked[0]} : {_ranked[1]}')
            pprint.pprint(self.token_attributions[_ranked[0]])
            print('-' * 70)





def main():
    """
    WikiExtractor の抽出結果(JSONL形式)を試験的に表示する。
    :return:
    """
    token_aggregator = TokenAggregator()
    extract_path = "../corpus/wikipedia/extracted/AA/wiki_00"
    with open(extract_path, 'r') as fp:
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
