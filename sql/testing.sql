select  date, count()
from    raw.trd_krk_xbtusdOlh
group   by date
order   by date asc;


;
alter table raw.trd_krk_xbtusdOlh drop partition '2021-07-30';

truncate TABLE raw.trd_krk_xbtusdOlh;



select sum((price_n / 1000000000) * volume_n) / sum(volume_n),
       sum(volume_n)

from raw.trd_krk_xbtusdOlh
where date = '2021-08-08';


select  min,
        moving_price,
        moving_cost,
        vol,
        price,
        moving_volume
from    (
            select
                groupArray(minute) min_arr,
                groupArray(volume_n) vol_arr,
                groupArray(price_n/1000000000) price_arr,
                groupArrayMovingSum(/*win_size=*/2)((price_n / 1000000000)*volume_n) moving_cost_arr,
                groupArrayMovingSum(/*win_size=*/2)(volume_n) as moving_volume_arr,
                arrayMap((x, y) -> x / y, moving_cost_arr, moving_volume_arr) as moving_price_arr
            from raw.trd_krk_xbtusdOlh
            where date = '2021-08-01'
            )
array join
        min_arr as min,
        moving_price_arr as moving_price,
        moving_cost_arr as moving_cost,
        vol_arr as vol,
        price_arr as price,
        moving_volume_arr as moving_volume;


select 16955285170 + 9973332190 = 26928617360


    ;
select sum((price_n / 1000000000) * volume_n) / sum(volume_n) from raw.trd_krk_xbtusdOlh
where date  = '2020-08-01'


;



select  min,
        price,
        moving_price,
        vol,
        moving_volume
from    (
         select
             groupArray(minute) min_arr,
             groupArray(volume_n) vol_arr,
             groupArray(price_n/1000000000) price_arr,
             groupArrayMovingSum(/*win_size=*/10)((price_n / 1000000000)*volume_n) moving_cost_arr,
             groupArrayMovingSum(/*win_size=*/10)(volume_n) as moving_volume_arr,
             arrayMap((x, y) -> x / y, moving_cost_arr, moving_volume_arr) as moving_price_arr
         from raw.trd_krk_xbtusdOlh
         where date = '2021-08-01'
            )
    array join
        min_arr as min,
        price_arr as price,
        moving_price_arr as moving_price,
        vol_arr as vol,
        moving_volume_arr as moving_volume

