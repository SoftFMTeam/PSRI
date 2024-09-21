import math

import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model


def func(X, a, b):
    return a * np.power(X, b)


def plot_data(data, x_label, y_label, title, path, save):
    plt.draw()

    if isinstance(data, list) and isinstance(y_label, list) and len(data) == len(y_label):
        for i in range(len(data)):
            plt.plot(data[i][0], data[i][1], label=y_label[i])
    elif isinstance(data, tuple) and isinstance(y_label, str):
        plt.plot(data[0], data[1])
        plt.ylabel(y_label)

    plt.title(title)
    plt.xlabel(x_label)

    if save and path is not None:
        plt.savefig(path, dpi=300, format='png')
    else:
        plt.show()


def DataGenerate(data):
    data_time = dict()
    length = math.ceil(data.shape[0])

    for i in range(length):
        if data_time.get(data.iloc[i][0]) is None:
            data_time[data.iloc[i][0]] = 1.0
        else:
            data_time[data.iloc[i][0]] += 1.0

    dict_num = sorted(data_time.items(), reverse=False)

    print(data_time)
    print(dict_num)
    dict_x = []
    dict_y = []
    for key, value in dict_num:
        dict_x.append(key)
        dict_y.append(value)

    dict_x = np.array(dict_x)
    dict_y = np.array(dict_y)

    plt.figure(figsize=(12, 6))
    plt.plot(dict_x, dict_y)
    plt.ylabel('Frequency')
    plt.xlabel('NCC')
    plt.title('NCC: distribution of "nginx" entity nodes')

    base = 10
    dict_x = np.log10(dict_x)
    dict_y = np.log10(dict_y)
    return dict_x, dict_y


def DataFitAndVisualization(X, Y):
    Y = np.log10(Y)
    X_parameter = []
    Y_parameter = []
    for single_square_feet, single_price_value in zip(X, Y):
        X_parameter.append([float(single_square_feet)])
        Y_parameter.append(float(single_price_value))

    regression = linear_model.LinearRegression()
    regression.fit(X_parameter, Y_parameter)
    print('Coefficients: \n', regression.coef_, )
    print("Intercept:\n", regression.intercept_)
    # The mean square error
    print("Residual sum of squares: %.8f"
          % np.mean((regression.predict(X_parameter) - Y_parameter) ** 2))  # 残差平方和

    plt.title("Log Data")
    plt.scatter(X_parameter, Y_parameter, color='black')
    plt.plot(X_parameter, regression.predict(X_parameter), color='blue', linewidth=3)

    return regression.coef_, regression.intercept_


def DrawCurveLine(x, a, b):
    y = list()
    for i in x:
        y.append(func(i, a, b))
    plt.figure(figsize=(12, 6))
    plt.plot(x, y)
    plt.ylabel('Frequency')
    plt.xlabel('NCC')
    plt.title('NCC: distribution of "nginx" entity nodes')
    plt.show()


if __name__ == '__main__':
    px, py = DataGenerate()
    Coefficients, Intercept = DataFitAndVisualization(px, py)
    truX, truIntercept = np.power(10, px), np.power(10, Intercept)
    DrawCurveLine(truX, truIntercept, Coefficients)
