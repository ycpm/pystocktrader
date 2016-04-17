# Format #
```
date,market_id,open,high,low,close,volume,adj_close
```

  * If you have no "volume" data, set "0".
  * If you have no "adj\_close" (adjusted close price) data, set adj\_close = close.
  * "market\_id" is not important. If no data, set "0"
  * If you have one price data only, set open = high = low = close = adj\_close
  * date format: Year-Month-Day
# Examples #
```
2005-4-8,4,2000000,2300000,1730000,2290000,2613,4580000
2005-4-11,4,2010000,2080000,1890000,1890000,1709,3780000
2005-4-12,4,1590000,1650000,1590000,1590000,491,3180000
2005-4-13,4,1530000,1580000,1300000,1470000,1517,2940000
2005-4-14,4,1410000,1480000,1340000,1440000,671,2880000
```