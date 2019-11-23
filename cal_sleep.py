import numpy as np
import pandas as pd
import base as bs

features = ['deep_sleep', 'light_sleep', 'all_sleep', 'deep_sleep_ratio', 'light_sleep_ratio',
            'sleep_time', 'wake_time', 'sport_ratio']

def get_time(s):
    '''
    get minutes from an array
    :param s:
    :return:
    '''
    res = 0  # minute in unites
    if s.find('d') >= 0:
        temp = str(s).split('d')
        res += 24 * 60 * int(temp[0])
        s = temp[1]
    if s.find('h') >= 0:
        temp = str(s).split('h')
        res += 60 * int(temp[0])
        s = temp[1]
    if s.find('min') >= 0:
        temp = str(s).split('min')
        res += int(temp[0])
    return res

def calculate_features(info_path, date, user):
    """
    calculate features about sleep
    :param whole_path:
    :param date:
    :return:
    """
    day = date
    sleep_df = bs.read_xlsx(info_path, '睡眠信息')
    res = pd.DataFrame(columns=features)
    temp = [0, 0, 0, 0, 0, 0, 0, 0]
    for index in sleep_df.index:
        raw = sleep_df.loc[index].values
        if raw[1] == user and raw[7] == day:
            temp[0] = get_time(raw[3])
            temp[2] = get_time(raw[2])
            temp[1] = temp[2] - temp[0]
            temp[3] = temp[0] / temp[2]
            temp[4] = 1 - temp[3]
            temp[7] = (24 * 60 - temp[2]) / (24 * 60)
            temp[5] = int(raw[4][:2])
            temp[6] = int(raw[5][:2])

    res.loc[len(res)] = temp

    res.to_csv(bs.get_save_whole_name('sleep.csv'))


