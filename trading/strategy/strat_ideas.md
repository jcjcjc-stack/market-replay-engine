# L2 Data

## Cross-Venue Strategy

The strategy compares the same product across multiple venues using top-of-book snapshots.

| Venue      | Product | Bid       | Bid quantity | Ask       | Ask quantity |
| ---------- | ------- | --------- | ------------ | --------- | ------------ |
| Exchange A | BTC-USD | 62,000.00 | 1.25 BTC     | 62,001.00 | 0.80 BTC     |
| Exchange B | BTC-USD | 62,050.00 | 0.60 BTC     | 62,051.00 | 1.10 BTC     |

For each venue, bid is the highest available buy price and ask is the lowest available sell price. The quantities are the available amounts at those prices.

This strategy looks for a temporary price difference between two exchanges where the same crypto trading pair can be bought on one exchange for less than it can be sold for on another. It attempts to capture that difference by submitting a market buy and a market sell for equal quantities as close together as possible. The two-standard-deviation threshold identifies an unusually large difference relative to recent observations; profitability still depends on execution prices and costs.

| Strategy rule       | Description                                                                                                 |
| ------------------- | ----------------------------------------------------------------------------------------------------------- |
| Compare             | The same trading pair across different venues                                                               |
| Price difference    | Selling venue’s bid minus buying venue’s ask                                                              |
| Entry condition     | The difference is positive and at least two standard deviations above its historical mean                   |
| Historical window   | Initially 50 observations (tbd)                                                                             |
| Execution           | Market buy at the lower-ask venue and market sell at the higher-bid venue.                                  |
| Quantity            | Use the smaller of the buying venue’s ask quantity and selling venue’s bid quantity for both orders       |
| Costs and execution | Account for fees, latency, slippage, and partial fills; the statistical threshold does not guarantee profit |

#### Execution Type 1: Buy, Then Sell

Buy the product on the venue with the lower ask. Once the purchase fills, sell the **actual filled quantity** on the venue with the higher bid as soon as possible.

The intended quantity is the smaller of the available ask quantity and bid quantity. Profit depends on the selling price remaining favourable during the delay between executions.

Selling immediately requires existing inventory on the second venue. Otherwise, the purchased asset must first be transferred, adding transfer time and costs.

#### Execution Type 2: Long and Short

Open a long position on the lower-priced venue and a short position of equal quantity on the higher-priced venue, as close together as possible. Hold both positions while waiting for the price difference to narrow.

| Risk or exit rule  | Description                                                                                                                              |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------- |
| Profit target      | Close both positions when their combined net profit reaches the initial cross-venue price difference multiplied by the executed quantity |
| Loss limit         | Close both positions when their combined loss reaches a predefined threshold                                                             |
| Profit calculation | Include both positions’ gains and losses, trading fees, and applicable funding or borrowing costs                                       |

The initial price difference is a **profit target, not profit already earned**. Actual profit depends on the prices at which both positions open and close. The loss threshold and mismatch-handling rule remain to be defined.

---

# L3 Data

## Cross-Venue VWAP Strategy

The strategy compares the same trading pair across exchanges using order-book snapshots containing multiple bid and ask levels.

For a proposed quantity **Q**, it calculates the volume-weighted average execution price (VWAP) by consuming enough order-book depth to fill that quantity. The buy VWAP uses asks from lowest to highest; the sell VWAP uses bids from highest to lowest. Only the required quantity from the final price level is included.

#### Core formula

For quantity Q, use a **VWAP across the order book**, consuming enough depth to fill Q:

$$
VWAP_Q = \frac{\sum_k P_k q_k}{\sum_k q_k}, \qquad \sum_k q_k = Q
$$

Here, P_k is the price at level k, and q_k is the quantity consumed at that level.

The executable trading signal becomes:

**Edge(Q) = Sell VWAP(Q) − Buy VWAP(Q) − Cost(Q)**

Here, cost is expressed per unit of the product so it is comparable with the VWAP prices. If the first venue is the buying venue, the formula is the second venue’s sell VWAP minus the first venue’s buy VWAP, minus costs.

| Strategy rule        | Description                                                                                                                    |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| Compare              | The same trading pair across different venues, using available order-book depth                                                |
| Buy price            | VWAP of the asks needed to buy Q on the buying venue                                                                           |
| Sell price           | VWAP of the bids needed to sell Q on the selling venue                                                                         |
| Trading signal       | Edge(Q): the difference between sell and buy VWAP, after costs                                                                 |
| Entry condition      | Edge(Q) is positive and at least two standard deviations above its historical mean for the same venue direction and quantity Q |
| Historical window    | Initially 50 preceding observations; the time covered depends on the sampling interval                                         |
| Quantity             | Evaluate a proposed Q only when both books contain sufficient depth to fill it                                                 |
| Execution            | Use either buy-then-sell or paired long-and-short execution, with the corresponding exit and risk rules                        |
| Execution constraint | Snapshot-based VWAP is an estimate; prices and available depth may change before orders fill                                   |

The method for choosing Q and the costs included remain to be defined.
