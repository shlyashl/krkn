with    (
            select  toUnixTimestamp(max(minute))
            from    raw.trd_krk_xbtusdOlh
            where   date = today()
        ) as row_ts,
        toUnixTimestamp(toStartOfMinute(now()) - 60 * 11) as ten_min_ego
select  if
        (
            row_ts > ten_min_ego,
            row_ts,
            ten_min_ego
        ) as sinse


