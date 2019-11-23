import cal_call
import cal_screen
import cal_sleep
import cal_app
import cal_location
import all_inone
import predict

whole_path = 'data\\H01-0078-MobileUseData.csv'
info_path = 'data\\all-CRFData.xlsx'
date = '2019-10-20'
user = 'H01-0078'

if __name__ == '__main__':
    # print('calculate call ...')
    # cal_call.calculate_features(whole_path,date)
    # print('calculate screen ...')
    # cal_screen.calculate_features(whole_path, date)
    # print('calculate sleep ...')
    # cal_sleep.calculate_features(info_path, date, user)
    # print('calculate app ...')
    # cal_app.calculate_features(whole_path, date)
    # print('calculate location ...')
    # cal_location.calculaue_features(whole_path, info_path, date, user)
    print('all in one ...')
    all_inone.create_csv()
    print('predict vas ...')
    vas = predict.predict()
    print(vas)
