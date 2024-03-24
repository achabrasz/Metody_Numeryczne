import pandas as pd
import matplotlib.pyplot as plt

# Wczytanie danych z pliku CSV
df = pd.read_csv('wig20.csv').head(1000)
price = df['Zamkniecie']
date = df['Data']

def EMA3(df, n):
    ema = []
    alpha = 2 / (n + 1)
    ema.append(price.iloc[0])

    denominator = 1
    for i in range(1, n):
        denominator += (1 - alpha) ** i

    for i in range(1, len(df)):
        numerator = price.iloc[i]
        for j in range(1, n):
            numerator += (1 - alpha) ** j * price.iloc[i - j]
        ema_value = numerator / denominator
        ema.append(ema_value)

    return ema

def MACD3(df, n_first, n_second):
    EMAfirst = EMA(df, n_first)
    EMAsecond = EMA(df, n_second)
    MACD = [EMAfirst[i] - EMAsecond[i] for i in range(len(EMAfirst))]
    return MACD

def Signal3(df, n_first, n_second, n_sign):
    MACDline = MACD(df, n_first, n_second)
    ema_signal = []
    alpha = 2 / (n_sign + 1)

    denominator = 1
    for i in range(1, n_sign):
        denominator += (1 - alpha) ** i

    for i in range(len(MACDline)):
        numerator = MACDline[i]
        for j in range(1, n_sign):
            numerator += (1 - alpha) ** j * MACDline[i - j]
        ema_value = numerator / denominator
        ema_signal.append(ema_value)

    return ema_signal


def EMA2(df, n):
    EMA = pd.Series(price.ewm(span=n, min_periods=n).mean(), name='EMA_' + str(n))
    return EMA

def MACD2(df, n_fast, n_slow):
    EMAfast = EMA2(df, n_fast)
    EMAslow = EMA2(df, n_slow)
    MACD = pd.Series(EMAfast - EMAslow, name='MACD')
    return MACD

def Signal2(df, n_fast, n_slow, n_sign):
    MACDline = MACD2(df, n_fast, n_slow)
    Signal = pd.Series(MACDline.ewm(span=n_sign, min_periods=n_sign).mean(), name='Signal')
    return Signal

def EMA(df, n):
    ema = []
    alpha = 2 / (n + 1)
    ema.append(price.iloc[0])

    for i in range(1, len(df)):
        ema_value = alpha * price.iloc[i] + (1 - alpha) * ema[i - 1]
        ema.append(ema_value)

    return ema

def MACD(df, n_first, n_second):
    EMAfirst = EMA(df, n_first)
    EMAsecond = EMA(df, n_second)
    MACD = [EMAfirst[i] - EMAsecond[i] for i in range(len(EMAfirst))]
    return MACD


def Signal(df, n_first, n_second, n_sign):
    MACDline = MACD(df, n_first, n_second)
    ema_signal = []
    alpha = 2 / (n_sign + 1)
    ema_signal.append(MACDline[0])

    for i in range(1, len(MACDline)):
        ema_value = alpha * MACDline[i] + (1 - alpha) * ema_signal[i - 1]
        ema_signal.append(ema_value)

    return ema_signal



def trading_strategy(df):
    signals = []
    counter = 0
    for i in range(1, len(df)):
        if df['MACD'].iloc[i] > df['Signal'].iloc[i] and df['MACD'].iloc[i - 1] <= df['Signal'].iloc[i - 1]:
            signals.append('BUY')
            counter+=1
        elif df['MACD'].iloc[i] < df['Signal'].iloc[i] and df['MACD'].iloc[i - 1] >= df['Signal'].iloc[i - 1]:
            signals.append('SELL')
            counter+=1
        else:
            signals.append('')

    signals.append('')
    print(counter)
    return signals

def trading_algorithm (df, signals, budget, stocks):
    #polacz dwie funkcje i dorob delte
    budget_history = []
    for i in range(1, len(df)):
        if signals[i] == 'BUY' and budget > 0:
            stocks = budget // price.iloc[i]
            budget = 0
        elif signals[i] == 'SELL' and stocks > 0:
            budget = budget + price.iloc[i]*stocks
            stocks = 0
        budget_history.append(budget + stocks * price.iloc[i])
    budget_history.append(budget + stocks * price.iloc[-1])
    return stocks, budget, budget_history

def trading_strategy2(df, budget, stocks):
    counter = 0
    budget_history = []
    signals = []
    budget_history.append(budget + stocks * price.iloc[0])
    delta_1 = df['MACD'].iloc[0] - df['Signal'].iloc[0]
    for i in range(1, len(df)):
        delta_2 = df['MACD'].iloc[i] - df['Signal'].iloc[i]
        if delta_1 <= 0 and delta_2 >= 0:
            if budget > 0:
                signals.append('BUY')
                stocks = budget // price.iloc[i]
                budget -= stocks * price.iloc[i]
                counter += 1
        elif delta_1 >= 0 and delta_2 <= 0:
            if stocks > 0:
                signals.append('SELL')
                budget += stocks * price.iloc[i]
                stocks = 0
                counter += 1
        else:
            signals.append('')
        delta_1 = delta_2
        budget_history.append(budget + stocks * price.iloc[i])
    budget_history.append(budget + stocks * price.iloc[-1])
    print(counter)
    signals.append('')
    return stocks, budget, budget_history, signals


#Wykres akcji
plt.figure(figsize=(10, 6))
plt.plot(price)
plt.title('Przebieg Wartosci')
plt.xlabel('Data')
plt.ylabel('Cena zamkniecia')
plt.grid(True)
plt.show()

# Obliczenie MACD i Signal
n_first = 12
n_second = 26
n_sign = 9
stocks_starting = 1000
budget_starting = 0
starting_working_capital = stocks_starting * price.iloc[0]

df['MACD'] = MACD2(df, n_first, n_second)
df['Signal'] = Signal2(df, n_first, n_second, n_sign)

# Wykres MACD i Signal
plt.figure(figsize=(10, 6))
plt.plot(df['MACD'], label='MACD', color = 'blue')
plt.plot(df['Signal'], label='Signal', color = 'red')
plt.title('Wskaznik MACD i Signal')
plt.xlabel('Data')
plt.ylabel('Wartosc')
plt.legend(loc='upper left')
plt.grid(True)
plt.show()

# Generowanie kupna/sprzedazy
#signals = trading_strategy(df)

#stocks, budget, budget_history = trading_algorithm(df, signals, budget_starting, stocks_starting)
stocks, budget, budget_history, signals = trading_strategy2(df, budget_starting, stocks_starting)

# Wykres kupna/sprzedaży
plt.figure(figsize=(10, 6))
plt.plot(price, label='Cena zamknięcia', color='black')
for i in range(len(signals)):
    if signals[i] == 'BUY':
        plt.scatter(i, price.iloc[i], marker='^', color='green', s=50, label='Buy', zorder=3)
    elif signals[i] == 'SELL':
        plt.scatter(i, price.iloc[i], marker='v', color='red', s=50, label='Sell', zorder=3)
plt.title('Transakcje kupna/sprzedaży na podstawie MACD i Signal')
plt.xlabel('Data')
plt.ylabel('Cena zamknięcia')
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(budget_history)
plt.title('Historia Wartosci Portfolio')
plt.xlabel('Data')
plt.ylabel('Wartosc')
plt.grid(True)
plt.show()

print("Warotsc poczatkowa: ", starting_working_capital)
print("Poczatkowy budzet: ", budget_starting)
print("Poczatkowa liczba akcji: ", stocks_starting)
print("Koncowa liczba akcji: ", stocks)
print("Koncowa wartosc akcji: ", price.iloc[-1] * stocks)
print("Koncowy budzet: ", budget)