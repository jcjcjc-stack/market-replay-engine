L2 Book snapshot requirements
For the first version of my strategy, I need a top-of-book snapshot for each venue and trading pair containing:
- Best bid price: highest available buy price.
- Best bid quantity: total quantity available at that price.
- Best ask price: lowest available sell price.
- Best ask quantity: total quantity available at that price.

{
  "venue": "coinbase",
  "product": "BTC-USD",
  "sequence": 123456789,
  "bid": "62000.00",
  "bid_quantity": "1.25",
  "ask": "62001.00",
  "ask_quantity": "0.80",
  "exchange_ts": "2026-10-06T10:00:00.123Z",
  "received_ts": "2026-10-06T10:00:00.128Z"
}