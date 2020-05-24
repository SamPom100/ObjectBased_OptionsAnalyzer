import yfinance as yf
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
        print("Ticker is: "+self.ticker)

    def getDates(self):
        print(self.DateArray)

    def getDateChoice(self):
        print(self.DateChoice)

    def getOptionChain(self):
        print(self.optChain)

    def pickStrike(self):
        tempTuple = ("Pick a Strike Price",)
        pickStrikePrice(tempTuple + self.DateArray)
        self.DateChoice = returnChoice()
        self.optChain = self.yfObject.option_chain(self.DateChoice)

    def pickTicker(self):
        self.ticker = onButton()
        self.setUpDefaults()

    def setUpDefaults(self):
        self.yfObject = yf.Ticker(self.ticker)
        self.DateArray = yf.Ticker(self.ticker).options
        self.DateChoice = self.DateArray[1]
        self.optChain = self.yfObject.option_chain(self.DateChoice)
