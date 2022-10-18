import yfinance as yf

###########################################
############       Stonks      ############
###########################################

# Get info about a ticket, this is terrible because terrible.
def getInfo(ticker):
    try:
        info = yf.Ticker(ticker).info
        try:
            name = info['shortName']  # 'GameStop Corporation'
        except:
            response="I can't find that ticker."
            return response
        try:
            info0 = "Company Name:  " + str(name)
        except:
            info0 = "Company Name:  " + "Error"
        try:
            info1 = "\nTicker:  " + str(ticker)
        except:
            info1 = "\nTicker:  " + "Error"
        try:
            info2 = "\nProfit Margins:  " + str(info['profitMargins'])
        except:
            info2 = "\nProfit Margins:  " + "Error"
        try:
            info3 = "\nBeta:  " + str(info['beta'])
        except:
            info3 = "\nBeta:  " + "Error"
        try:
            info4 = "\n\nCurrent value:  " + str(checkStonks(ticker))
        except:
            info4 = "\n\nCurrent value:  " + "Error"
        try:
            info5 = "\n\nLast Close:  $" + str(info['previousClose'])
        except:
            info5 = "\n\nLast Close:  $" + "Error"
        try:
            info6 = "\nOpened At:  $" + str(info['open'])
        except:
            info6 = "\nOpened At:  $" + "Error"
        try:
            info7 = "\nDay's Low:  $" + str(info['dayLow'])
        except:
            info7 = "\nDay's Low:  $" + "Error"
        try:
            info8 = "\nDay's High:  $" + str(info['dayHigh'])
        except:
            info8 = "\nDay's High:  $" + "Error"
        try:
            info9 = "\n\nTotal Share Count:  " + str("{:,}".format(info['sharesOutstanding']))
        except:
            info9 = "\n\nTotal Share Count:  " + "Error"
        try:
            info10 = "\nShares Short Last Month:  " + str("{:,}".format(info['sharesShortPriorMonth']))
        except:
            info10 = "\nShares Short Last Month:  " + "Error"
        try:
            info11 = "\nShares Short Today:  " + str("{:,}".format(info['sharesShort']))
        except:
            info11 = "\nShares Short Today:  " + "Error"
        try:
            info12 = "\nShort Percent:  " + str(round((info['sharesPercentSharesOut']) * 100, 4)) + "%"
        except:
            info12 = "\nShort Percent:  " + "Error"
        try:
            info13 = "\n\nAverage Volume (Year):  " + str("{:,}".format(info['averageVolume']))
        except:
            info13 = "\n\nAverage Volume (Year):  " + "Error"
        try:
            info14 = "\nDaily Volume:  " + str("{:,}".format(info['volume']))
        except:
            info14 = "\nDaily Volume:  " + "Error"
        response = info0 + info1 + info2 + info3 + info4 + info5 + info6 + info7 + info8 + info9 + info10 + info11 + info12 + info13 + info14
        return response
    except Exception as e:
        return("'Grats.  You broke it.  Here's the error.\n" + str(e))

# Check a specific ticker
def checkStonks(symbol):
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period='1d')
        try:
            data = round(data['Close'][0], 2)
            data = "{:,}".format(data)
            data = "$" + data
        except:
            data = "That's an error.  Might be delisted / alt exchange."
    except:
        data = "I can't find that ticker..."
    return data