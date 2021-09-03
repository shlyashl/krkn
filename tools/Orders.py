#!/usr/bin/env python
# coding: utf-8
import time
import urllib.parse
import hashlib
import hmac
import base64
import requests
from tools.ColorLoger import log



def current_milli_time():
    return str(int(1000 * time.time()))




def get_kraken_signature(urlpath, data, secret):
    postdata = urllib.parse.urlencode(data)
    encoded = (str(data['nonce']) + postdata).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()

    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    sigdigest = base64.b64encode(mac.digest())
    return sigdigest.decode()




def kraken_request(uri_path, data, api_key, api_sec):
    headers = {}
    api_url = 'https://api.kraken.com'
    headers['API-Key'] = api_key
    # get_kraken_signature() as defined in the 'Authentication' section
    headers['API-Sign'] = get_kraken_signature(uri_path, data, api_sec)
    req = requests.post((api_url + uri_path), headers = headers, data = data)
    return req




def buy_order_best_price(api_key, api_sec, wish_coin_price, usd_vol = 10):
    uri_path = '/0/private/AddOrder'
    coin_vol = round((usd_vol / wish_coin_price), 5)
    data = {
        "nonce": current_milli_time(),
        "ordertype": "market",
        "pair": "XBTUSD",
        "type": "buy",
        "volume": coin_vol,
    }
    try:
        resp = kraken_request(uri_path, data, api_key, api_sec).json()
        log.info(f"!!! bought !!! wish_coin_price:{wish_coin_price}\t{resp['result']['descr']['order']}\ttxid: {resp['result']['txid']}\terrors: {resp['error']}")
    except KeyError as e:
        log.debug(resp)
        raise e
    return resp['result']['txid'][0]




def get_order_info(api_key, api_sec, txid):
    uri_path = '/0/private/QueryOrders'
    data = {
        "nonce": current_milli_time(), "txid": txid, "trades": False}

    try:
        resp = kraken_request(uri_path, data, api_key, api_sec).json()
        log.debug(f"Cheking info for order {txid}")
    except KeyError as e:
        log.debug(resp)
        raise KeyError(e)

    order_info = {
        'txid':    txid,
        'pair':    resp['result'][txid]['descr']['pair'],
        'type':    resp['result'][txid]['descr']['type'],
        # status in (open, closed, canceled)
        'status':  resp['result'][txid]['status'],
        'price':   float(resp['result'][txid]['price']),
        'cost':    float(resp['result'][txid]['cost']),
        'vol':     float(resp['result'][txid]['vol']),
    }
    log.debug(f'Order ({txid}) info is {order_info=}')
    return order_info




def buy_order(api_key, api_sec, coin_price, usd_vol = 10):
    uri_path = '/0/private/AddOrder'
    coin_vol = round((usd_vol / coin_price), 5)
    print(coin_vol)
    data = {
        "nonce": current_milli_time(), "ordertype": "limit", "pair": "XBTUSD", "price": coin_price, "type": "buy", "volume": coin_vol}
    try:
        resp = kraken_request(uri_path, data, api_key, api_sec).json()
        print(f"sell order created: {resp['result']['descr']['order']}\ttxid: {resp['result']['txid']}\terrors: {resp['error']}")
    except KeyError as e:
        print(resp)
        raise KeyError(e)
    return resp['result']['txid'][0]




def sell_order(api_key, api_sec, coin_price, coins_vol):
    uri_path = '/0/private/AddOrder'
    data = {
        "nonce": current_milli_time(), "ordertype": "limit", "pair": "XBTUSD", "price": coin_price, "type": "sell", "volume": coins_vol}
    try:
        resp = kraken_request(uri_path, data, api_key, api_sec).json()
        log.info(f"order: {resp['result']['descr']['order']}\ttxid: {resp['result']['txid']}\terrors: {resp['error']}")
    except KeyError as e:
        log.info(resp)
        raise KeyError(e)
    return resp['result']['txid'][0]




def cancel_order(api_key, api_sec, txid):
    uri_path = '/0/private/CancelOrder'
    data = {
        "nonce": current_milli_time(),
        "txid": txid
    }
    try:
        resp = kraken_request(uri_path, data, api_key, api_sec).json()
        print(f"cancel txid: {txid}\terrors: {resp['error']}")
    except KeyError as e:
        print(resp)
        raise (e)
    return txid

