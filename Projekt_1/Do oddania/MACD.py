import pandas as pd
import matplotlib.pyplot as plt

# Wczytanie danych z pliku CSV
df = pd.read_csv('nvda_us_d.csv').head(1000)
price = df['Zamkniecie']

def EMA(df, n):
    ema = []
    alpha = 2 / (n + 1)
    ema.append(price.iloc[0])

    denominator = 1
    for i in range(1, n):
        denominator += (1 - alpha) ** i

    for i in range(1, len(df)):
        numerator = price.iloc[i]
        for j in range(1, n):
            if i - j >= 0:
                numerator += (1 - alpha) ** j * price.iloc[i - j]
            else:
                numerator += (1 - alpha) ** j * price.iloc[0]
        ema_value = numerator / denominator
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
    denominator = 1
    for i in range(1, n_sign):
        denominator += (1 - alpha) ** i

    for i in range(1, len(MACDline)):
        numerator = MACDline[i]
        for j in range(1, n_sign):
            if i - j >= 0:
                numerator += (1 - alpha) ** j * MACDline[i - j]
            else:
                numerator += (1 - alpha) ** j * MACDline[0]
        ema_value = numerator / denominator
        ema_signal.append(ema_value)

    return ema_signal


def trading_strategy(df, budget, stocks):
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
    #print(counter)
    signals.append('')
    return stocks, budget, budget_history, signals


def calculate_relative_growth_intervals(budget_history):
    initial_value = budget_history[0]
    final_value = budget_history[-1]
    relative_growth_25 = ((budget_history[len(budget_history)//4] - initial_value) / initial_value) * 100
    relative_growth_50 = ((budget_history[len(budget_history)//2] - initial_value) / initial_value) * 100
    relative_growth_75 = ((budget_history[3*len(budget_history)//4] - initial_value) / initial_value) * 100
    relative_growth_100 = ((final_value - initial_value) / initial_value) * 100
    return relative_growth_25, relative_growth_50, relative_growth_75, relative_growth_100


plt.figure(figsize=(10, 6))
plt.plot(price)
plt.title('Przebieg Wartosci')
plt.xlabel('Dzien')
plt.ylabel('Cena zamkniecia')
plt.grid(True)
plt.savefig('price.jpg')
plt.show()


n_first = 12
n_second = 26
n_sign = 9
stocks_starting = 1000
budget_starting = 0
starting_working_capital = stocks_starting * price.iloc[0]

df['MACD'] = MACD(df, n_first, n_second)
df['Signal'] = Signal(df, n_first, n_second, n_sign)

plt.figure(figsize=(10, 6))
plt.plot(df['MACD'], label='MACD', color = 'blue')
plt.plot(df['Signal'], label='Signal', color = 'red')
plt.title('Wskaznik MACD i Signal')
plt.xlabel('Dzien')
plt.ylabel('Wartosc')
plt.legend(loc='upper left')
plt.grid(True)
plt.savefig('MACD.jpg')
plt.show()


stocks, budget, budget_history, signals = trading_strategy(df, budget_starting, stocks_starting)

plt.figure(figsize=(10, 6))
plt.plot(price, label='Cena zamknięcia', color='black')
for i in range(len(signals)):
    if signals[i] == 'BUY':
        plt.scatter(i, price.iloc[i], marker='^', color='green', s=50, label='Buy', zorder=3)
    elif signals[i] == 'SELL':
        plt.scatter(i, price.iloc[i], marker='v', color='red', s=50, label='Sell', zorder=3)
plt.title('Transakcje kupna/sprzedaży na podstawie MACD i Signal')
plt.xlabel('Dzien')
plt.ylabel('Cena zamknięcia')
plt.grid(True)
plt.savefig('transactions.jpg')
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(price[600:800], label='Cena zamknięcia', color='black')
for i in range(600, 800):
    if signals[i] == 'BUY':
        plt.scatter(i, price.iloc[i], marker='^', color='green', s=50, label='Buy', zorder=3)
    elif signals[i] == 'SELL':
        plt.scatter(i, price.iloc[i], marker='v', color='red', s=50, label='Sell', zorder=3)
plt.title('Przyblizone transakcje kupna/sprzedaży na podstawie MACD i Signal')
plt.xlabel('Dzien')
plt.ylabel('Cena zamknięcia')
plt.grid(True)
plt.savefig('transactions_mini.jpg')
plt.show()


plt.figure(figsize=(10, 6))
plt.plot(budget_history)
plt.title('Historia Wartosci Portfolio')
plt.xlabel('Dzien')
plt.ylabel('Wartosc')
plt.grid(True)
plt.savefig('budget_history.jpg')
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(budget_history[600:800])
plt.title('Historia Wartosci Portfolio')
plt.xlabel('Dzien')
plt.ylabel('Wartosc')
plt.grid(True)
plt.savefig('budget_history_mini.jpg')
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(budget_history[400:600])
plt.title('Historia Wartosci Portfolio')
plt.xlabel('Dzien')
plt.ylabel('Wartosc')
plt.grid(True)
plt.savefig('budget_history_mini2.jpg')
plt.show()

print("Poczatkowa liczba akcji: ", stocks_starting)
print("Poczatkowa wartosc akcji: ", starting_working_capital)
print("Poczatkowy budzet: ", budget_starting)
print("Koncowa liczba akcji: ", stocks)
print("Koncowa wartosc akcji: ", price.iloc[-1] * stocks)
print("Koncowy budzet: ", budget)
print()

relative_growth_25, relative_growth_50, relative_growth_75, relative_growth_100 = calculate_relative_growth_intervals(budget_history)
print("Wartosci wzglednego wzrostu w poszczegolnych kwartalach:")
print("1/4: ", round(relative_growth_25, 2), "%")
print("1/2: ", round(relative_growth_50, 2), "%")
print("3/4: ", round(relative_growth_75, 2), "%")
print("Calkowity: ", round(relative_growth_100, 2), "%")
