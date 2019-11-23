import datetime
import pandas as pd
import os

save_path = 'handle_data\\'
model_path='_model\\'
features_path= 'features\\features.csv'


def get_save_whole_name(name):
    """
    just add save path to the file name
    :param name:
    :return:
    """
    return os.path.join(save_path, name)


def get_whole_time_from_str(str_time):
    '''
    get the time in the str
    :param str_time:time in the file
    :return:date
    '''
    return datetime.datetime.strptime(str_time, '%Y-%m-%d %H:%M:%S')

def get_date_from_whole_str(str_time):
    '''
    get the time in the str
    :param str_time:time in the file
    :return:date
    '''
    return datetime.datetime.strptime(str_time, '%Y-%m-%d %H:%M:%S').date()


def get_date_from_str(str_time):
    '''
    get the date in the str
    :param str_time:time in the file
    :return:date
    '''
    return datetime.datetime.strptime(str_time, '%Y-%m-%d').date()


def read_xlsx(file_name, sheet_name):
    '''
    read all-CRFData.xlsx with the sheet names
    :param file_name:file name
    :param sheet_name:sheet name
    :return: dataframe
    '''
    xl = pd.ExcelFile(file_name)
    df = xl.parse(sheet_name)

    return df


def date_toString(dt):
    '''
    把date转成字符串
    :param dt:
    :return:
    '''
    return dt.strftime("%Y-%m-%d")
