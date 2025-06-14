import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt


datos = pd.read_csv("data/datos_1_y_prior_to_20240613.csv")
last_Day = pd.read_csv("data/last_Day_1_y_prior_to_20240613.csv")

# Convert date columns to datetime
datos['date'] = pd.to_datetime(datos['date'])
last_Day['lastBusinessDay'] = pd.to_datetime(last_Day['lastBusinessDay'])
last_Day['lastTradingDay'] = pd.to_datetime(last_Day['lastTradingDay'])


r1 = {'lastBusinessDay': last_Day.loc[0, 'lastBusinessDay'], 'lastTradingDay': last_Day.loc[0, 'lastTradingDay']}
last_Day = pd.concat([pd.DataFrame([r1]), last_Day], ignore_index=True)


datos['FrontSynthetic'] = 0
datos['ThirteenthSynthetic'] = 0

roll_diff_F = 0
roll_diff_T = 0
indE = datos.index[-1]

# Identify index for alignment
for indT in range(last_Day.index[-1], -1, -1):
    if datos.loc[indE, 'date'] > last_Day.loc[indT, 'lastTradingDay']:
        break
indB = indT + 1

# Create last entry
if datos.loc[indE, 'date'] == last_Day.loc[indB, 'lastBusinessDay']:
    roll_diff_F += datos.loc[indE, 'SecondMonth'] - datos.loc[indE, 'FrontMonth']
    roll_diff_T += datos.loc[indE, 'FourteenthMonth'] - datos.loc[indE, 'ThirteenthMonth']
    datos.loc[indE, 'FrontSynthetic'] = datos.loc[indE, 'FrontMonth'] + roll_diff_F
    datos.loc[indE, 'ThirteenthSynthetic'] = datos.loc[indE, 'ThirteenthMonth'] + roll_diff_T
else:
    datos.loc[indE, 'FrontSynthetic'] = datos.loc[indE, 'SecondMonth'] + roll_diff_F
    datos.loc[indE, 'ThirteenthSynthetic'] = datos.loc[indE, 'FourteenthMonth'] + roll_diff_T


for ind in range(indE - 1, -1, -1):
    if datos.loc[ind, 'date'] == last_Day.loc[indT, 'lastTradingDay']:
        indT -= 1
        indB -= 1
        datos.loc[ind, 'FrontSynthetic'] = datos.loc[ind, 'SecondMonth'] + roll_diff_F
        datos.loc[ind, 'ThirteenthSynthetic'] = datos.loc[ind, 'FourteenthMonth'] + roll_diff_T
    elif datos.loc[ind, 'date'] == last_Day.loc[indB, 'lastBusinessDay']:
        roll_diff_F += datos.loc[ind, 'SecondMonth'] - datos.loc[ind, 'FrontMonth']
        roll_diff_T += datos.loc[ind, 'FourteenthMonth'] - datos.loc[ind, 'ThirteenthMonth']
        datos.loc[ind, 'FrontSynthetic'] = datos.loc[ind, 'FrontMonth'] + roll_diff_F
        datos.loc[ind, 'ThirteenthSynthetic'] = datos.loc[ind, 'ThirteenthMonth'] + roll_diff_T
    else:
        datos.loc[ind, 'FrontSynthetic'] = datos.loc[ind, 'FrontMonth'] + roll_diff_F
        datos.loc[ind, 'ThirteenthSynthetic'] = datos.loc[ind, 'ThirteenthMonth'] + roll_diff_T


datos['Carry'] = datos['FrontSynthetic'] - datos['ThirteenthSynthetic']
datos['CarrySMA20'] = datos['Carry'].rolling(20).mean()
datos['CarryMom'] = datos['Carry'] - datos['CarrySMA20']


def backtest_strategy(df, signal_column, start_index, end_index):
    pos = 0
    open_p = df.loc[start_index, 'FrontSynthetic']
    pos = 1 if df.loc[start_index, signal_column] > 0 else -1
    PnL, logPnL, cross_index = [0], [0], [start_index]

    for i in range(start_index + 1, end_index + 1):
        close_p = df.loc[i, 'FrontSynthetic']
        PnL.append(pos * (close_p - open_p))
        logPnL.append(pos * np.log(close_p / open_p))
        open_p = close_p

        if df.loc[i, signal_column] * df.loc[i - 1, signal_column] < 0:
            pos = 1 if df.loc[i, signal_column] > 0 else -1
            cross_index.append(i)

    results = pd.DataFrame({'date': df['date'].iloc[start_index:end_index + 1],
                            'PnL': PnL, 'logPnL': logPnL})
    return results, cross_index

start_idx, end_idx = 59, 318
carry_results, carry_cross = backtest_strategy(datos, 'Carry', start_idx, end_idx)
carry_mom_results, carry_mom_cross = backtest_strategy(datos, 'CarryMom', start_idx, end_idx)


print("Carry Strategy Total PnL:", round(carry_results.PnL.sum(), 2))
print("Carry Strategy Total Return (%):", round(carry_results.logPnL.sum() * 100, 2))
print("Carry-Momentum Strategy Total PnL:", round(carry_mom_results.PnL.sum(), 2))
print("Carry-Momentum Strategy Total Return (%):", round(carry_mom_results.logPnL.sum() * 100, 2))

# === EXPORT RESULTS ===
carry_results.to_csv("carry_strategy_results.csv", index=False)
carry_mom_results.to_csv("carry_momentum_strategy_results.csv", index=False)
