from sklearn.externals import joblib
import base as bs
import pandas as pd
import os


def load_model():
    """
    load model from directory
    :return:
    """
    clf = joblib.load(os.path.join(bs.model_path, 'model.m'))
    scale = joblib.load(os.path.join(bs.model_path, 'scale.m'))
    return clf, scale


def get_features_list():
    """
    get the features we used in training the model
    :return:
    """
    df = pd.read_csv(bs.features_path)
    if 'vas_score' in df.columns.values:
        del df['vas_score']
    return df.columns.values


def predict():
    """
    predict vas
    :param all_inone_path:
    :return:
    """
    clf, scale = load_model()
    df = pd.read_csv(bs.get_save_whole_name('all_inone.csv'))
    if 'Unnamed: 0' in df.columns.values:
        del df['Unnamed: 0']

    _list = get_features_list()
    df = df[_list]
    x = df.loc[0].values
    x = scale.transform([x])
    vas = clf.predict(x)
    return vas[0]
