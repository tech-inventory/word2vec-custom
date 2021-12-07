"""

  形態素解析モジュール :: Mecab
  日本語文字列をMecabを使って形態素に分割する処理

"""

import MeCab

class Tagger():

  def __init__(self):
    """
    コンストラクタ。
    MeCab の Tagger インスタンスを初期化する。
    """
    self._mecab = MeCab.Tagger()

    # 半角空白対策
    self._spacer = '\u0080'


  def parse_each_line(self, line):
    """
    mecabの解析結果1行を受け取って、構造化して返す。

    :param line:
    :return: 形態素情報
    """
    if len(line) > 0:
      if line[0:3] != 'EOS':
        _token, _info = str(line).split('\t')
        _info_chunk = _info.split(',')

        # 半角空白対策
        if _token == self._spacer:
          _token = ' '

        _parse_result = {'token': _token,
                         'pos_type': _info_chunk[0],
                         'pos_category_1st': _info_chunk[1],
                         'pos_category_2nd': _info_chunk[2],
                         'pos_category_3rd': _info_chunk[3],
                         'prototype': _info_chunk[6],
                         # 'yomi': _info_chunk[7],
                         # 'pronunciation': _info_chunk[8]
                         }
        return _parse_result
      else:
        return None
    else:
      return None

  def parse(self, text):
    """
    受け取ったテキストを解析し、形態素単位に分割する。

    :param text:
    :return:
    """

    # 半角空白対策
    text = text.replace(" ", self._spacer)

    _raw_result = self._mecab.parse(text)
    lines = str(_raw_result).split('\n')

    parsed_result = []
    for _l in lines:
      _tagged = self.parse_each_line(_l)
      if _tagged is not None:
        parsed_result.append(_tagged)

    return parsed_result