from utils import (FanInfo, month_iter, TEAM_TO_THEATER, team_order,
                   theater_order)
from copy import deepcopy
import csv


def write_csv(date, mobility, team_fans_num, theater_fans_num):
    print('writing', date)
    global w
    output = [str(date)[:-3]]

    # num of theater
    for th in theater_order:
        output.append(round(theater_fans_num.get(th, 0)))

    # num of team and rate of theater
    for te in team_order:
        tn = team_fans_num.get(te, 0)
        output.append(round(tn))
        th = TEAM_TO_THEATER[te]
        rate = tn / theater_fans_num.get(th, 0) if tn != 0 else 0
        output.append("{0:.2f}%".format(rate * 100))

    # new fan of theater
    for th in theater_order:
        key = (None, th)
        output.append(round(mobility.get(key, 0)))

    # mobility of theater
    for th1 in theater_order:
        for th2 in theater_order:
            if th1 == th2:
                continue
            key = (th1, th2)
            output.append(round(mobility.get(key, 0)))

    # mobility of team
    for te1 in team_order:
        for te2 in team_order:
            if te1 == te2:
                continue
            key = (te1, te2)
            output.append(round(mobility.get(key, 0)))

    w.writerow(output)


def write_csv_fields():
    output = ['Date']
    for th in theater_order:
        output.append("Fan_{}".format(th))
    for te in team_order:
        output.append("Fan_{}".format(te))
        output.append("Fan_{}_P".format(te))
    for th in theater_order:
        output.append("NewFan_{}".format(th))
    for th1 in theater_order:
        for th2 in theater_order:
            if th1 == th2:
                continue
            output.append("{}->{}".format(th1, th2))
    for te1 in team_order:
        for te2 in team_order:
            if te1 == te2:
                continue
            output.append("{}->{}".format(te1, te2))
    global w
    print('writing fields', output)
    w.writerow(output)


def get_mobility_key_by_team(from_team, to_team):
    from_48 = TEAM_TO_THEATER[from_team]
    to_48 = TEAM_TO_THEATER[to_team]
    if from_48 == to_48:
        return None
    return (from_48, to_48)


def main():
    tui_dict = {
        # fan_id: set(team)
    }
    for start_date, end_date in month_iter():
        print('starting', start_date, end_date)

        old_tui_dict = deepcopy(tui_dict)
        mobility = {
            # (from_48, to_48): num
        }
        team_fans_num = {
            # team: num
        }
        theater_fans_num = {
            # theater: num
        }

        # add in fans
        in_fans = FanInfo.select().where((FanInfo.first_date>=start_date) &
                                         (FanInfo.first_date<=end_date))
        for faninfo in in_fans:
            fan_id = faninfo.fan_id.strip()
            tui_dict.setdefault(fan_id, set()).add(faninfo.team)

        # remove out fans
        out_fans = FanInfo.select().where((FanInfo.last_date>=start_date) &
                                          (FanInfo.last_date<=end_date))
        for faninfo in out_fans:
            fan_id = faninfo.fan_id.strip()
            tui_dict.setdefault(fan_id, set()).discard(faninfo.team)

        # calculate
        for fan_id, team_set in tui_dict.items():
            old_teams = old_tui_dict.get(fan_id, set())
            in_teams = team_set - old_teams

            # mobility
            if not team_set:
                # shouldn't calculate mobility
                pass
            elif not old_teams:
                increase = 1 / len(in_teams) if in_teams else 0
                for team in in_teams:
                    # team
                    key = (None, team)
                    mobility[key] = mobility.get(key, 0) + increase
                    # theater
                    key = (None, TEAM_TO_THEATER[team])
                    mobility[key] = mobility.get(key, 0) + increase
            elif not in_teams:
                increase = (1 / len(old_teams)) / len(team_set)
                for team in (old_teams - team_set):
                    for remain_team in team_set:
                        # team
                        key = (team, remain_team)
                        mobility[key] = mobility.get(key, 0) + increase
                        # theater
                        key = get_mobility_key_by_team(team, remain_team)
                        if key is None:
                            continue
                        mobility[key] = mobility.get(key, 0) + increase
            else:
                increase = ((1 / (len(old_teams) + len(in_teams))) /
                            len(old_teams))
                for team in old_teams:
                    for new_team in in_teams:
                        # team
                        key = (team, new_team)
                        mobility[key] = mobility.get(key, 0) + increase
                        # theater
                        key = get_mobility_key_by_team(team, new_team)
                        if key is None:
                            continue
                        mobility[key] = mobility.get(key, 0) + increase

            # fans num
            fan_num = 1 / len(team_set) if team_set else 0
            for team in team_set:
                team_fans_num[team] = team_fans_num.get(team, 0) + fan_num
                th = TEAM_TO_THEATER[team]
                theater_fans_num[th] = theater_fans_num.get(th, 0) + fan_num

        # write
        write_csv(start_date, mobility, team_fans_num, theater_fans_num)

        # delete
        del old_tui_dict
        del mobility
        del team_fans_num
        del theater_fans_num


if __name__ == '__main__':
    global w
    f = open('result.csv', 'w')
    w = csv.writer(f)
    write_csv_fields()
    main()
    f.close()
