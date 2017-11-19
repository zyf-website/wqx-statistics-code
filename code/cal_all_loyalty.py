import csv
from utils import member_order
import pymysql


file_no = 0
f = None
w = None
outputs = []
count = 250000

def gen_new_file():
    global file_no, f, w
    if f:
        f.close()
    file_no += 1
    print('generating file {}...'.format(file_no))
    filename = 'all_loyalty{}.csv'.format(file_no)
    f = open(filename, 'w')
    w = csv.writer(f)
    output = ['']
    for mem in member_order:
        output.append(mem)
    w.writerow(output)


def main():
    global loyalty_dict
    print('start')
    with open('fan_ids') as f:
        all_fans = f.read().split(',')
    print('reading fans id over', len(all_fans))
    for fan_ids in zip(*[iter(all_fans)]*100):
        conn = pymysql.connect(host='localhost', port=3306, user='root', password='toor333666', db='wqx', charset='utf8')
        c = conn.cursor()
        c.execute('select fan_id, member, loyalty from allfaninfo where fan_id in {}'.format(tuple(fan_ids)))
        tuis = c.fetchall()

        tui_dicts = {}
        for tui in tuis:
            fan_id = tui[0]
            member = tui[1].strip()
            loyalty = tui[2]
            tui_dicts.setdefault(fan_id, {}).update({member: loyalty})
        write(fan_ids, tui_dicts)

        del tui_dicts
        del tuis


def write(fan_ids, tui_dicts):
    global w, count, outputs
    for fan_id in fan_ids:
        tui_dict = tui_dicts.get(fan_id, {})
        if count >= 250000:
            count = 0
            gen_new_file()
        if count % 1000 == 999:
            print(count)
            w.writerows(outputs)
            outputs = []

        output = [fan_id]
        for mem in member_order:
            loyalty = tui_dict.get(mem, '')
            output.append(loyalty)
        outputs.append(output)

        count += 1


if __name__ == '__main__':
    main()
    if f:
        f.close()