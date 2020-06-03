from financeObj import *
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
import seaborn as sb
import yfinance as yf
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


class Factory:
    Calls = None
    Puts = None
    opt = None
    strikeChoice = None
    ticker = None
    DateArray = None
    financeObj = None

    def __init__(self, financeObj):
        self.financeObj = financeObj
        self.opt = financeObj.getOptionChain()
        self.Calls = self.opt.calls
        self.Puts = self.opt.puts
        self.strikeChoice = financeObj.getDateChoice()
        self.ticker = financeObj.getTicker()
        self.DateArray = financeObj.getDateArray()

    def update(self):
        self.opt = self.financeObj.getOptionChain()
        self.Calls = self.opt.calls
        self.Puts = self.opt.puts
        self.strikeChoice = self.financeObj.getDateChoice()
        self.ticker = self.financeObj.getTicker()
        self.DateArray = self.financeObj.getDateArray()

    def getCalls(self):
        return self.Calls

    def getPuts(self):
        return self.Puts

    def sortCallsandPuts(self):
        calls = self.opt.calls
        calls = cleaner(calls)
        calls['Mid Price'] = calls.apply(
            lambda row: (row.ask + row.bid)/2, axis=1)
        calls = calls.drop(columns=["ask", "bid"])
        self.Calls = calls[["strike", "Mid Price", "openInterest", "volume"]]
        puts = self.opt.puts
        puts = cleaner(puts)
        puts['Mid Price'] = puts.apply(
            lambda row: (row.ask + row.bid)/2, axis=1)
        puts = puts.drop(columns=["ask", "bid"])
        self.Puts = puts[["strike", "Mid Price", "openInterest", "volume"]]

    def OIChart(self):
        self.sortCallsandPuts()
        callData = self.Calls.drop(columns=['Mid Price', 'volume'])
        putData = self.Puts.drop(columns=['Mid Price', 'volume'])
        finalFrame = pd.DataFrame(callData)
        finalFrame.rename(columns={'openInterest': 'Calls'}, inplace=True)
        tempFrame = pd.DataFrame(putData)
        tempFrame.rename(columns={'openInterest': 'Puts'}, inplace=True)
        finalFrame = pd.merge(finalFrame, tempFrame, on='strike')
        finalFrame.plot.bar(figsize=(20, 8), x="strike", y=["Calls", "Puts"],
                            title="Open Interest for "+self.ticker.upper()+" all options at every strike on "+self.strikeChoice)
        plt.show()
        plt.clf()

    def CallsOIMap(self):  # plt.style.use("dark_background")
        callsArray = heatCleaner(self.opt.calls)
        callsArray.rename(
            columns={'openInterest': self.DateArray[1]}, inplace=True)
        for x in range(2, len(self.DateArray)-1):
            opt2 = yf.Ticker(self.ticker).option_chain(self.DateArray[x])
            callsArray2 = heatCleaner(opt2.calls)
            callsArray2.rename(
                columns={'openInterest': self.DateArray[x]}, inplace=True)
            callsArray = pd.merge(callsArray, callsArray2, on='strike')
        callsArray.set_index('strike', inplace=True)
        callsArray = callsArray.fillna(0)
        heat_map = sb.heatmap(callsArray, cmap="Reds", linewidths=0)
        plt.yticks(rotation=0)
        plt.xticks(rotation=50)
        plt.gca().invert_yaxis()
        plt.show()
        plt.clf()

    def PutsOIMap(self):  # plt.style.use("dark_background")
        callsArray = heatCleaner(self.opt.puts)
        callsArray.rename(
            columns={'openInterest': self.DateArray[1]}, inplace=True)
        for x in range(2, len(self.DateArray)-1):
            opt2 = yf.Ticker(self.ticker).option_chain(self.DateArray[x])
            callsArray2 = heatCleaner(opt2.puts)
            callsArray2.rename(
                columns={'openInterest': self.DateArray[x]}, inplace=True)
            callsArray = pd.merge(callsArray, callsArray2, on='strike')
        callsArray.set_index('strike', inplace=True)
        callsArray = callsArray.fillna(0)
        heat_map = sb.heatmap(callsArray, cmap="Blues", linewidths=0)
        plt.yticks(rotation=0)
        plt.xticks(rotation=50)
        plt.gca().invert_yaxis()
        plt.show()
        plt.clf()

    def CallsVolumeMap(self):
        callsArray = heatCleanerVOLUME(self.opt.calls)
        callsArray.rename(columns={'volume': self.DateArray[1]}, inplace=True)
        for x in range(2, len(self.DateArray)-1):
            opt2 = yf.Ticker(self.ticker).option_chain(self.DateArray[x])
            callsArray2 = heatCleanerVOLUME(opt2.calls)
            callsArray2.rename(
                columns={'volume': self.DateArray[x]}, inplace=True)
            callsArray = pd.merge(callsArray, callsArray2, on='strike')
        callsArray.set_index('strike', inplace=True)
        callsArray = callsArray.fillna(0)
        heat_map = sb.heatmap(callsArray, cmap="Reds", linewidths=0)
        plt.yticks(rotation=0)
        plt.xticks(rotation=50)
        plt.gca().invert_yaxis()
        plt.show()
        plt.clf()

    def PutsVolumeMap(self):
        callsArray = heatCleanerVOLUME(self.opt.puts)
        callsArray.rename(columns={'volume': self.DateArray[1]}, inplace=True)
        for x in range(2, len(self.DateArray)-1):
            opt2 = yf.Ticker(self.ticker).option_chain(self.DateArray[x])
            callsArray2 = heatCleanerVOLUME(opt2.puts)
            callsArray2.rename(
                columns={'volume': self.DateArray[x]}, inplace=True)
            callsArray = pd.merge(callsArray, callsArray2, on='strike')
        callsArray.set_index('strike', inplace=True)
        callsArray = callsArray.fillna(0)
        heat_map = sb.heatmap(callsArray, cmap="Blues", linewidths=0)
        plt.yticks(rotation=0)
        plt.xticks(rotation=50)
        plt.gca().invert_yaxis()
        plt.show()
        plt.clf()

    def threedeegraph(self, object):
        eg = object
        dx, dy = .8, .8
        fig = plt.figure(figsize=(10, 10))
        ax = Axes3D(fig)
        xpos = np.arange(eg.shape[0])
        ypos = np.arange(eg.shape[1])
        ax.set_xticks(xpos + dx/2)
        ax.set_yticks(ypos + dy/2)
        xpos, ypos = np.meshgrid(xpos, ypos)
        xpos = xpos.flatten()
        ypos = ypos.flatten()
        zpos = np.zeros(eg.shape).flatten()
        dz = eg.values.ravel(order='F')
        values = np.linspace(0.2, 1., xpos.ravel().shape[0])
        colors = cm.rainbow(values)
        ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color=colors)
        ax.w_yaxis.set_ticklabels(eg.columns)
        ax.w_xaxis.set_ticklabels(eg.index)
        ax.set_zlabel('Open Interest / Volume')
        plt.show()
        plt.clf()

    def CallsOI3D(self):
        callsArray = heatCleaner(self.opt.calls)
        callsArray.rename(
            columns={'openInterest': self.DateArray[1]}, inplace=True)
        for x in range(2, len(self.DateArray)-1):
            opt2 = yf.Ticker(self.ticker).option_chain(self.DateArray[x])
            callsArray2 = heatCleaner(opt2.calls)
            callsArray2.rename(
                columns={'openInterest': self.DateArray[x]}, inplace=True)
            callsArray = pd.merge(callsArray, callsArray2, on='strike')
        callsArray.set_index('strike', inplace=True)
        callsArray = callsArray.fillna(0)
        self.threedeegraph(callsArray)

    def PutsOI3D(self):
        callsArray = heatCleaner(self.opt.puts)
        callsArray.rename(
            columns={'openInterest': self.DateArray[1]}, inplace=True)
        for x in range(2, len(self.DateArray)-1):
            opt2 = yf.Ticker(self.ticker).option_chain(self.DateArray[x])
            callsArray2 = heatCleaner(opt2.puts)
            callsArray2.rename(
                columns={'openInterest': self.DateArray[x]}, inplace=True)
            callsArray = pd.merge(callsArray, callsArray2, on='strike')
        callsArray.set_index('strike', inplace=True)
        callsArray = callsArray.fillna(0)
        self.threedeegraph(callsArray)

    def CallsVolume3D(self):
        callsArray = heatCleanerVOLUME(self.opt.calls)
        callsArray.rename(columns={'volume': self.DateArray[1]}, inplace=True)
        for x in range(2, len(self.DateArray)-1):
            opt2 = yf.Ticker(self.ticker).option_chain(self.DateArray[x])
            callsArray2 = heatCleanerVOLUME(opt2.calls)
            callsArray2.rename(
                columns={'volume': self.DateArray[x]}, inplace=True)
            callsArray = pd.merge(callsArray, callsArray2, on='strike')
        callsArray.set_index('strike', inplace=True)
        callsArray = callsArray.fillna(0)
        self.threedeegraph(callsArray)

    def PutsVolume3D(self):
        callsArray = heatCleanerVOLUME(self.opt.puts)
        callsArray.rename(columns={'volume': self.DateArray[1]}, inplace=True)
        for x in range(2, len(self.DateArray)-1):
            opt2 = yf.Ticker(self.ticker).option_chain(self.DateArray[x])
            callsArray2 = heatCleanerVOLUME(opt2.puts)
            callsArray2.rename(
                columns={'volume': self.DateArray[x]}, inplace=True)
            callsArray = pd.merge(callsArray, callsArray2, on='strike')
        callsArray.set_index('strike', inplace=True)
        callsArray = callsArray.fillna(0)
        ###########################
        print(callsArray)
        heat_map = sb.heatmap(callsArray, cmap="Blues", linewidths=0)
        plt.yticks(rotation=0)
        plt.xticks(rotation=50)
        plt.gca().invert_yaxis()
        plt.show()
        ############################
        self.threedeegraph(callsArray)


def heatCleaner(object):
    object = object.drop(columns=["contractSymbol", "lastTradeDate", "lastPrice", "change", "percentChange",
                                  "volume", "inTheMoney", "contractSize", "currency", "impliedVolatility", "ask", "bid"])
    object = object[["strike", "openInterest"]]
    return object


def cleaner(object):
    return object.drop(columns=["contractSymbol", "lastTradeDate", "lastPrice", "change", "percentChange", "impliedVolatility", "inTheMoney", "contractSize", "currency"])


def heatCleanerVOLUME(object):
    object = object.drop(columns=["contractSymbol", "lastTradeDate", "lastPrice", "change", "percentChange",
                                  "openInterest", "inTheMoney", "contractSize", "currency", "impliedVolatility", "ask", "bid"])
    object = object[["strike", "volume"]]
    return object
