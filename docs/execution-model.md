# Execution Model

What the simulator models **exactly**, what it **approximates**, and what it **does not** claim. Being explicit here is the difference between a credible backtester and a toy.

## Modeled exactly

From recorded L2 data, the following are deterministic:

- **Price-time priority matching** against the reconstructed book
- **Marketable order execution** — an aggressive order consumes book levels in order, with exact prices and quantities from the recording
- **Partial fills** when available quantity is insufficient
- **Maker/taker fees** per venue fee schedule
- **Order validation** — tick size, lot size, min notional
- **Self-trade prevention** (configurable mode)
- **Event ordering** — the replayed stream is the recorded stream

## Approximated (documented assumptions)

### Queue position for resting limit orders

A recording of L2 data does not contain individual order identities, so the simulator cannot know exactly where a new resting order sits in the queue. It models queue position as:

> The order is behind all quantity that was resting at its price level at the time of entry.

The order fills only when cumulative trade volume at that price (plus level depletion) exceeds the quantity ahead of it. This is the standard **conservative** model: it systematically underestimates fill probability rather than overestimating it.

**Known limitation:** if the level grows after entry, new joiners are behind our order in reality but invisible in L2 data — this is ignored (conservative direction is preserved).

### Latency

Configured per venue/run:

- Order-entry latency (strategy decision → order reaches matcher)
- Cancel latency
- Feed latency (exchange timestamp vs. receipt timestamp skew is recorded and can be applied)

During replay, a strategy sees the book as of `t - feed_latency` and its orders take effect at `t + entry_latency`.

### Market impact

The simulator assumes our orders are small enough not to move the market: the recorded book evolution is independent of our simulated orders. Aggressive orders consume recorded liquidity but do not alter subsequent recorded events.

**This assumption must be stated on every backtest report**, with the order size as a fraction of average level depth.

## Explicitly not claimed

- **No guarantee of real-world profitability.** Backtest results are conditional on the approximations above.
- **No real-money execution.** The system is for simulation and paper trading only.
- **Not a full venue replica.** Auctions, halts, order types beyond limit/market, and venue-specific matching nuances are out of scope unless explicitly added.
- **Candles are not a simulation input.** Backtests run on event-level L2 data; candle-based "the price touched my limit so I filled" logic is rejected as unsound.

## Backtest report requirements

Every backtest run must emit a report containing:

1. The recording(s) used (venue, product, time range, content hash)
2. All model parameters (fees, latencies, queue model version)
3. Order sizes relative to average depth (market-impact sanity check)
4. P&L, fill rate, average queue wait, latency breakdown
5. A determinism hash (re-running yields identical results)
