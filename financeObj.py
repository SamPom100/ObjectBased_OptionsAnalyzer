import yfinance as yf
import easygui
import matplotlib.pyplot as plt
from pick import pickStrikePrice, onButton, returnChoice


class financeObj:

    # default ticker is AMD
    ticker = None
    yfObject = None
    DateArray = None
    DateChoice = None
    optChain = None

    # parameterized constructor
    def __init__(self, tick="AMD"):
        self.ticker = tick
        self.setUpDefaults()

    def getTicker(self):
        return self.ticker

    def getDateArray(self):
        return self.DateArray

    def getDateChoice(self):
        return self.DateChoice

    def getOptionChain(self):
        return self.optChain

    def getYFObject(self):
        return self.yfObject

    def pickStrike(self):
        tempTuple = ("Pick a Strike Price",)
        pickStrikePrice(tempTuple + self.DateArray)
        self.DateChoice = returnChoice()
        self.optChain = self.yfObject.option_chain(self.DateChoice)

    def setTicker(self, tick):
        self.ticker = tick
        self.setUpDefaults

    def pickTicker(self):
        #self.ticker = onButton()
        self.ticker = easygui.enterbox("Pick a Stock Ticker")
        self.setUpDefaults()

    def setUpDefaults(self):
        self.yfObject = yf.Ticker(self.ticker)
        self.DateArray = yf.Ticker(self.ticker).options
        self.DateChoice = self.DateArray[1]
        # self.addSpaceToArray()
        self.optChain = self.yfObject.option_chain(self.DateChoice)
