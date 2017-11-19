from utils import (FanInfo, month_iter, pop_mems, get_mem_key)
from copy import deepcopy
import csv


def write_csv(date, mobility, fans_num):
    print('writing', date)
    global w
    output = [str(date)[:-3]]

    # num of member
    for m in pop_mems:
        output.append(round(fans_num.get(m, 0)))

    # new fan of member
    for m in pop_mems:
        key = (None, m)
        output.append(round(mobility.get(key, 0)))

    # mobility of member
    for m1 in pop_mems:
        for m2 in pop_mems:
            if m1 == m2:
                continue
            key = (m1, m2)
            output.append(round(mobility.get(key, 0)))

    w.writerow(output)


def write_csv_fields():
    output = ['Date']
    for m in pop_mems:
        output.append("Fan_{}".format(m))
    for m in pop_mems:
        output.append("NewFan_{}".format(m))
    for m1 in pop_mems:
        for m2 in pop_mems:
            if m1 == m2:
                continue
            output.append("{}->{}".format(m1, m2))
    global w
    print('writing fields', output)
    w.writerow(output)


def main():
    tui_dict = {
        # fan_id: set(mem)
    }
    for start_date, end_date in month_iter():
        print('starting', start_date, end_date)

        old_tui_dict = deepcopy(tui_dict)
        mobility = {
            # (from_mem, to_mem): num
        }
        fans_num = {
            # mem: num
        }

        # add in fans
        in_fans = FanInfo.select().where((FanInfo.first_date>=start_date) &
                                         (FanInfo.first_date<=end_date))
        for faninfo in in_fans:
            fan_id = faninfo.fan_id.strip()
            tui_dict.setdefault(fan_id, set()).add(get_mem_key(faninfo))

        # remove out fans
        out_fans = FanInfo.select().where((FanInfo.last_date>=start_date) &
                                          (FanInfo.last_date<=end_date))
        for faninfo in out_fans:
            fan_id = faninfo.fan_id.strip()
            tui_dict.setdefault(fan_id, set()).discard(get_mem_key(faninfo))

        # calculate
        for fan_id, mem_set in tui_dict.items():
            old_mems = old_tui_dict.get(fan_id, set())
            in_mems = mem_set - old_mems

            # mobility
            if not mem_set:
                # shouldn't calculate mobility
                pass
            elif not old_mems:
                increase = 1 / len(in_mems) if in_mems else 0
                for mem in in_mems:
                    # mem
                    key = (None, mem)
                    mobility[key] = mobility.get(key, 0) + increase
            elif not in_mems:
                increase = (1 / len(old_mems)) / len(mem_set)
                for mem in (old_mems - mem_set):
                    for remain_mem in mem_set:
                        # mem
                        key = (mem, remain_mem)
                        mobility[key] = mobility.get(key, 0) + increase
            else:
                increase = ((1 / (len(old_mems) + len(in_mems))) /
                            len(old_mems))
                for mem in old_mems:
                    for new_mem in in_mems:
                        # mem
                        key = (mem, new_mem)
                        mobility[key] = mobility.get(key, 0) + increase

            # fans num
            fan_num = 1 / len(mem_set) if mem_set else 0
            for mem in mem_set:
                fans_num[mem] = fans_num.get(mem, 0) + fan_num

        # write
        write_csv(start_date, mobility, fans_num)

        # delete
        del old_tui_dict
        del mobility
        del fans_num


if __name__ == '__main__':
    global w
    f = open('result.csv', 'w')
    w = csv.writer(f)
    write_csv_fields()
    main()
    f.close()
