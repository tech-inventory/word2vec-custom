"""
    Livedoor コーパス読み込みの試験
    カスタムにビルドした word2vec モデルの性能を評価する
"""

import argparse
import numpy as np

from gensim.models.keyedvectors import load_word2vec_format
from gensim.models.word2vec import Word2Vec
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from tqdm import tqdm

from encoder.vector.text import TextVectorEncoder
from reader.corpus.livedoor import LivedoorCorpusReader


def get_options():
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input-livedoor-data',
                        default='corpus/livedoor')

    parser.add_argument('-m', '--model-path',
                        default='models/ja-wikipedia')

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

    model = Word2Vec.load(options['model_path'])

    # ベクトル変換試験
    tvencoder = TextVectorEncoder(wv=model.wv)

    # データセット準備
    X_buffer = []
    Y_buffer = []
    text_buffer = []
    for _id, _text in tqdm(lcreader):
        Y_buffer.append(_id)
        X_buffer.append(tvencoder.encode(_text, use_prototype=True))
        text_buffer.append(_text)

    X = np.array(X_buffer)
    Y = np.array(Y_buffer)

    X_train, X_test, Y_train, Y_test, text_train, text_test = train_test_split(X,
                                                        Y,
                                                        text_buffer,
                                                        test_size=0.2,
                                                        random_state=40)

    clf_svm = make_pipeline(StandardScaler(), svm.SVC(gamma='auto'))
    clf_svm.fit(X_train, Y_train)
    predicted = clf_svm.predict(X_test)

    print('Accuracy: ', accuracy_score(Y_test, predicted))
    print(classification_report(Y_test, predicted))

    # しくじったケースの表示
    for _y_pred, _y_true, _text in zip(predicted, Y_test, text_test):
        if _y_pred != _y_true:
            _cat_pred = lcreader.get_category_name(_y_pred)
            _cat_true = lcreader.get_category_name(_y_true)
            print(f'[x] 予測 f{_cat_pred}   正解{_cat_true}')
            print(_text)
            print('=' * 80)

    # ロジスティック回帰
    clf_lg = LogisticRegression(max_iter=1000)
    clf_lg.fit(X_train, Y_train)
    predicted = clf_lg.predict(X_test)

    print('Accuracy: ', accuracy_score(Y_test, predicted))
    print(classification_report(Y_test, predicted))

if __name__ == '__main__':
    main()
