from tools.OLHDataSinc import *
from tools.ColorLoger import *
from time import sleep




def run_olh_sinc():
    while True:
        last_minute_in_ch = upload_last_ten_min_olh()
        sleep_sec = 65 - (get_kraken_server_time() - last_minute_in_ch)
        log.debug(f'sleeping for {sleep_sec} sec')
        sleep(sleep_sec)




if __name__ == '__main__':
    run_olh_sinc()