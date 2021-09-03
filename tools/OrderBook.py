import requests
import json
from time import sleep
from tools.ColorLoger import log

def get_order_book(pair, sleeping = 10, attempts = 7):
    api_url = f'https://api.kraken.com/0/public/Depth?pair={pair}'
    for attempt in range(attempts):
        try:
            response = requests.get(url = api_url)
            data = json.loads(response.text)
            if data['error']:
                raise Exception(response.text)
            return data['result'][f'X{pair[:3]}Z{pair[3:]}']['asks']
        except Exception as err:
            sleeping = sleeping if attempt == 0 else sleeping * 2
            log.debug(f'get_order_book err\t{sleeping=},\t{attempt=},\t{err=}')
            sleep(sleeping)
    raise Exception(f'get_olh_data err\tdid not work in {attempts} attempts')



def get_price_from_order_book(ttl_usd_cost, pair):
    orderbook_data = get_order_book(pair, sleeping = 10, attempts = 7)
    by_for = ttl_usd_cost
    usd_cost, coin_volume = 0, 0
    for page in orderbook_data:
        usd_cost_in_step = ttl_usd_cost if ttl_usd_cost - float(page[1])*float(page[0]) <= 0 else float(page[1])*float(page[0])
        usd_cost += usd_cost_in_step

        coin_volume_in_step = usd_cost_in_step/float(page[0])
        coin_volume += coin_volume_in_step

        ttl_usd_cost -= usd_cost_in_step
        if ttl_usd_cost <= 0:
            # print(f'tail_{ttl_usd_cost=}, {coin_volume=}, {usd_cost=}')
            break

    price_in_order_book = round(usd_cost/coin_volume, 1)
    log.info(f'Current price in order book $ {price_in_order_book} per coin if buy for $ {by_for}')
    return price_in_order_book


if __name__ == '__main__':
    price_in_order_book = get_price_from_order_book(10, 'XBTUSD')
    print(price_in_order_book)