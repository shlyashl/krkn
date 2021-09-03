# -*- coding: utf-8 -*-
import datetime
import json
from io import BytesIO
import pytz
import requests
import configparser
from time import sleep
import pandas as pd
from tools.ColorLoger import *




def get_data_from_ch(query_name):
    with open(fr'sql/{query_name}.sql', 'rb') as qf:
        q = qf.read()
    q = q + b'\nFORMAT CSVWithNames'
    out = requests.post(url = 'http://localhost:8123/', data = q,
                        auth = ('default', ''))

    if out.status_code == 200 and out.text != '':
        return pd.read_csv(BytesIO(out.content))
    else:
        raise Exception(f'\nStatus: {out.status_code}\n{out.text}')



def drop_part_in_clickhouse(ch_host, login, password, verify, table_name, ed):
    query_dict = {'query': f"alter table {table_name} drop partition '{ed}' "}
    response = requests.post(ch_host, auth=(login, password), verify=verify, params=query_dict)
    if response.status_code != 200:
        raise ValueError('Drop error: ', response.text)




def upload_to_clickhouse(ch_host, login, password, row, verify, table_name, ed):
    data = '\t'.join(map(str, row)).encode()
    query_dict = {'query': f'insert into {table_name} FORMAT TSV '}
    response = requests.post(ch_host, auth=(login, password), data=data, verify=verify, params=query_dict)
    if response.status_code != 200 or response.text != '':
        raise ValueError('Insert error: ', response.text)




def get_olh_data(pair, since, sleeping = 10, attempts = 7):
    olh_url = f'https://api.kraken.com/0/public/Trades?pair={pair}&since={since}'
    log.debug(f'recived\tsince={datetime.datetime.utcfromtimestamp(int(since)).strftime("%Y-%m-%d %H:%M:%S")}\t{olh_url=}')
    for attempt in range(attempts):
        try:
            response = requests.get(url = olh_url)
            olh_data = json.loads(response.text)
            last_trade = int(int(olh_data['result']['last'])/1_000_000_000)
            if olh_data['error']:
                raise Exception(response.text)
            return olh_data, last_trade
        except Exception as err:
            sleeping = sleeping if attempt == 0 else sleeping * 2
            log.debug(f'get_olh_data err\t{sleeping=},\t{attempt=},\t{olh_url=},\t{err=}')
            sleep(sleeping)
    raise Exception(f'get_olh_data err\tdid not work in {attempts} attempts')




def update_olh_ch_part(ed, pair):
    Cfg = configparser.ConfigParser()
    Cfg.read('cfg.ini')
    ch_host = Cfg.get('ClickHouse', 'ch_host')
    login = Cfg.get('ClickHouse', 'login')
    password = Cfg.get('ClickHouse', 'password')
    table_name = f'raw.trd_krk_{pair}Olh'
    drop_part_in_clickhouse(ch_host, login, password, False, table_name, ed)

    pair_json_name = ('X' + pair[:3] + 'Z' + pair[3:]).upper()

    part_start_sec = int(datetime.datetime.timestamp(datetime.datetime.strptime(ed, '%Y-%m-%d').replace(tzinfo=pytz.UTC)))
    part_end_sec = part_start_sec + 60*60*24

    olh_data_ts_sec = part_start_sec
    olh_data_prev_ts_min, volume, cost, since = 0, 0, 0, part_start_sec


    while part_end_sec > olh_data_ts_sec:
        olh_data, olh_data_last_trade_sec = get_olh_data(pair, since)

        for trade in olh_data['result'][pair_json_name]:
            olh_data_ts_sec = int(trade[2])
            olh_data_ts_min = int(olh_data_ts_sec / 60) * 60


            if olh_data_prev_ts_min and olh_data_prev_ts_min != olh_data_ts_min and cost and volume:
                # create and send row
                row = (olh_data_prev_ts_min, int((cost / volume) * 10 ** 9), int(volume * 10 ** 9))
                upload_to_clickhouse(ch_host, login, password, row, False, table_name, ed)
                volume, cost = 0, 0

                log_row = f'\tts={row[0]}\tprice_n={row[2]}\tvolume={row[2]}'
                log.debug(f'inserted\tolh_data_prev_ts_min={datetime.datetime.utcfromtimestamp(olh_data_prev_ts_min).strftime("%Y-%m-%d %H:%M:%S")}{log_row}')


            # check is allowed parse file or continue main while loop
            if olh_data_ts_sec >= olh_data_last_trade_sec or olh_data_ts_sec >= part_end_sec:
                since = olh_data_ts_sec
                break


            cost += float(trade[0]) * float(trade[1])
            volume += float(trade[1])

            olh_data_prev_ts_min = olh_data_ts_min

            # log.debug(f'parsed\tolh_data_ts_ms={datetime.datetime.utcfromtimestamp(olh_data_ts_ms).strftime("%Y-%m-%d %H:%M:%S")}\t{trade=}')

    log.debug(f'Part {ed} updated for {pair}')










