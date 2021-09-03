import datetime
from tools.ClickHouseKrakenUtils import update_olh_ch_part


end_date = datetime.datetime.today() - datetime.timedelta(days=1)
# end_date = datetime.datetime.strptime('2017-01-22', '%Y-%m-%d')
start_date = datetime.datetime.strptime('2017-01-01', '%Y-%m-%d')
numdays = (end_date - start_date).days + 1
date_list = [(end_date - datetime.timedelta(days=x)).strftime('%Y-%m-%d') for x in range(numdays)]

for ed in date_list:
    update_olh_ch_part(ed, 'xbtusd')
