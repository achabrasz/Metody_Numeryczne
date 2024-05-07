import matplotlib.pyplot as plt

def Exercise_E(file):
    E_Sizes = []
    E_LU_Time = []
    E_Jacobi_Time = []
    E_Gauss_Time = []
    e = 0
    for i, line in enumerate(file):
        #print(line)
        if e == 4:
            e = 1
        if i % 2 == 0 and e == 3:
            line = line.split()
            E_LU_Time.append(float(line[1])/1000)
            e = 4
        if i % 2 == 0 and e == 2:
            line = line.split()
            E_Gauss_Time.append(float(line[1])/1000)
            e = 3
        if i % 2 == 0 and e == 1:
            line = line.split()
            E_Jacobi_Time.append(float(line[1])/1000)
            e = 2
        if e == 0:
            line = line.rstrip()
            E_Sizes = line.split()
            e = 1
    return E_Sizes, E_LU_Time, E_Jacobi_Time, E_Gauss_Time

def Exercise_D(file):
    D_LU_Norm = 0
    for line in file:
        #print(line)
        line = line.split()
        if line[0] == "Norm:":
            D_LU_Norm = float(line[1])
            return D_LU_Norm

def Exercise_C(file):
    C_Jacobi_Norm = []
    C_Jacobi_Iters = 0
    C_Jacobi_Time = 0
    C_Gauss_Norm = []
    C_Gauss_Iters = 0
    C_Gauss_Time = 0
    isJacobi = True
    for line in file:
        line = line.split()
        if line[0] == "Norm:":
            if isJacobi:
                C_Jacobi_Norm = line[1:]
            else:
                C_Gauss_Norm = line[1:]
        if line[0] == "Iterations:":
            if isJacobi:
                C_Jacobi_Iters = int(line[1])
            else:
                C_Gauss_Iters = int(line[1])
        if line[0] == "Time:":
            if isJacobi:
                C_Jacobi_Time = float(line[1])
            else:
                C_Gauss_Time = float(line[1])
                return C_Jacobi_Norm, C_Jacobi_Iters, C_Jacobi_Time, C_Gauss_Norm, C_Gauss_Iters, C_Gauss_Time
        if line[0] == "Gauss":
            isJacobi = False
    return C_Jacobi_Norm, C_Jacobi_Iters, C_Jacobi_Time, C_Gauss_Norm, C_Gauss_Iters, C_Gauss_Time

def Exercise_B(file):
    B_Jacobi_Norm = []
    B_Jacobi_Iters = 0
    B_Jacobi_Time = 0
    B_Gauss_Norm = []
    B_Gauss_Iters = 0
    B_Gauss_Time = 0
    isJacobi = True
    for line in file:
        line = line.split()
        if line[0] == "Norm:":
            if isJacobi:
                B_Jacobi_Norm = line[1:]
            else:
                B_Gauss_Norm = line[1:]
        if line[0] == "Iterations:":
            if isJacobi:
                B_Jacobi_Iters = int(line[1])
            else:
                B_Gauss_Iters = int(line[1])
        if line[0] == "Time:":
            if isJacobi:
                B_Jacobi_Time = float(line[1])
            else:
                B_Gauss_Time = float(line[1])
                return B_Jacobi_Norm, B_Jacobi_Iters, B_Jacobi_Time, B_Gauss_Norm, B_Gauss_Iters, B_Gauss_Time
        if line[0] == "Gauss":
            isJacobi = False
    return B_Jacobi_Norm, B_Jacobi_Iters, B_Jacobi_Time, B_Gauss_Norm, B_Gauss_Iters, B_Gauss_Time

def plot_B(B_Jacobi_Norm, B_Jacobi_Iters, B_Jacobi_Time, B_Gauss_Norm, B_Gauss_Iters, B_Gauss_Time):
    for i in range(len(B_Jacobi_Norm)):
        if B_Jacobi_Norm[i] == '-nan(ind)':
            B_Jacobi_Norm[i] = 'inf'
        B_Jacobi_Norm[i] = float(B_Jacobi_Norm[i])

    for i in range(len(B_Gauss_Norm)):
        if B_Gauss_Norm[i] == '-nan(ind)':
            B_Gauss_Norm[i] = 'inf'
        B_Gauss_Norm[i] = float(B_Gauss_Norm[i])

    plt.plot(B_Jacobi_Norm, label='Jacobi')
    plt.plot(B_Gauss_Norm, label='Gauss')
    plt.yscale('log')
    plt.xlabel('Iterations')
    plt.ylabel('Norm')
    plt.title('Exercise B')
    plt.legend()
    plt.show()

    print("Jacobi Iterations: ", B_Jacobi_Iters)
    print("Jacobi Time: ", B_Jacobi_Time, " ms")
    print("Jacobi Norm: ", B_Jacobi_Norm[-1])
    plt.plot(B_Jacobi_Norm[:100], label='Jacobi')
    plt.yscale('log')
    plt.xlabel('Iterations')
    plt.ylabel('Norm')
    plt.title('Exercise B Jacobi')
    plt.legend()
    plt.show()

    print("Gauss Iterations: ", B_Gauss_Iters)
    print("Gauss Time: ", B_Gauss_Time, " ms")
    print("Gauss Norm: ", B_Gauss_Norm[-1])
    plt.plot(B_Gauss_Norm, label='Gauss')
    plt.yscale('log')
    plt.xlabel('Iterations')
    plt.ylabel('Norm')
    plt.title('Exercise B Gauss')
    plt.legend()
    plt.show()

def plot_C(C_Jacobi_Norm, C_Jacobi_Iters, C_Jacobi_Time, C_Gauss_Norm, C_Gauss_Iters, C_Gauss_Time):
    for i in range(len(C_Jacobi_Norm)):
        if C_Jacobi_Norm[i] == '-nan(ind)':
            C_Jacobi_Norm[i] = 'inf'
        C_Jacobi_Norm[i] = float(C_Jacobi_Norm[i])

    for i in range(len(C_Gauss_Norm)):
        if C_Gauss_Norm[i] == '-nan(ind)':
            C_Gauss_Norm[i] = 'inf'
        C_Gauss_Norm[i] = float(C_Gauss_Norm[i])

    print("Jacobi Iterations: ", C_Jacobi_Iters)
    print("Jacobi Time: ", C_Jacobi_Time, " ms")
    print("Jacobi Norm: ", C_Jacobi_Norm[-1])
    print("Gauss Iterations: ", C_Gauss_Iters)
    print("Gauss Time: ", C_Gauss_Time, " ms")
    print("Gauss Norm: ", C_Gauss_Norm[-1])
    plt.plot(C_Jacobi_Norm, label='Jacobi')
    plt.plot(C_Gauss_Norm, label='Gauss')
    plt.yscale('log')
    plt.xlabel('Iterations')
    plt.ylabel('Norm')
    plt.title('Exercise C')
    plt.legend()
    plt.show()

def plot_E(E_Sizes, E_LU_Time, E_Jacobi_Time, E_Gauss_Time):
    plt.plot(E_Sizes, E_LU_Time, label='LU')
    plt.plot(E_Sizes, E_Jacobi_Time, label='Jacobi')
    plt.plot(E_Sizes, E_Gauss_Time, label='Gauss')
    plt.xlabel('Size')
    plt.ylabel('Time')
    plt.title('Exercise E')
    plt.legend()
    plt.show()

def load():
    with open("data.txt") as file:
        for line in file:
            print(line)
            if line == "Exercise B\n":
                B_Jacobi_Norm, B_Jacobi_Iters, B_Jacobi_Time, B_Gauss_Norm, B_Gauss_Iters, B_Gauss_Time = Exercise_B(file)
                plot_B(B_Jacobi_Norm, B_Jacobi_Iters, B_Jacobi_Time, B_Gauss_Norm, B_Gauss_Iters, B_Gauss_Time)
            if line == "Exercise C\n":
                C_Jacobi_Norm, C_Jacobi_Iters, C_Jacobi_Time, C_Gauss_Norm, C_Gauss_Iters, C_Gauss_Time = Exercise_C(file)
                plot_C(C_Jacobi_Norm, C_Jacobi_Iters, C_Jacobi_Time, C_Gauss_Norm, C_Gauss_Iters, C_Gauss_Time)
            if line == "Exercise D\n":
                D_LU_Norm = Exercise_D(file)
                print("LU Norm: ", D_LU_Norm)
            if line == "Exercise E\n":
                E_Sizes, E_LU_Time, E_Jacobi_Time, E_Gauss_Time = Exercise_E(file)
                plot_E(E_Sizes, E_LU_Time, E_Jacobi_Time, E_Gauss_Time)

if __name__ == "__main__":
    load()