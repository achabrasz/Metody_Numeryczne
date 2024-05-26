from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

def remove_duplicates(nodes):
    return list(dict.fromkeys(nodes))

def cubic_spline_interpolation(nodes, nodes_x, nodes_y, x, y):
    n = len(nodes)
    h = np.zeros(n-1)
    for i in range(n-1):
        h[i] = nodes_x[i+1] - nodes_x[i]

    A = np.zeros((n, n))
    A[0, 0] = 1
    A[n-1, n-1] = 1
    for i in range(1, n-1):
        A[i, i-1] = h[i-1]
        A[i, i] = 2*(h[i-1] + h[i])
        A[i, i+1] = h[i]

    B = np.zeros(n)
    for i in range(1, n-1):
        B[i] = 3*(nodes_y[i+1] - nodes_y[i])/h[i] - 3*(nodes_y[i] - nodes_y[i-1])/h[i-1]

    c = np.linalg.solve(A, B)

    a = np.zeros(n-1)
    b = np.zeros(n-1)
    d = np.zeros(n-1)
    for i in range(n-1):
        a[i] = nodes_y[i]
        b[i] = (nodes_y[i+1] - nodes_y[i])/h[i] - h[i]*(2*c[i] + c[i+1])/3
        d[i] = (c[i+1] - c[i])/(3*h[i])

    m = len(x)
    y_spline = []
    for i in range(int(x[m-1])):
        for j in range(n-1):
            if i >= nodes_x[j] and i <= nodes_x[j+1]:
                y_spline.append(a[j] + b[j]*(i - nodes_x[j]) + c[j]*(i - nodes_x[j])**2 + d[j]*(i - nodes_x[j])**3)
                break
    return y_spline


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
    for k in range(1, n, jump):
        x.append((int)((np.cos(k/(n-1)*np.pi)+1)*n/2))
    x.sort()
    x = remove_duplicates(x)
    return x


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
    data = pd.read_csv(r'2018_paths/tczew_starogard.txt', sep=' ', header=None)
    x = data.iloc[:, 0]
    y = data.iloc[:, 1]
    size = len(x)

    nodes = spacing(False, size, 30)
    nodes_x, nodes_y = reformat_Nodes(nodes, data)

    plt.title('Interpolation Cubic Spline - Tczew 30')
    #plt.title('Interpolation Lagrange Polynomial Tczew - 30')
    #plt.plot(x, LagrangePolynomial(x, nodes_x, nodes_y), color='red')
    plt.plot(cubic_spline_interpolation(nodes, nodes_x, nodes_y, x, y), color='red')
    plt.plot(x, y, color='blue')
    plt.plot(nodes_x, nodes_y, 'o', color='green', markersize=5)
    plt.xlabel('Odleglosc')
    plt.ylabel('Wysokosc')
    plt.show()


if __name__ == "__main__":
    main()

