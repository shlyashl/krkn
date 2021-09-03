from tools.ClickHouseKrakenUtils import get_data_from_ch
from tools.ColorLoger import log


def get_moving_price_val():
    df = get_data_from_ch('moving_price_val')
    moving_price_val = float(df['moving_price'][0])
    is_valid_moving_price_val = bool(df['moving_price'][0])
    if not is_valid_moving_price_val:
        raise ValueError('Moving price value is not up-to-date')
    log.info(f'Current moving price $ {moving_price_val} per coin')
    return moving_price_val





if __name__ == '__main__':
    print(get_moving_price_val())