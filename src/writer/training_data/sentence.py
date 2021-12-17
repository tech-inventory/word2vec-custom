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
        self.current_buffer = []   # 現在のバッファ
        self.current_buffer_size = 0

    def write(self, filtered_tokens):
        """
            １つの文を表すトークン列を指定し、1行書き出す。
            トークン列は、必ずフィルタ後のモノを使うこと。(トークンの属性に`processed`という値が付与されている）
        :param filtered_tokens:
        :return:
        """
        if type(filtered_tokens) in [list, tuple]:
            if len(filtered_tokens) > 0:
                _sentence = ' '.join([_['processed'] for _ in filtered_tokens])
                self.current_buffer.append(_sentence)
                self.current_buffer_size += len(_sentence) + 1
                if self.current_buffer_size > self.buffer_size:
                    self.flush_buffer()

    def flush_buffer(self):
        """
            バッファリングした内容を書き出す。
        :return:
        """
        _file_path = os.path.join(self.write_path, self.file_name_template.format(number=self.writing_number))
        with open(_file_path, 'w') as fp:
            fp.write('\n'.join(self.current_buffer))
            print(f'wrote training data : {_file_path} , {self.current_buffer_size} bytes')

        self.current_buffer = []
        self.current_buffer_size = 0
        self.writing_number += 1










