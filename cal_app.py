import pandas as pd
import numpy as np
import os
import base as bs
import datetime

small_features = ['duration', '0-3_duration', '3-6_duration', '6-9_duration',
                  '9-12_duration', '12-15_duration', '15-18_duration', '18-21_duration', '21-24_duration',
                  'count', '0-3_count', '3-6_count', '6-9_count', '9-12_count', '12-15_count', '15-18_count',
                  '18-21_count', '21-24_count']

big_features = ['contact', 'content', 'shopping', 'video', 'music', 'take_out', 'all']


def get_class(big):
    if big == 'contact':
        ll = ['QQ', '微信']
    elif big == 'content':
        ll = ['微博', '豆瓣', '知乎', '头条', '小红书']
    elif big == 'shopping':
        ll = ['淘宝', '京东', '拼多多']
    elif big == 'video':
        ll = ['哔哩哔哩', '优酷', '抖音', '爱奇艺', '腾讯视频', '芒果TV']
    elif big == 'music':
        ll = ['网易云', 'qq音乐', '酷狗音乐', '虾米音乐']
    elif big == 'take_out':
        ll = ['美团外卖', '饿了么']
    elif big == 'else':
        ll = ['百度', '浏览器']
    elif big == 'all':
        ll = [';']
    return ll


def calculate_features(whole_path, date):
    """
    calculate features about app
    :return:
    """
    day = date
    features = []
    for x in big_features:
        for y in small_features:
            features.append(x + '_' + y)
    res = pd.DataFrame(columns=features)
    _feature_dict = {}  # 存放我们想要特征的字典
    for feature in features:
        _feature_dict[feature] = 0  # 开始先全部赋值为0
    df = pd.read_csv(whole_path, header=None)
    for index in df.index:  # 遍历该用户的csv
        #  得到csv的一行
        raw = df.loc[index].values.tolist()
        if str(raw[1]).split(' ')[0] == day:
            if raw[0] == 'OPEN_ACT_2':
                for big_feature in big_features:
                    ll = get_class(big_feature)
                    IsClass = False
                    for l in ll:
                        if str(raw[2]).find(l) >= 0:
                            IsClass = True
                    if IsClass:
                        _feature_dict[big_feature + '_' + 'duration'] += int(str(raw[2]).split(';')[-1])
                        _feature_dict[big_feature + '_' + 'count'] += 1
                        _time = bs.get_whole_time_from_str(raw[1])
                        if _time.hour in [0, 1, 2]:
                            _feature_dict[big_feature + '_' + '0-3_duration'] += int(str(raw[2]).split(';')[-1])
                            _feature_dict[big_feature + '_' + '0-3_count'] += 1
                        elif _time.hour in [3, 4, 5]:
                            _feature_dict[big_feature + '_' + '3-6_duration'] += int(str(raw[2]).split(';')[-1])
                            _feature_dict[big_feature + '_' + '3-6_count'] += 1
                        elif _time.hour in [6, 7, 8]:
                            _feature_dict[big_feature + '_' + '6-9_duration'] += int(str(raw[2]).split(';')[-1])
                            _feature_dict[big_feature + '_' + '6-9_count'] += 1
                        elif _time.hour in [9, 10, 11]:
                            _feature_dict[big_feature + '_' + '9-12_duration'] += int(str(raw[2]).split(';')[-1])
                            _feature_dict[big_feature + '_' + '9-12_count'] += 1
                        elif _time.hour in [12, 13, 14]:
                            _feature_dict[big_feature + '_' + '12-15_duration'] += int(str(raw[2]).split(';')[-1])
                            _feature_dict[big_feature + '_' + '12-15_count'] += 1
                        elif _time.hour in [15, 16, 17]:
                            _feature_dict[big_feature + '_' + '15-18_duration'] += int(str(raw[2]).split(';')[-1])
                            _feature_dict[big_feature + '_' + '15-18_count'] += 1
                        elif _time.hour in [18, 19, 20]:
                            _feature_dict[big_feature + '_' + '18-21_duration'] += int(str(raw[2]).split(';')[-1])
                            _feature_dict[big_feature + '_' + '18-21_count'] += 1
                        elif _time.hour in [21, 22, 23]:
                            _feature_dict[big_feature + '_' + '21-24_duration'] += int(str(raw[2]).split(';')[-1])
                            _feature_dict[big_feature + '_' + '21-24_count'] += 1

    res.loc[len(res)] = list(_feature_dict.values())
    res.to_csv(bs.get_save_whole_name('app.csv'))
