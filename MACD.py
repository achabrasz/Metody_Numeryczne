import pandas as pd
import matplotlib.pyplot as plt

# Wczytanie danych z pliku CSV
df = pd.read_csv('DaneApple2020_2024.csv').head(1000)
price = df['Close']
date = df['Date']
print(len(df))
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
    for i in range(1, len(df)):
        if df['MACD'].iloc[i] > df['Signal'].iloc[i] and df['MACD'].iloc[i - 1] <= df['Signal'].iloc[i - 1]:
            signals.append('BUY')
        elif df['MACD'].iloc[i] < df['Signal'].iloc[i] and df['MACD'].iloc[i - 1] >= df['Signal'].iloc[i - 1]:
            signals.append('SELL')
        else:
            signals.append('')

    signals.append('')

    return signals

def trading_algorithm (df, signals, budget, stocks):
    #polacz dwie funkcje i dorob delte
    for i in range(1, len(df)):
        if signals[i] == 'BUY' and budget > 0:
            stocks = budget // price.iloc[i]
            budget = 0
        elif signals[i] == 'SELL' and stocks > 0:
            budget = budget + price.iloc[i]*stocks
            stocks = 0
    return stocks, budget


#Wykres akcji
plt.plot(date, price)
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

df['MACD'] = MACD(df, n_first, n_second)
df['Signal'] = Signal(df, n_first, n_second, n_sign)

# Wykres MACD i Signal
plt.plot(date, df['MACD'], label='MACD', color = 'blue')
plt.plot(date, df['Signal'], label='Signal', color = 'red')
plt.title('Wskaznik MACD i Signal')
plt.xlabel('Data')
plt.ylabel('Wartosc')
plt.legend(loc='upper left')
plt.grid(True)
plt.show()

# Generowanie kupna/sprzedazy
signals = trading_strategy(df)

# Wykres kupna/sprzedaży
plt.figure(figsize=(10, 6))
plt.plot(date, price, label='Cena zamknięcia', color='black')
for i in range(len(signals)):
    if signals[i] == 'BUY':
        plt.scatter(date.iloc[i], price.iloc[i], marker='^', color='green', s=50, label='Kupno', zorder=3)
    elif signals[i] == 'SELL':
        plt.scatter(date.iloc[i], price.iloc[i], marker='v', color='red', s=50, label='Sprzedaż', zorder=3)
plt.title('Transakcje kupna/sprzedaży na podstawie MACD i Signal')
plt.xlabel('Data')
plt.ylabel('Cena zamknięcia')
plt.grid(True)
plt.show()

stocks, budget = trading_algorithm(df, signals, budget_starting, stocks_starting)

print("Warotsc poczatkowa: ", starting_working_capital)
print("Poczatkowy budzet: ", budget_starting)
print("Poczatkowa liczba akcji: ", stocks_starting)
print("Koncowa liczba akcji: ", stocks)
print("Koncowa wartosc akcji: ", price.iloc[-1] * stocks)
print("Koncowy budzet: ", budget)