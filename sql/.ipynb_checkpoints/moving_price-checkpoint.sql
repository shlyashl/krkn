select  min,
        price,
        moving_price,
        moving_price * (1 - 0.0026) as moving_price_com_under,
        moving_price * (1 + 0.0026) as moving_price_com_above,
        moving_price * (1 - 0.0026) * (1 - 0.0005) as mp_u,
        moving_price * (1 + 0.0026) * (1 + 0.0005) as mp_a,
        vol,
        moving_volume
from    (
         select
             groupArray(minute) min_arr,
             groupArray(volume_n) vol_arr,
             groupArray(price_n/1000000000) price_arr,
             groupArrayMovingSum(/*win_size=*/30)((price_n / 1000000000)*volume_n) moving_cost_arr,
             groupArrayMovingSum(/*win_size=*/30)(volume_n) as moving_volume_arr,
             arrayMap((x, y) -> x / y, moving_cost_arr, moving_volume_arr) as moving_price_arr
         from raw.trd_krk_xbtusdOlh
         where date = '2021-08-02'
            )
    array join
        min_arr as min,
        price_arr as price,
        moving_price_arr as moving_price,
        vol_arr as vol,
        moving_volume_arr as moving_volume