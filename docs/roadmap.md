# Roadmap

Each phase ends with a demoable vertical slice.

## Phase 1 — Correct order-book reconstruction

- Coinbase WebSocket feed adapter (snapshot + deltas)
- Sequence-gap detection and re-sync
- L2 order-book engine with invariants
- Unit, property, and replay tests
- Benchmarks (updates/sec, latency histograms)

**Demo:** connect to the live feed and display a correct, self-healing book.

## Phase 2 — Record & replay

- Normalized event schema (versioned)
- Parquet recorder with partitioned layout
- Virtual clock; replay at 1×/N×/step/pause/seek
- DuckDB queries over recordings
- Determinism test: double replay → identical hashes

**Demo:** record 10 minutes, replay to a byte-identical final book state.

## Phase 3 — Matching engine & OMS

- Price-time priority matcher (limit/market/cancel, partial fills)
- Order lifecycle state machine
- Maker/taker fees, tick/lot validation, self-trade prevention
- Pre-trade risk checks + kill switch

**Demo:** place simulated orders into a replaying market; watch fills and rejections.

## Phase 4 — Backtesting

- Strategy interface (same API for live/paper/backtest)
- Reference strategies: market making, book imbalance
- Queue-position and latency models (see [execution-model.md](execution-model.md))
- P&L, inventory, drawdown, fill metrics
- Backtest report with stated assumptions

**Demo:** run the same strategy twice, prove deterministic output; inspect the report.

## Phase 5 — Second venue & polish

- Second venue adapter (e.g. Kraken) with normalized products
- Cross-venue book comparison
- React UI: depth chart, ladder, blotter, replay controls, run comparison
- Feed-health monitoring dashboard (Prometheus/Grafana)
- CI, one-command Docker Compose startup, demo video

**Demo:** compare two venues over the same window in the UI; full replay-driven order flow.

## Possible later extensions

- Rust re-implementation of the order-book core, with comparative benchmarks
- Optional gRPC service split / Redpanda event bus (only when justified)
- FIX adapter
- Additional order types (post-only, IOC, stop)
- Strategy parameter search in Python against the Go engine's API
