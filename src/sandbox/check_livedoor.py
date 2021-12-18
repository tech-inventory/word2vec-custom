"""
    Livedoor コーパス読み込みの試験

"""

import argparse

from reader.corpus.livedoor import LivedoorCorpusReader


def get_options():
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input-livedoor-data',
                        default='corpus/livedoor')

    args = parser.parse_args()
    return vars(args)


def main():
    """
    Livedoorコーパスを読み込む実験。
    :return:
    """
    options = get_options()
    print(options)
    lcreader = LivedoorCorpusReader(base_path=options['input_livedoor_data'])
    for _id, _text in lcreader:
        print(f'category = {_id}')
        print(f'{_text[0:100]} ...')
        print("- " * 35)


if __name__ == '__main__':
    main()
