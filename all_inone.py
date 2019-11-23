import pandas as pd
import base as bs


files = ['app', 'call', 'screen', 'sleep', 'location']


def create_csv():
    """
    all in one
    :return:
    """
    temp = []
    for file in files:
        df = pd.read_csv(bs.get_save_whole_name(file+'.csv'))
        if 'Unnamed: 0' in df.columns.values:
            del df['Unnamed: 0']
        _dict={}
        for x in df.columns.values:
            _dict[x]=file+'_'+x
        df.rename(columns= _dict,inplace=True)
        temp.append(df)
    temp = pd.concat(temp, axis=1)
    temp.to_csv(bs.get_save_whole_name('all_inone.csv'))
