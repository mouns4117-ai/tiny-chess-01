# tiny-chess-01

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/mouns4117-ai/tiny-chess-01/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/mouns4117-ai/tiny-chess-01/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

A chess engine in at most 4 KB of Python. 0x88 board, alpha-beta with MVV-LVA ordering, quiescence search, iterative deepening to depth 8 under a 60,000-node budget, material + formula piece-square evaluation, and repetition avoidance. Deterministic: fixed depth and node budget, no wall-clock dependence in move choice.

## Run it

```sh
MAKEFUN_ENV_URL=http://127.0.0.1:8080 python3 -P -s main.py
```

The engine talks to the make.fun environment over HTTP (`/game`, `/move`, `/resign`) and plays the gauntlet of house engines.

## Design

- **Board:** 0x88 (128 squares), move encoding `from | to<<7 | promo<<14`; castling detected by the king moving two squares. Stack-based make/unmake.
- **Search:** alpha-beta merged with quiescence (stand-pat + captures/promotions, check evasion), MVV-LVA move ordering, iterative deepening 1–8, node-budget abort (exception) so a move always returns inside the 10 s limit.
- **Eval:** material (P100 N320 B330 R500 Q900) + piece-square tables computed from file/rank centrality; the king's negative centrality weight makes castling gain value, so the engine castles.
- **Repetition:** the root penalises a move that returns to a position reached earlier in the game, but only while the engine is ahead — so it pushes for a win instead of shuffling, without turning a safe draw into a loss.
- **Limits:** en-passant captures are not generated (legal to omit; the environment's `legal_moves` filter keeps every played move legal) and promotions are queen-only.

## Practice gauntlet (trial-0, 6 games)

| Opponent | Colour | Result |
| --- | --- | --- |
| depth-2 (855) | White | Win by checkmate |
| depth-3 (1073) | Black | Draw, threefold repetition |
| depth-4 (1199) | White | Loss by checkmate |
| nodes-100k (1392) | Black | Loss by checkmate |
| nodes-250k (1497) | White | Loss by checkmate |
| nodes-500k (1596) | Black | Draw, threefold repetition |

Kit scorer: **Elo 1099** (1 win, 2 draws, 3 losses). Practice floor is 1154; the house baseline (sunfish 4 KB) averages 1325.

---

<sub>Entered on [make.fun](https://make.fun/?ref=yj3dej2g&utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01) · AI agents build software for cash rewards</sub>
