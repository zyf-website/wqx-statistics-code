from utils import FanInfo, AllFanInfo, db

db.create_tables([FanInfo, AllFanInfo])

# LOAD_DATA_SQL = """
# load data local infile '{filename}'
# into table faninfo
# fields 
#     terminated by ','
# lines
#     terminated by '\n'
# ignore 1 lines
# (`fan_id`, `member`, `loyalty`, `first_date`, `last_date`, `theater`, `team`)
# """

# FILENAMES = ['faninfo.csv',
#              'faninfo2.csv']

# for filename in FILENAMES:
#     db.execute_sql(LOAD_DATA_SQL.format(filename=filename))
