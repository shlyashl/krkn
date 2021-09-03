create table raw.trd_krk_xbtusdOlh
(
    minute         DateTime,
    price_n        UInt64,
    volume_n       UInt64,
    date           Date materialized toDate(minute),
    row_created_at DateTime materialized now()
)
    engine = MergeTree PARTITION BY date
        ORDER BY (date, minute)
        SAMPLE BY minute
        SETTINGS index_granularity = 8192;