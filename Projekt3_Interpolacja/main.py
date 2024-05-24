from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

def reformat_Nodes(nodes, data):
    n = len(nodes)
    nodes_y = []
    nodes_x = []
    for i in range(n):
        nodes_x.append(data.iloc[nodes[i], 0])
        nodes_y.append(data.iloc[nodes[i], 1])
    return nodes_x, nodes_y

def spacing(even : bool, n, nodes_num):
    if even:
        nodes = np.linspace(0, n-1, nodes_num)
        return nodes.astype(int)
    else:
        return chebyshev_nodes(n, nodes_num)

def chebyshev_nodes(n, nodes_num):
    x = []
    jump = n//nodes_num
    for k in range(1, n+1, jump):
        x.append((int)((np.cos(k/(n-1)*np.pi)+1)*n/2))
    return x

#moze trzeba polaczyc te dwie funkcje pod stabilnosc numeryczna bo zaokragla do 2 miejsc po przecinku
def Lagrange(x0, x, i):
    n = len(x)
    L = 1
    for j in range(n):
        if j != i:
            L *= (x0 - x[j])/(x[i] - x[j])
    return L

def LagrangePolynomial(x0, x, y):
    n = len(x)
    P = 0
    for i in range(n):
        P += y[i]*Lagrange(x0, x, i)
    return P

def main():
    data = pd.read_csv(r'2018_paths/100.csv', sep = ',', header = None)
    nodes = spacing(False, data.shape[0], 20)
    nodes_x, nodes_y = reformat_Nodes(nodes, data)
    print(LagrangePolynomial(data.iloc[:, 0], nodes_x, nodes_y))
    plt.plot(LagrangePolynomial(data.iloc[:, 0], nodes_x, nodes_y), color = 'red')
    plt.plot(data.iloc[:, 1], color = 'blue')
    plt.plot(nodes, nodes_y, 'o', color = 'black')
    plt.show()

if __name__ == "__main__":
    main()
