import configparser
import multiprocessing
from time import sleep
from tools.MovingAveragePrice import get_moving_price_val
from tools.Orders import cancel_order, sell_order, get_order_info, buy_order_best_price
from tools.OrderBook import get_price_from_order_book
from RunOlhDataSinc import run_olh_sinc
from tools.ColorLoger import log


def get_target_buy_price(moving_price_val, ex_commission, extra_commission):
    target_buy_price = moving_price_val * (1 - ex_commission - extra_commission)
    log.info(f'Target buy price $ {target_buy_price}')
    return target_buy_price



def get_target_sell_price(real_buy_price, ex_commission, extra_commission):
    target_sell_price = real_buy_price * (1 + 2 * ex_commission + extra_commission)
    log.info(f'Target sel price $ {target_sell_price}')
    return target_sell_price




if __name__ == '__main__':
    Cfg = configparser.ConfigParser()
    Cfg.read('cfg.ini')
    usd_cost = float(Cfg.get('AlgParams', 'usd_cost'))
    ex_commission = float(Cfg.get('AlgParams', 'ex_commission'))
    extra_commission = float(Cfg.get('AlgParams', 'extra_commission'))
    pair = Cfg.get('AlgParams', 'pair')
    api_key = Cfg.get('KrakenAPI', 'api_key')
    api_sec = Cfg.get('KrakenAPI', 'api_sec')

    olh_sinc_process = multiprocessing.Process(target=run_olh_sinc)
    olh_sinc_process.start()
    log.debug(f'wait while olh data is synchronized')
    sleep(30)

    sell_order_txid = 'OAO45A-5N55J-EESK6V'

    while True:
        moving_price_val = get_moving_price_val()
        currnet_price = get_price_from_order_book(usd_cost, pair)
        target_buy_price = get_target_buy_price(moving_price_val, ex_commission, extra_commission)

        if sell_order_txid:
            while True:
                sell_order_info = get_order_info(api_key, api_sec, sell_order_txid)
                sell_order_staus = sell_order_info['status']
                if sell_order_staus == 'closed':
                    log.info(f'!!! sold !!! sell_order status is closed')
                    break
                log.info(f'sell_order: waiting for close status')
                sleep(5)

        if currnet_price <= target_buy_price and not sell_order_txid:
            buy_order_txid = buy_order_best_price(api_key, api_sec, currnet_price, usd_cost)

            while True:
                buy_order_info = get_order_info(api_key, api_sec, buy_order_txid)
                buy_order_staus = buy_order_info['status']
                if buy_order_staus == 'closed':
                    log.info(f'buy_order status is closed')
                    sell_order_txid = None
                    break
                log.info(f'buy_order: waiting for close status')
                sleep(5)


            target_sell_price = round(get_target_sell_price(buy_order_info['price'], ex_commission, extra_commission), 1)
            sell_order_txid = sell_order(api_key, api_sec, target_sell_price, buy_order_info['vol'])
            while True:
                sell_order_info = get_order_info(api_key, api_sec, sell_order_txid)
                sell_order_staus = sell_order_info['status']
                if sell_order_staus == 'closed':
                    log.info(f'!!! sold !!! sell_order status is closed')
                    sell_order_txid = None
                    break
                log.info(f'sell_order: waiting for close status')
                sleep(5)

        else:
            log.debug(f'nothing to buy (wating 10 sec) {currnet_price=}\t{target_buy_price=}')
            sleep(10)

        # break


    olh_sinc_process.terminate()


