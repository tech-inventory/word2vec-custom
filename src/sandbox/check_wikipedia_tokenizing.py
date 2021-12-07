"""
    Wikipedia の抽出結果を形態素に分割し、分析する

"""

import json
import pprint
from parser.mecab import Tagger
mecab_tagger = Tagger()

exclude_pos_config = ("格助詞", "読点", "係助詞", "句点", "接続助詞", "代名詞",
                      "括弧開", "括弧閉", "並立助詞", "連体化", '副助詞')

def is_exclude(token):
    """
    形態素1個のトークン情報を受け取り、除外対象か判定する。
    :param token:
    :return:
    """
    has_exclude = False
    if token['pos_category_1st'] in exclude_pos_config:
        has_exclude = True

    if token['pos_category_1st'] == '自立':
        if token['prototype'] in ('する', 'なる', 'なす', 'できる', 'ある'):
            has_exclude = True

    if token['pos_category_1st'] == '一般':
        if token['prototype'] in ('・'):
            has_exclude = True

    if token['pos_category_1st'] == '接尾':
        if token['prototype'] in ('れる'):
            has_exclude = True

    if token['pos_category_1st'] == '非自立':
        if token['prototype'] in ('いる', 'よう', 'にくい'):
            has_exclude = True

    if token['pos_type'] == '助動詞':
        if token['prototype'] in ('だ', 'ある', 'た', 'ない'):
            has_exclude = True



    return has_exclude

def parse(text: str):
    """
    テキストを受け取り、形態素に分割する
    :param text:
    :return:
    """
    parse_results = mecab_tagger.parse(text)
    # pprint.pprint(parse_results)
    for _token in parse_results:
        _processed = ''
        # 品詞カテゴリ１が除外対象 だったら表示しない
        if is_exclude(_token) is not True:
            # 基本形を優先的に採用する
            if _token['prototype'] != '*' :
                _processed = _token['prototype']
            else:
                _processed = _token['token']
            print(f'{_processed}', end=' ')
            # print(f'{_processed}({_token["pos_category_1st"]}) ', end=' ')
            # print(_token)




def main():
    """
    WikiExtractor の抽出結果(JSONL形式)を試験的に表示する。
    :return:
    """
    extract_path = "../corpus/wikipedia/extracted/AA/wiki_00"
    with open(extract_path, 'r') as fp:
        view_count = 0
        while True:
            _line = fp.readline()
            # print(_line)
            _parsed = json.loads(_line)
            pprint.pprint(_parsed)

            _sentences = str(_parsed['text']).split("\n")
            for _sen in _sentences:
                print(_sen)
                parse(_sen)
                print("\n")
                print('=' * 70)
            view_count += 1
            if view_count > 1:
                break


if __name__ == '__main__':
    main()
