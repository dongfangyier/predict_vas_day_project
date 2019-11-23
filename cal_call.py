import pandas as pd
import os
import base as bs

features = ['out_duration', 'out_people_number', 'answer_duration', 'answer_people_number', 'reject_duration',
            'reject_people_number', 'all_duration', 'all_people_number']

def calculate_features(whole_path, date):
    """
    calculate features about call information
    :param whole_path:
    :param date:
    :return:
    """
    day = date
    res = pd.DataFrame(columns=features)
    _feature_dict = {}  # 存放我们想要特征的字典
    out_num = {}
    answer_num = {}
    reject_num = {}
    all_num = {}
    for feature in features:
        _feature_dict[feature] = 0  # 开始先全部赋值为0

    df = pd.read_csv(whole_path, header=None)
    for index in df.index:  # 遍历该用户的csv
        #  得到csv的一行
        raw = df.loc[index].values.tolist()
        if str(raw[1]).split(' ')[0] == day:
            if raw[0] == 'OUTGOTING_CALL_TYPE':
                _feature_dict['out_duration'] += int(str(raw[2]).split(';')[2])
                _feature_dict['all_duration'] += int(str(raw[2]).split(';')[2])
                out_num[str(raw[2]).split(';')[1]] = 0
                all_num[str(raw[2]).split(';')[1]] = 0
            if raw[0] == 'INCOMING_CALL_TYPE':
                if str(raw[2]).find('answer') >= 0:
                    _feature_dict['answer_duration'] += int(str(raw[2]).split(';')[2])
                    _feature_dict['all_duration'] += int(str(raw[2]).split(';')[2])
                    answer_num[str(raw[2]).split(';')[1]] = 0
                    all_num[str(raw[2]).split(';')[1]] = 0
                elif str(raw[2]).find('reject') >= 0:
                    _feature_dict['reject_duration'] += int(str(raw[2]).split(';')[2])
                    _feature_dict['all_duration'] += int(str(raw[2]).split(';')[2])
                    reject_num[str(raw[2]).split(';')[1]] = 0
                    all_num[str(raw[2]).split(';')[1]] = 0

    _feature_dict['out_people_number'] = len(out_num.keys())
    _feature_dict['answer_people_number'] = len(answer_num.keys())
    _feature_dict['reject_people_number'] = len(reject_num.keys())
    _feature_dict['all_people_number'] = len(all_num.keys())

    res.loc[len(res)] = list(_feature_dict.values())

    res.to_csv(bs.get_save_whole_name('call.csv'))