"""
    入力されたテキストを形態素（＝トークン）に分割し、それを選別した結果を返す。
"""
from parser.mecab import Tagger
mecab_tagger = Tagger()

exclude_pos_config = ('格助詞', '読点', '係助詞', '句点', '接続助詞', '代名詞',
                      '括弧開', '括弧閉', '並立助詞', '連体化', '副助詞', '副助詞／並立助詞／終助詞')

def is_exclude(token):
    """
    形態素1個のトークン情報を受け取り、除外対象か判定する。
    :param token:
    :return: 判定結果(True/False)
    """
    has_exclude = False
    if token['pos_category_1st'] in exclude_pos_config:
        has_exclude = True

    if token['pos_category_1st'] == '自立':
        if token['prototype'] in ('する', 'なる', 'なす', 'できる', 'ある', 'いる'):
            has_exclude = True

    if token['pos_category_1st'] == '一般':
        if token['prototype'] in ('・'):
            has_exclude = True

    if token['pos_category_1st'] == '接尾':
        if token['prototype'] in ('れる', 'られる', 'せる'):
            has_exclude = True

    if token['pos_category_1st'] == '非自立':
        if token['prototype'] in ('いる', 'にくい', 'おる', 'の'):
            has_exclude = True

    if token['pos_type'] == '名詞':
        if token['pos_category_1st'] == '非自立':
            if token['prototype'] in ('ため', 'よう', 'もの', 'こと'):
                has_exclude = True

    if token['pos_type'] == '助動詞':
        if token['prototype'] in ('だ', 'ある', 'た', 'ない', 'ぬ'):
            has_exclude = True

    if token['pos_type'] == '接続詞':
        has_exclude = True

    return has_exclude

def filter(text: str):
    """
    テキストを受け取り、形態素に分割する
    :param text:
    :return:
    """
    filtered = []
    parse_results = mecab_tagger.parse(text)
    for _token in parse_results:
        _processed = ''
        # 品詞カテゴリ１が除外対象 だったら表示しない
        if is_exclude(_token) is not True:
            # 基本形を優先的に採用する
            if _token['prototype'] != '*':
                _processed = _token['prototype']
            else:
                _processed = _token['token']
            # print(f'{_processed}', end=' ')
            _token['processed'] = _processed
            filtered.append(_token)
    return filtered
