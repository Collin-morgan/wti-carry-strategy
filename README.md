# wti-carry-strategy
Backtested WTI Carry and Carry-Momentum Futures Strategy using synthetic contract roll logic, based on academic research.

# WTI Carry and Carry-Momentum Futures Strategy

We explore the use of futures term structure signals—specifically **Carry** and **Carry Momentum**—to construct a systematic trading strategy in the WTI Crude Oil market over a one-year period from June 2023 to June 2024.

## Data Sources

This quantitative model uses historical prices from front and deferred-month WTI futures contracts. The synthetic contracts are constructed based on rolling methodologies outlined in:

**I. Bouchouev, _Energy Quantamentals: Myths and Realities about Algorithmic Oil Traders_, Oxford Institute for Energy Studies (2024)**

The roll dates are determined using the last business and trading days of each front-month contract. The synthetic front and thirteenth-month contracts are used to model carry exposure consistently through monthly roll cycles.

## Strategy Description

We define **Carry** as the spread between the front-month synthetic contract and the thirteenth-month synthetic contract. **Carry Momentum** is defined as the difference between the current Carry and its 20-day simple moving average.

Two separate strategies are backtested:
- **Carry Strategy**: Long when carry is positive; short when carry is negative
- **Carry-Momentum Strategy**: Long when carry momentum is positive; short when it is negative

Positions are updated daily, and the strategy rolls on the last business day of each month. Backtesting is conducted using log returns and daily PnL.

## Results

| Metric                              | Carry Strategy     | Carry-Momentum Strategy |
|-------------------------------------|---------------------|--------------------------|
| Total PnL ($/barrel)               | 10.81               | 16.67                    |
| Total Log-Return (%)               | 14.61%              | 21.93%                   |
| Net PnL (3 MCL contracts after fees) | ~$3,226             | ~$4,900                  |

## Implementation

The full implementation is provided in the Python script `wti_carry_strategy.py`. This script handles:
- Data loading and pre-processing
- Construction of synthetic contracts
- Calculation of carry and momentum signals
- Regime-based strategy backtesting
- Output of PnL and return metrics

All intermediate and final results are stored in the `results` directory.

## Acknowledgements

This project is based on methodology and insights introduced by Dr. I. Bouchouev in his research at the Oxford Institute for Energy Studies. We acknowledge the importance of academic research in bridging real-world commodity markets and systematic trading frameworks.

## Disclaimer

This strategy is strictly for educational and research purposes. It is a simulation only. No part of this model should be used for live trading or financial decision-making.
