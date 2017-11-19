import pymysql
from functools import reduce


def main():
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='toor333666', db='wqx')
    c = conn.cursor()
    print(1)
    c.execute('select distinct fan_id from allfaninfo')
    print(2)
    result = c.fetchall()
    print(3)
    ids = set()
    for i in result:
        if not i:
            print(i)
        ids.add(i[0])
    print(4)
    print(len(ids))
    with open('fan_ids', 'w') as f:
        f.write(','.join(ids))


if __name__ == '__main__':
    main()