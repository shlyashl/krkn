# -*- coding: utf-8 -*-
import pandas as pd
from io import BytesIO
from tools.ClickHouseKrakenUtils import *
from tools.ColorLoger import *


def get_kraken_server_time(sleeping = 10, attempts = 7):

    for attempt in range(attempts):
        try:
            response = requests.get('https://api.kraken.com/0/public/Time')
            response_data = json.loads(response.text)

            kraken_server_date_time = response_data['result']['unixtime']
            log.debug(f'checked server date_time\t{kraken_server_date_time}')
            if response_data['error']:
                raise Exception(response.text)
            return kraken_server_date_time
        except Exception as err:
            sleeping = sleeping if attempt == 0 else sleeping * 2
            log.debug(f'get_kraken_server_time err\t{sleeping=},\t{attempt=}, \t{err=}')
            sleep(sleeping)
    raise Exception(f'get_olh_data err\tdid not work in {attempts} attempts')




def get_data_from_clickhouse(query_name):
    with open(fr'sql/{query_name}.sql', 'rb') as qf:
        q = qf.read()
    q = q + b'\nFORMAT CSVWithNames'
    out = requests.post(url = 'http://localhost:8123/', data = q,
                        auth = ('default', ''))

    if out.status_code == 200 and out.text != '':
        return pd.read_csv(BytesIO(out.content))
    else:
        raise Exception(f'\nStatus: {out.status_code}\n{out.text}')




def get_last_ten_min_olh(sleeping = 10, attempts = 7):
    since = get_data_from_clickhouse('last_todays_ts').iloc[0, 0]
    api_url = f'https://api.kraken.com/0/public/OHLC?pair=XBTUSD&interval=1&since={since}'
    for attempt in range(attempts):
        try:
            response = requests.get(url = api_url)
            olh_data = json.loads(response.text)
            if olh_data['error']:
                raise Exception(response.text)
            log.debug(f'got last ten min olh data: {api_url}')
            return olh_data['result']['XXBTZUSD']
        except Exception as err:
            sleeping = sleeping if attempt == 0 else sleeping * 2
            log.debug(f'get_olh_data err\t{sleeping=},\t{attempt=},\t{api_url=},\t{err=}')
            sleep(sleeping)
    raise Exception(f'get_olh_data err\tdid not work in {attempts} attempts')




def upload_last_ten_min_olh():
    Cfg = configparser.ConfigParser()
    Cfg.read('cfg.ini')
    ch_host = Cfg.get('ClickHouse', 'ch_host')
    login = Cfg.get('ClickHouse', 'login')
    password = Cfg.get('ClickHouse', 'password')
    ts = get_kraken_server_time() - 60
    for elem in get_last_ten_min_olh():
        minute = elem[0]
        if ts > minute:
            row = [minute, int(float(elem[5])*10**9),  int(float(elem[6])*10**9)]
            upload_to_clickhouse(ch_host, login, password, row, False, 'raw.trd_krk_xbtusdOlh', '')
            log.debug(f'min was uploded to clickhouse: {elem[0]}')
    return minute




