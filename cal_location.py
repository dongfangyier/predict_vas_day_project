import pandas as pd
import base as bs
import amap

MAX_PLACE_DISTANCE = 500  # we think this is one place


def IsEmpty(data):
    '''
    check a data is null or not
    :param data:
    :return:
    '''
    if str(data) == 'None' or str(data) == 'nan' or str(data) == 'NaN' or str(data) == '':
        return True
    return False


def get_home_work_place(file_path, user):
    '''
    read xlsx file and get home address and work address
    :param file_path: all-CRFData-10-22.xlsx
    :return: a list
    '''
    xl = pd.ExcelFile(file_path)
    df = xl.parse('研究对象')

    df = df[['受试者编号', '家庭地址', '工作地址']]
    _list = df.loc[df['受试者编号'] == user].values[0][1:]
    if IsEmpty(_list[1]):
        _list[1] = _list[0]
    if IsEmpty(_list[0]):
        _list[0] = _list[1]
    _list[0] = amap.addr_to_cod(_list[0])
    _list[1] = amap.addr_to_cod(_list[1])

    return _list


def handle_direction(east, west, south, north, new_info):
    '''
    modify direction information
    :param east:
    :param west:
    :param south:
    :param north:
    :param new_info:new direction
    :return:
    '''
    info = str(new_info).split(',')
    info[0] = float(info[0])
    info[1] = float(info[1])
    if float(str(east).split(',')[0]) < info[0]:
        east = new_info
    if float(str(west).split(',')[0]) > info[0]:
        west = new_info
    if float(str(north).split(',')[1]) < info[1]:
        north = new_info
    if float(str(south).split(',')[1]) > info[1]:
        south = new_info

    return east, west, south, north


needed_calculate_features = ['move_distance', 'longest_distance_from_home',
                             'longest_distance_from_home_remove_work', 'max_move_radius',
                             'numof_key_locations', 'numof_locations', 'exceed_work_radius_places',
                             'home_time', 'move_time', 'rest_time', 'missing_data_duration']


def has_place(point, places):
    '''
    a function that we try to fix the times bug of amap
    just check if the point in places
    :return:
    '''
    for x in places:
        if amap.calaulate_distance(x, point) < MAX_PLACE_DISTANCE:
            return True
    return False


def get_the_freq_place(places):
    '''
    we will get the highest frequency longitude anf latitude
    :return:
    '''
    my_dict = {}
    for place in places:
        if my_dict.__contains__(place):
            my_dict[place] += 1
        else:
            my_dict[place] = 0

    return max(my_dict, key=my_dict.get)


def get_places_keys_end(place, places, place_count_list, current_day, current_user, temp_home, work_distance,
                        exceed_work_places, key_places, place_count):
    '''
    there are too many values,just use it
    :param place:
    :param places:
    :param place_count_list:
    :param current_day:
    :param current_user:
    :param temp_home:
    :param work_distance:
    :param exceed_work_places:
    :param key_places:
    :param place_count:
    :return:
    '''
    if place_count >= 4:
        # not add to places
        if not has_place(place, places):
            p = get_the_freq_place(place_count_list)

            places.append(p)
            this_distance = amap.calaulate_distance(temp_home, place)
            if this_distance > work_distance:
                if not has_place(place, exceed_work_places):
                    exceed_work_places.append(p)
    if place_count >= 12:
        if not has_place(place, key_places):
            p = get_the_freq_place(place_count_list)
            key_places.append(p)

    return place, places, place_count_list, current_day, current_user, temp_home, work_distance, exceed_work_places, key_places, place_count


def calculate_time_features(_dict, df, date):
    '''
    calculate time features
    :param _dict:
    :param df:
    :return:
    '''
    # result dictionary
    rea_list = []

    # the features we want to calculate
    home_time = 0
    missing_data_duration = 0

    # temp attribute
    current_day = bs.get_date_from_str(date)
    all_count = 0
    home_count = 0
    current_state = None
    move_count = 0
    rest_count = 0

    for index in df.index:
        raw = df.loc[index].values
        _day = bs.get_date_from_whole_str(raw[1])
        _states = str(raw[-1]).replace(';', ',')
        if raw[0] != 'LOCATION_TYPE' or _states == '-1,-1':
            continue
        if current_state is None and current_day == _day:
            all_count = 1
            move_count = 0
            rest_count = 0
            current_state = _states
            if amap.calaulate_distance(_dict[0], _states) <= MAX_PLACE_DISTANCE:  # at home
                home_count = 1
        elif current_day == _day:
            all_count += 1
            if _states != current_state:
                move_count += 1
            else:
                rest_count += 1
            current_state = _states
            if amap.calaulate_distance(_dict[0], _states) <= MAX_PLACE_DISTANCE:  # at home
                home_count += 1
        elif (_day - current_day).days > 0 or index == df.index[-1]:
            # save information here
            rea_list = [home_count * 5, move_count * 5, rest_count * 5, 24 * 60 - all_count * 5]
            break

    return rea_list


def calculate_move_features(_dict, df, date):
    '''
    calcluate features about move
    :param _dict:
    :param df:
    :return:
    '''
    # the result we want to save
    res_list = []

    # the features we want to calculate
    move_distance = 0
    longest_distance_from_home = 0
    longest_distance_from_home_remove_work = 0
    max_move_radius = 0

    # temp attribute
    current_user = None
    current_day = bs.get_date_from_str(date)
    east = None
    west = None
    north = None
    south = None
    current_long_lat = ''
    temp_move_distance = 0
    temp_longest_distance_from_home = 0
    temp_longest_distance_from_home_remove_work = 0

    for index in df.index:
        raw = df.loc[index].values
        _day = bs.get_date_from_whole_str(raw[1])
        _states = str(raw[-1]).replace(';', ',')
        if raw[0] != 'LOCATION_TYPE' or _states == '-1,-1':
            continue
        if current_user is None and current_day == _day:
            current_user = 1
            east = _states
            west = _states
            north = _states
            south = _states
            current_long_lat = _states
            d = amap.calaulate_distance(_states, _dict[0])
            temp_longest_distance_from_home = d
            if amap.calaulate_distance(_dict[1], _states) > MAX_PLACE_DISTANCE:
                temp_longest_distance_from_home_remove_work = d
        elif current_day == _day:
            east, west, south, north = handle_direction(east, west, south, north, _states)
            temp_move_distance += amap.calaulate_distance(_states, current_long_lat)
            current_long_lat = _states
            d = amap.calaulate_distance(_states, _dict[0])
            if d > temp_longest_distance_from_home:
                temp_longest_distance_from_home = d
            if amap.calaulate_distance(_dict[1],
                                       _states) > MAX_PLACE_DISTANCE and d > temp_longest_distance_from_home_remove_work:
                temp_longest_distance_from_home_remove_work = d
        elif (_day - current_day).days > 0 or index == df.index[-1]:
            # save information
            temp1 = amap.calaulate_distance(east, west)
            temp2 = amap.calaulate_distance(north, south)
            temp3 = amap.calaulate_distance(east, north)
            temp4 = amap.calaulate_distance(east, south)
            temp5 = amap.calaulate_distance(west, north)
            temp6 = amap.calaulate_distance(west, south)
            res_list = [temp_move_distance, temp_longest_distance_from_home,
                        temp_longest_distance_from_home_remove_work,
                        max(temp1, temp2, temp3, temp4, temp5,
                            temp6)]
    return res_list


def calculate_location_features(_dict, df, date):
    '''
    calculate move features here
    :param _dict:
    :param df:
    :return:
    '''
    # result dictionary
    res_list = []

    # the features we want to calculate
    numof_key_locations = 0
    numof_locations = 0
    exceed_work_radius_places = 0

    # temp attribute
    work_distance = 0
    current_user = None
    current_day = bs.get_date_from_str(date)
    place = ''
    place_count = 0
    place_count_list = []  # record the longitude and latitude information at the same place
    exceed_work_places = []
    places = []
    key_places = []

    for index in df.index:
        raw = df.loc[index].values
        _day = bs.get_date_from_whole_str(raw[1])
        _states = str(raw[-1]).replace(';', ',')
        if raw[0] != 'LOCATION_TYPE' or _states == '-1,-1':
            continue

        if current_user is None and current_day == _day:
            current_user = 1
            temp_home = _dict[0]
            temp_work = _dict[1]
            work_distance = amap.calaulate_distance(temp_home, temp_work)
            place = _states
            place_count += 1
            place_count_list.append(_states)
        elif current_day == _day:
            # if the place is same as the last one
            if amap.calaulate_distance(_states, place) < MAX_PLACE_DISTANCE:
                place_count += 1
                place_count_list.append(_states)

            else:  # if not the same
                # save old informations
                place, places, place_count_list, current_day, current_user, temp_home, work_distance, exceed_work_places, key_places, place_count = get_places_keys_end(
                    place, places, place_count_list,
                    current_day, current_user,
                    temp_home,
                    work_distance,
                    exceed_work_places, key_places, place_count)

                # calculate current features
                place = _states
                place_count = 1
                place_count_list = [_states]
        elif (_day - current_day).days > 0 or index == df.index[-1]:
            # save old informations
            place, places, place_count_list, current_day, current_user, temp_home, work_distance, exceed_work_places, key_places, place_count = get_places_keys_end(
                place, places,
                place_count_list,
                current_day, current_user,
                temp_home,
                work_distance,
                exceed_work_places, key_places, place_count)

            # save information that we have
            res_list = [
                len(key_places),
                len(places), len(exceed_work_places)]

    return res_list


def modify_list_Todataframe(location_dict, move_dict, time_dict):
    '''
    modify lists to a dataframe
    :param location_dict:
    :param move_dict:
    :param time_dict:
    :return:
    '''
    df = pd.DataFrame(columns=needed_calculate_features)
    df.loc[0] = move_dict + location_dict + time_dict
    return df


def calculaue_features(whole_path, info_path, date, users):
    '''
    main function
    :return:
    '''
    home_work_place = get_home_work_place(info_path, users)
    df = pd.read_csv(whole_path, header=None)
    location_dict = calculate_location_features(home_work_place, df.copy(), date)
    move_dict = calculate_move_features(home_work_place, df.copy(), date)
    time_dict = calculate_time_features(home_work_place, df.copy(), date)
    df = modify_list_Todataframe(location_dict, move_dict, time_dict)
    df.to_csv(bs.get_save_whole_name('location.csv'))
