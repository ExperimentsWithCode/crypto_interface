import json, requests

# API Docs
# https://coinmarketcap.com/api/
# https://bittrex.com/home/api
# https://docs.gdax.com/


HOLDINGS={
    'ETH-GNT': {'coins': 1.0},
    'ETH-OMG': {'coins': 2.0},
    'ETH-BAT': {'coins': 3.0},
    'ETH-LTC': {'coins': 4.0}
    }



class Crypto():
    def __init__(self):
        self.holdings = HOLDINGS
        self.holdingsKeys = self.holdings.keys()
        self.ethPrice = None
        self.currencies = {}   # [u'Notice', u'TxFee', u'CurrencyLong', u'CoinType', u'Currency', u'MinConfirmation', u'BaseAddress', u'IsActive']
        self.options = {'a': {'display': 'Update Local ETH Price', 'func': self._updateETHprice},
                        'b': {'display': 'Display Currency Info', 'func': self._displayCurrencies},
                        'c': {'display': 'Display Holdings Price Rates', 'func': self._displayHoldingsRate},
                        'd': {'display': 'Display Current Holdings Value', 'func': self._displayHoldingsValue},
                        'e': {'display': 'Get Currencies', 'func': self._getCurrencies}
                        }
        self._updateETHprice()
        self._getCurrencies()

    def _updateETHprice(self):
        # api call to pull ETH price from coinmarketcap which considers many exchange prices.
        ethereumInfo = requests.get('https://api.coinmarketcap.com/v1/ticker/ethereum/')
        # data is stored here after being converted from json to python dict
        #   Because the data is returned as an array of dicts of length 1
        #   I just indexed into the first result by default.
        data = json.loads(ethereumInfo.text)[0]
        # The price is stored to the class in a dict under the key price_usd as a string.
        #   Convert to Float cause more useful
        self.ethPrice = float(data['price_usd'])
        # Inform user of side effect
        self._printDivider()
        print ("Updated Eth Price to: {0}".format(self.ethPrice))
#
#
    def _displayCurrencies(self):
        self._printDivider()
        # Return data keys:
        #   [u'Notice', u'TxFee', u'CurrencyLong', u'CoinType', u'Currency', u'MinConfirmation', u'BaseAddress', u'IsActive']
        # Loop through resulting data
        print("Currency List")
        for d in self.currencies.keys():
            this_currency = self.currencies[d]
            print "{0} - {1} - {2}".format(this_currency['Currency'], this_currency['CurrencyLong'], this_currency['IsActive'])

    def _getCurrencies(self):
        self._printDivider()
        print("Loading Currencies...")
        # Return data keys:
        #   [u'Notice', u'TxFee', u'CurrencyLong', u'CoinType', u'Currency', u'MinConfirmation', u'BaseAddress', u'IsActive']
        # Get list of pairs
        #   Currently not doing anything with this info
        pairs = requests.get('https://bittrex.com/api/v1.1/public/getcurrencies')
        data = json.loads(pairs.text)
        # Loop through resulting data
        for d in data['result']:
            self.currencies[d['Currency']] = d

#
    def _displayHoldingsRate(self):
        self._printDivider()
        print("Current Holdings Rates")
        # [u'Ask', u'Bid', u'Last']
        for pair in self.holdingsKeys:
            count = 0
            while count == 0 or (ticker.status_code != 200 or count < 5):
                ticker = requests.get('https://bittrex.com/api/v1.1/public/getticker?market=' + pair)
                count += 1
            if count == 5:
                print("\t\tCould not gather data")
            data = json.loads(ticker.text)
            print("\tpair: {0}".format(pair))
            print("\t\tAsk: {0}".format(data['result']['Ask']))
            print("\t\tBid: {0}".format(data['result']['Bid']))
            print("\t\tLast: {0} \n\n".format(data['result']['Last']))



    def _displayHoldingsValue(self):
        self._printDivider()
        print("Current Holdings Value")
        totalVal= 0.0
        for pair in self.holdingsKeys:
            ticker = requests.get('https://bittrex.com/api/v1.1/public/getticker?market='+pair)
            data = json.loads(ticker.text)
            currentVal = data['result']['Last'] * self.ethPrice * self.holdings[pair]['coins']
            totalVal += currentVal
            print("\tPair: " + pair)
            print("\t\tValue: {0} \n\n".format(currentVal) )
        print("\tTotal Value: {0} \n\n".format(totalVal) )

    def _printDivider(self):
        print("_"*100)




# Below will run if called directly. i.e . $python <file.py>
# As opposed to importing this file from another function, it will not run.
# if __name__== "__main__":
#     c = Crypto()
