import peewee
from playhouse.db_url import connect
import calendar
import datetime

db = connect("mysql://root:toor333666@localhost:3306/wqx")
db.set_autocommit(True)


class BaseModel(peewee.Model):
    class Meta:
        database = db


class FanInfo(BaseModel):
    fan_id = peewee.CharField(index=True)
    member = peewee.CharField()
    loyalty = peewee.FloatField()
    first_date = peewee.DateField(index=True)
    last_date = peewee.DateField(index=True)
    team = peewee.CharField()
    theater = peewee.CharField()


class AllFanInfo(BaseModel):
    fan_id = peewee.CharField(index=True)
    member = peewee.CharField()
    loyalty = peewee.FloatField()
    first_date = peewee.DateField(index=True)
    last_date = peewee.DateField(index=True)
    team = peewee.CharField()
    theater = peewee.CharField()


member_order = ['陈观慧', '陈思', '成珏', '戴萌', '蒋芸', '孔肖吟', '李宇琪',
                '吕一', '莫寒', '潘燕琦', '钱蓓婷', '邱欣怡', '沈之琳', '孙芮',
                '温晶婕', '吴哲晗', '徐晨辰', '徐子轩', '许佳琪', '袁丹妮',
                '袁雨桢', '张语格', '赵韩倩', '赵烨', '陈佳莹', '陈问言',
                '冯薪朵', '龚诗淇', '何晓玉', '黄婷婷', '黄彤扬', '江真仪',
                '金莹玥', '鞠婧祎', '李艺彤', '林思意', '刘菊子', '刘瀛',
                '陆婷', '万丽娜', '许逸', '易嘉爱', '曾艳芬', '张雅梦',
                '张雨鑫', '赵粤', '周怡', '郭倩芸', '郝婉晴', '李清扬', '林楠',
                '刘炅然', '刘佩鑫', '沈梦瑶', '孙珍妮', '王柏硕', '王露皎',
                '文文', '吴燕文', '谢妮', '徐晗', '徐伊人', '许杨玉琢',
                '杨惠婷', '袁航', '袁一琦', '张昕', '陈琳', '冯晓菲', '李晶',
                '李钊', '林忆宁', '祁静', '邵雪聪', '宋昕冉', '孙歆文',
                '汪佳翎', '汪束', '王晓佳', '谢天依', '杨冰怡', '杨韫玉',
                '姚祎纯', '张丹三', '张嘉予', '陈韫凌', '费沁源', '洪珮雲',
                '姜杉', '蒋舒婷', '李佳恩', '刘增艳', '吕梦莹', '潘瑛琪',
                '宋雨珊', '陶波尔', '徐诗琪', '严佼君', '於佳怡', '曾晓雯',
                '张文静', '张怡', 'GNZ48陈佳莹', '陈俊宏', '陈珂', '陈乐添',
                '陈雨琪', '程一心', '杜雨微', '方晓瑜', '高源婧', '黄黎蓉',
                '李沁洁', '梁可', '林嘉佩', '刘梦雅', '刘小末', '刘筱筱',
                '罗寒月', '谢蕾蕾', '阳青颖', '曾艾佳', '张凯祺', '张琼予',
                '朱怡欣', '陈慧婧', '陈楠茜', '陈欣妤', '冯嘉希', '高雪逸',
                '洪静雯', '李伊虹', '刘力菲', '刘倩倩', '卢静', '孙馨',
                '唐莉佳', '唐诗怡', '冼燊楠', '肖文铃', '谢艾琳', '熊心瑶',
                '郑丹妮', '郑悦', '左嘉欣', '左婧媛', '陈桂君', '陈梓荧',
                '代玲', '杜秋霖', '赖俊亦', '刘嘉怡', '龙亦瑞', '农燕萍',
                '王偲越', '王翠菲', '王炯义', '王盈', '王秭歆', '杨可璐',
                '杨媛媛', '于珊珊', '张秋怡', '张心雨', '赵欣雨', '赵翊民',
                '陈美君', '段艺璇', '胡丽芝', '胡晓慧', '李沐遥', '林溪荷',
                '刘崇恬', '刘姝贤', '毛其羽', '牛聪聪', '青钰雯', '宋思娴',
                '孙姗', '孙晓艳', '田姝丽', '熊素君', '闫明筠', '张梦慧',
                '郑依灵', '陈姣荷', '陈倩楠', '冯思佳', '黄子璇', '李娜',
                '李诗彦', '李想', '李媛媛', '李梓', '刘胜男', '罗雪丽',
                '马玉灵', '苏杉杉', '顼凘炀', '徐静', '杨一帆', '张笑盈',
                '赵笛儿', '郑一凡', '陈雅钰', '房蕾', '葛司琪', '黄恩茹',
                '金锣赛', '兰昊', '李泓瑶', '刘闲', '刘一菲', '乔钰珂',
                '任心怡', '石羽莎', '孙语姗', '王雨煊', '许婉玉', '杨晔',
                '叶苗苗', '张韩紫陌', '张怀瑾', '郑心雨', '陈婧文', '陈奕君',
                '冯译莹', '付紫琪', '关思雨', '韩家乐', '菅瑞静', '赖梓惜',
                '李慧', '刘娇', '刘娜', '卢天惠', '南翎璞', '秦玺', '孙敏',
                '王诗蒙', '徐静妍', '杨允涵', '叶锦童', '臧聪', '赵佳蕊',
                '郑诗琪', '朱燕', '董思佳', '方诗涵', '高崇', '高志娴',
                '龚梦婷', '寇承希', '李晴', '李熙凝', '刘静晗', '逯芳竹',
                '曲悦萌', '任雨情', '王菲妍', '王金铭', '王睿琦', '徐斐然',
                '杨肖', '张爱静', '张儒轶', '张羽涵', '张云梦', '郑洁丽']
teams = ['SII', 'NII', 'HII', 'X', 'XII', 'G', 'NIII', 'Z', 'B', 'E', 'J',
         'SIII', 'HIII']
team_order = ['Team {}'.format(t) for t in teams]
theater_order = ['SNH48', 'GNZ48', 'BEJ48', 'SHY48']

TEAM_TO_THEATER = {
    'Team SII': 'SNH48',
    'Team NII': 'SNH48',
    'Team HII': 'SNH48',
    'Team X': 'SNH48',
    'Team XII': 'SNH48',
    'Team G': 'GNZ48',
    'Team NIII': 'GNZ48',
    'Team Z': 'GNZ48',
    'Team B': 'BEJ48',
    'Team E': 'BEJ48',
    'Team J': 'BEJ48',
    'Team SIII': 'SHY48',
    'Team HIII': 'SHY48',
}

pop_mems = ['鞠婧祎', '李艺彤', '黄婷婷', '冯薪朵', '陆婷', '曾艳芬', '赵粤',
            '莫寒', '张语格', '林思意', '费沁源', 'Team SII', 'Team NII',
            'Team HII', 'Team X', 'Team XII', 'GNZ48', 'BEJ48', 'SHY48']

START_DATE = (2012, 9)
END_DATE = (2017, 9)


def get_mem_key(faninfo):
    if faninfo.member.strip() in pop_mems:
        return faninfo.member.strip()
    if faninfo.team.strip() in pop_mems:
        return faninfo.team.strip()
    return faninfo.theater.strip()


def month_iter():
    year, month = START_DATE
    tmpl = '{}{:02d}'
    while tmpl.format(year, month) <= tmpl.format(*END_DATE):
        end_day = calendar.monthrange(year, month)[1]
        month_start = datetime.date(year=year, month=month, day=1)
        month_end = datetime.date(year=year, month=month, day=end_day)
        yield month_start, month_end

        month += 1
        if month == 13:
            month = 1
            year += 1
