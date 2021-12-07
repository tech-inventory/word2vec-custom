"""
    Wikipedia の抽出結果を閲覧する

"""

import json
import pprint


def main():
    """
    WikiExtractor の抽出結果(JSONL形式)を試験的に表示する。
    :return:
    """
    extract_path = "./corpus/wikipedia/extracted/AA/wiki_00"
    with open(extract_path, 'r') as fp:
        view_count = 0
        while True:
            _line = fp.readline()
            # print(_line)
            _parsed = json.loads(_line)
            pprint.pprint(_parsed)
            view_count += 1
            if view_count > 10:
                break


if __name__ == '__main__':
    main()
