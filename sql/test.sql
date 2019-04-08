---------------QUERY INTERSECTION OF 2 EXCHANGE
SELECT binance.base_asset
   FROM binance
UNION (
         SELECT binance.quote_asset AS base_asset
           FROM binance
        INTERSECT
         SELECT bitfinex.base_asset
           FROM bitfinex
)
UNION
 SELECT bitfinex.quote_asset AS base_asset
   FROM bitfinex;

---------------QUERY VIEW OF DB
--RETURN ALL THE VIEW (SERVE PER PRENDERE LE INTERSEZIONI)

SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'VIEW'

SELECT distinct binance.base_asset, binance.exchange_name, bitfinex.exchange_name FROM binance JOIN bitfinex ON binance.symbol_std=bitfinex.symbol_std


SELECT distinct s1.symbol as symbol_cex, s2.symbol as symbol_poloniex, s1.base_asset, s1.exchange_name as cex_name, s2.exchange_name as poloniex_name FROM (SELECT *
    FROM cex)s1
inner JOIN (SELECT *
    FROM poloniex)s2
ON s1.symbol_std = s2.symbol_std
