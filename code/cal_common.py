import csv
from utils import FanInfo, member_order, team_order, theater_order


result_dict = {
    # key: set(fan_id)
}


def get_data(key_field):
    global result_dict
    del result_dict
    result_dict = {}

    print('reading...')
    faninfos = FanInfo.select()
    for faninfo in faninfos:
        key = getattr(faninfo, key_field).strip()
        result_dict.setdefault(key, set()).add(faninfo.fan_id)
    print('read over')


def output_cross(key_field):
    filename = '{}_cross_rate.csv'.format(key_field)
    get_data(key_field)
    order_list = globals()['{}_order'.format(key_field)]

    with open(filename, 'w') as f:
        r = csv.writer(f)
        r.writerow([''] + order_list)

        for key in order_list:
            print('{} is calculating...'.format(key))
            line = [key]
            for key2 in order_list:
                set1 = result_dict.get(key, set())
                num = len(set1.intersection(result_dict.get(key2, set())))
                rate = num / len(set1) if num != 0 else 0
                rate = "{0:.2f}%".format(rate * 100)
                line.append(rate)
            r.writerow(line)

        print('{} over'.format(key_field))


if __name__ == '__main__':
    output_cross('member')
    output_cross('team')
    output_cross('theater')
