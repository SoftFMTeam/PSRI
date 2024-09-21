import collections
import math

import numpy as np
import powerlaw
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit


def powerlaw_func(x, pa, pc):
    return pc * (x ** -pa)


def liner_func(x, alpha, pb):
    return pb - alpha * x


def powerlaw_curve_fit_log(logX, logY, alpha):
    def _liner_func_(x, pb):
        return pb - alpha * x

    popt, pcov = curve_fit(_liner_func_, logX, logY)
    pBeta = popt[0]
    pC = math.exp(pBeta)

    return pBeta, pC


def powerlaw_fit(data, xmin=None, bi=0, plotPdf=False, plotCcdf=False, title=None, kMinPlot=False):
    if bi:
        if isinstance(data, np.ndarray):
            data = data + bi
        elif isinstance(data, list):
            data = [x + bi for x in data]
    if xmin:
        fit = powerlaw.Fit(data, discrete=True, xmin=xmin)
    else:
        fit = powerlaw.Fit(data, discrete=True)
    alpha = fit.alpha
    sigma = fit.sigma
    xMin = fit.xmin
    D = fit.D

    counter = dict(collections.Counter(data))
    X = np.asarray([x + bi for x in counter.keys()])
    Y = np.asarray(list(counter.values()))
    logX = np.log2(X)
    logY = np.log2(Y)

    def _liner_func_(x, pb):
        return pb - alpha * x

    popt, pcov = curve_fit(_liner_func_, logX, logY)
    pBeta = popt[0]
    pC = np.exp2(pBeta)

    if plotPdf:
        fig = fit.plot_pdf(marker='o', color='r', linewidth=1, linear_bins=False, label='Logarithmic binning')
        fit.power_law.plot_pdf(color='g', linestyle='-', ax=fig,
                               label=f'alpha={round(alpha, 2)} kMin={xMin} D={round(D, 2)}')
        plt.legend()
        if title:
            plt.title(title + 'dfp')
        plt.show()

    if plotCcdf:
        fig = fit.plot_ccdf(marker='o', color='b', linewidth=1, label=r'Logarithmic binning')
        fit.power_law.plot_ccdf(color='b', linestyle='-', ax=fig,
                               label=f'alpha={round(alpha, 2)} kMin={xMin} D={round(D, 2)}')
        plt.legend()
        if title:
            plt.title(title + 'ccdf')
        plt.show()

    if kMinPlot:
        D_list = []
        for x in np.linspace(1, 51, 26):
            fit = powerlaw.Fit(data, xmin=x)
            D_list.append(fit.power_law.D)

        plt.plot(np.linspace(1, 51, 26), D_list, "r-")
        plt.xlabel("$K_{min}$")
        plt.ylabel("$D$")
        plt.yscale("log")
        if title:
            plt.title(title + ' $D$ values under different $K_{min}$ values')
        else:
            plt.title(' $D$ values under different $K_{min}$ values')
        plt.show()

    info = {
        'alpha': alpha,
        'sigma': sigma,
        'xMin': xMin,
        'pBeta': pBeta,
        'pC': pC,
        'D': D
    }

    return fit, info, X, Y, logX, logY
