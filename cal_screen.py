import pandas as pd
import numpy as np
import base as bs

features = ['duration', 'count', '0-3', '3-6', '6-9',
            '9-12', '12-15', '15-18','18-21','21-24']


def calculate_features(whole_path, date):
    """
    calculate features about screen
    :param whole_path:
    :param date:
    :return:
    """
    day = date
    res = pd.DataFrame(columns=features)
    _feature_dict = {}  # 存放我们想要特征的字典
    for feature in features:
        _feature_dict[feature] = 0  # 开始先全部赋值为0
    df = pd.read_csv(whole_path, header=None)
    for index in df.index:  # 遍历该用户的csv
        #  得到csv的一行
        raw = df.loc[index].values.tolist()
        if str(raw[1]).split(' ')[0] == day:
            if raw[0] == 'SCREEN_ACTIVE_TYPE_2':
                _feature_dict['duration'] += int(raw[2])
                _feature_dict['count'] += 1
                _time = bs.get_whole_time_from_str(raw[1])
                if _time.hour in [0, 1, 2]:
                    _feature_dict['0-3'] += int(raw[2])
                elif _time.hour in [3, 4, 5]:
                    _feature_dict['3-6'] += int(raw[2])
                elif _time.hour in [6, 7, 8]:
                    _feature_dict['6-9'] += int(raw[2])
                elif _time.hour in [9, 10, 11]:
                    _feature_dict['9-12'] += int(raw[2])
                elif _time.hour in [12, 13, 14]:
                    _feature_dict['12-15'] += int(raw[2])
                elif _time.hour in [15, 16, 17]:
                    _feature_dict['15-18'] += int(raw[2])
                elif _time.hour in [18, 19, 20]:
                    _feature_dict['18-21'] += int(raw[2])
                elif _time.hour in [21, 22, 23]:
                    _feature_dict['21-24'] += int(raw[2])
    res.loc[len(res)] = list(_feature_dict.values())
    res.to_csv(bs.get_save_whole_name('screen.csv'))