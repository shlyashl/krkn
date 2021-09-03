select sum(price * volume) / sum(volume)                                   as moving_price,
       toStartOfMinute(now()) - 60 * 2 <= max(minute)                      as is_data_up_to_date,
       count() = 20                                                        as is_correct_cnt_rows,
       ((max(minute) - min(minute) + 60) / 60) = 20                        as is_all_minutes_in_set,
       and(is_data_up_to_date, is_correct_cnt_rows, is_all_minutes_in_set) as is_valid_data

from (
         select price_n / 1000000000  as price,
                volume_n / 1000000000 as volume,
                minute
         from raw.trd_krk_xbtusdOlh
         where 1 = 1
           and date = today()
         order by minute desc
         limit 20
    ) raw
