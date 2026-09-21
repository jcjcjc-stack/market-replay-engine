# Correctness

This document defines the correctness guarantees of the system and how they are tested.

## Feed sequence handling

Venue feeds deliver an initial snapshot followed by sequenced incremental updates. The adapter must handle:

| Case | Required behavior |
|---|---|
| Delta arrives before snapshot | Buffer deltas; apply after snapshot if sequence permits |
| Sequence number skipped (gap) | Invalidate book, re-fetch snapshot, re-apply buffered deltas |
| Duplicate delta | Detect via sequence number; discard |
| Out-of-order delta | Treat as gap; re-sync |
| Feed disconnect | Reconnect, re-fetch snapshot, resume |
| Snapshot older than first buffered delta | Discard snapshot, re-fetch |

Each venue has its own sequencing rules (per-product sequences, snapshot sequence alignment). The adapter encapsulates these; downstream components only see clean, gap-free normalized event streams.

## Order-book invariants

After every applied event:

1. Bids are strictly ordered highest → lowest; asks lowest → highest.
2. No price level has zero or negative quantity.
3. The book is uncrossed: `best_bid < best_ask`.
4. Replaying the same event stream from the same snapshot produces a byte-identical book state (verified via content hash).
5. Midpoint is within `[best_bid, best_ask]`.

Invariants are checked by property-based tests over recorded real feeds, not just synthetic data.

## Determinism guarantees

A run is fully determined by:

- The input event stream (Parquet files)
- The strategy configuration
- The seed (virtual clock, RNG)

Repeated runs with identical inputs must produce identical:

- Order and fill sequences
- Final positions, balances, and P&L
- Event logs (excluding wall-clock timestamps)

Enforced by a CI test that runs a fixed recording twice and compares output hashes.

## Hard test scenarios

The following must have dedicated tests:

1. Delta arrives before snapshot (buffered correctly)
2. A sequence number is skipped (re-sync triggered)
3. Duplicate delta received (discarded)
4. Best-bid level fully removed
5. One aggressive order walks multiple price levels
6. Cancel races with a fill (exactly one wins)
7. Two resting orders at the same price preserve time priority
8. Partial fill leaves residual quantity at the same priority
9. Risk rejects an order before it reaches the matcher (no state mutation)
10. Replay of the same recording produces identical output hashes across runs
11. Fixed-point arithmetic: no precision drift after 1M random price/qty operations

## Numeric correctness

- All money math is fixed-point integer arithmetic.
- Division (e.g. average fill price) uses explicit rounding modes, documented at each call site.
- Conversions at boundaries (feed parsing, UI) are the only places floats/decimals may appear, and they must round-trip-tested against the fixed-point representation.
