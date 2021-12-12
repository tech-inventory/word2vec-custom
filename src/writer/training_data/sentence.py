"""
    学習データの書き出し処理 : 文単位の学習データ
"""
import os


class SentenceTrainingdataWriter(object):
    """
        Wikipedia 用の学習データ出力クラス
    """

    def __init__(self, write_path, buffer_size=104857600):
        """
            コンストラクタ。
            出力先を指定する。

        :param write_path: 出力先
        :param buffer_size: バッファリングサイズ(単位:byte)
        """
        self.write_path = write_path
        self.buffer_size = buffer_size
        self.writing_number = 0  # 分割出力する際のファイル番号
        self.file_name_template = 'wiki_sentences_{number}.txt'  # 出力ファイル名の書式
        self.current_buffer = ''   # 現在のバッファ

    def write(self, sentence):
        """
            １つの文を表すトークン列を指定し、1行書き出す。
            トークン列は、必ずフィルタ後のモノを使うこと。(トークンの属性に`processed`という値が付与されている）
        :param sentence:
        :return:
        """
        if type(sentence) in [list, tuple]:
            self.current_buffer += [_['processed'] for _ in sentence]
            if len(self.current_buffer) > self.buffer_size:
                self.flush_buffer()

    def flush_buffer(self):
        """
            バッファリングした内容を書き出す。
        :return:
        """
        _file_path = os.path.join(self.write_path, self.file_name_template.format(number=self.writing_number))
        with open(_file_path, 'w') as fp:
            fp.write(self.current_buffer)

        self.current_buffer = ''
        self.writing_number += 1










