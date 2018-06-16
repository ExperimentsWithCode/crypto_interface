from bot.crypto import Crypto
from bot.reader.chan_reader import ChanReader
from bot.reader.reddit_reader import RedditReader
from db.pg import PostgresConnection
from utils.colorize import colorize
import json
import requests
from bot.coin import Coin
import locale
import pandas as pd
from utils.utils import is_number

locale.setlocale(locale.LC_ALL, 'en_US')

REDDIT_SUBS = ['cryptocurrency']
LIMIT = 3000
HOLDINGS={
    'ETH-GNT': {'coins': 1.0},
    'ETH-OMG': {'coins': 2.0},
    'ETH-BAT': {'coins': 3.0},
    'ETH-LTC': {'coins': 4.0}
    }


class Main():
    def __init__(self, pg=None):
        if pg is None:
            pg = PostgresConnection()
        self.crypto = Crypto(pg)
        self.chan_reader = ChanReader(self.crypto, {'board': 'biz'}, pg)
        self.reddit_reader = RedditReader(self.crypto, {'subs': REDDIT_SUBS}, pg)
        self.crypto_options = {
            'a': {'display': 'Update Local ETH Price', 'func': self._update_eth_price},
            'b': {'display': 'Display Coins', 'func': self.print_filtered_coins},
            'd': {'display': 'Display Current Holdings Value', 'func': self._display_holdings_value},
            'e': {'display': 'Get Currencies', 'func': self._get_coins},
            'f': {'display': 'Set Filters', 'func': self.set_filters},
            'g': {'display': 'Sort', 'func': self.set_sorting}
        }
        self.options = {
            'a': {'display': 'Crypto Interface', 'func': self.crypto_options},
            'b': {'display': '4Chan Interface', 'func': self.chan_reader.options},
            'r': {'display': 'Reddit Interface', 'func': self.reddit_reader.options}
        }
        self.holdings = HOLDINGS
        self.holdings_keys = self.holdings.keys()
        self.eth_price = None
        self.coins = None
        self.filtered_coins = None
        self._update_eth_price()
        self._get_coins()
        self.pg = pg
        self.filters = {
            'market_cap_usd': {'max': 999999999999999, 'min': 0},
            'price_btc': {'max': 999999999999999, 'min': 0},
            'price_usd': {'max': 999999999999999, 'min': 0}
        }

    def get_coins_by_market_cap(self, min_mkt_cap, max_mkt_cap):
        return self.pg.get_coins_by_market_cap(min_mkt_cap, max_mkt_cap)

    def _update_eth_price(self):
        ethereum_info = requests.get('https://api.coinmarketcap.com/v1/ticker/ethereum/')
        if ethereum_info.status_code == 429:
            print("** ** Too many requests ** **")
        else:
            data = json.loads(ethereum_info.text)[0]
            self.eth_price = float(data['price_usd'])
            self._print_divider()
            print(colorize.OKGREEN + "Updated Eth Price to: {0}".format(self.eth_price) + colorize.ENDC)

    def _display_coins(self):
        self._print_divider()
        # Return data keys:
        #   [u'Notice', u'TxFee', u'CurrencyLong', u'CoinType', u'Currency', u'MinConfirmation', u'BaseAddress', u'IsActive']
        print("Currency List")
        for symbol in self.coins.keys():
            this_coin = self.coins[symbol]
            print("{0} - {1} - {2}".format(symbol, this_coin.name, this_coin.price_usd))

    def _get_coins(self):
        self._print_divider()
        print("Loading Currencies...")
        # Return data keys:
        #   [u'Notice', u'TxFee', u'CurrencyLong', u'CoinType', u'Currency', u'MinConfirmation', u'BaseAddress', u'IsActive']
        start = 0
        limit = LIMIT
        raw_coins = requests.get(
            'https://api.coinmarketcap.com/v1/ticker/?start=' + str(start) + '&limit=' + str(limit))
        if raw_coins.status_code == 429:
            print("** ** Too many requests ** **")
        else:
            coins = json.loads(raw_coins.text)
            self.coins = pd.DataFrame(coins)
            self.coins = self.coins.convert_objects(convert_numeric=True)

    def set_filters(self):
        self.get_set_mkt_cap_range()
        self.apply_filters()

    def set_sorting(self):
        param = self.get_sort_parameter()
        dir = self.get_sort_direction()
        self.filtered_coins = self.filtered_coins.sort_values(by=[param], ascending=[dir])

    def get_sort_direction(self):
        print(colorize.OKBLUE + "\nSort `up` or `down`?" + colorize.ENDC)
        up_down = raw_input()
        if up_down not in ['up', 'down', 'u', 'd']:
            print(colorize.FAIL + "\nInvalid direction, please try again\n" + colorize.ENDC)
            self.get_sort_direction()
        else:
            if up_down == 'u' or up_down == 'up':
                return 1
            else:
                return 0

    def get_sort_parameter(self):
        sort_string = colorize.OKGREEN + ""
        for f_name, f_values in self.filters.items():
            sort_string += "\t\n" + f_name
        print(colorize.OKBLUE + "\nPick a parameter to sort by:" + sort_string + colorize.ENDC)
        parameter = raw_input()
        if parameter not in self.filters:
            print(colorize.FAIL + "\nThat parameter doesnt exist\n" + colorize.ENDC)
            self.get_sort_parameter()
        else:
            return parameter

    def get_set_mkt_cap_range(self):
        try:
            print(colorize.OKBLUE + "\nInput minimum market cap:" + colorize.ENDC)
            min_mkt_cap = raw_input()
            print(colorize.OKBLUE + "\nInput maximum market cap:" + colorize.ENDC)
            max_mkt_cap = raw_input()
            if is_number(min_mkt_cap) and is_number(max_mkt_cap):
                self._set_mkt_cap_range(min_mkt_cap, max_mkt_cap)
            else:
                print(colorize.FAIL + "\nPlease enter a valid number\n")
                self.get_set_mkt_cap_range()
        except ValueError:
            print(colorize.FAIL + "\nPlease enter a valid number\n")
            self.get_set_mkt_cap_range()

    def _set_mkt_cap_range(self, min_mkt_cap, max_mkt_cap):
        self.filters['market_cap_usd'] = {'max': float(max_mkt_cap), 'min': float(min_mkt_cap)}

    def apply_filters(self):
        self.filtered_coins = self.coins.copy()
        for f_name, f_values in self.filters.items():
            self.filtered_coins = self.filtered_coins[self.filtered_coins[f_name] > f_values['min']]
            self.filtered_coins = self.filtered_coins[self.filtered_coins[f_name] < f_values['max']]

    def print_filtered_coins(self):

        self.print_coins(self.filtered_coins)

    def print_all_coins(self):
        self.print_coins(self.coins)

    @staticmethod
    def print_coins(coins):
        # header
        print(
            "{0:{sym_width}}{1:{name_width}}::\t{2:{data_width}}{3:{data_width}}{4:{data_width}}{5:{data_width}}\t".format(
                'Symbol',
                'Name',
                'Price BTC',
                'Price USD',
                'MktCap USD',
                'Supply',
                sym_width=10,
                name_width=28,
                data_width=20
            ))

        for idx, coin in coins.iterrows():
            # watch out for None's
            mkt_cap_usd = coin['market_cap_usd']
            if mkt_cap_usd is None:
                mkt_cap_usd = 0
            available_supply = coin['available_supply']
            if available_supply is None:
                available_supply = 0

            print(
                "{0:{sym_width}}{1:{name_width}}\t::\t{2:{data_width}}{3:{data_width}}{4:{data_width}}{5:{data_width}}\n".format(
                    coin['symbol'],
                    coin['name'],
                    str(coin['price_btc']),
                    str(coin['price_usd']),
                    locale.format("%d", float(mkt_cap_usd), grouping=True),
                    locale.format("%d", float(available_supply), grouping=True),
                    sym_width=10,
                    name_width=28,
                    data_width=20
                ))

    def _display_holdings_value(self):
        self._print_divider()
        print("Current Holdings Value")
        total_val = 0.0
        for pair in self.holdings_keys:
            ticker = requests.get('https://bittrex.com/api/v1.1/public/getticker?market=' + pair)
            data = json.loads(ticker.text)
            current_val = data['result']['Last'] * self.eth_price * self.holdings[pair]['coins']
            total_val += current_val
            print("\tPair: " + pair)
            print("\t\tValue: {0} \n\n".format(current_val))
        print("\tTotal Value: {0} \n\n".format(total_val))

    def _print_divider(self):
        print("_" * 100)

    def run(self):
        # This function allows users to interact with the class object
        options = self.options
        selection = 'main'
        # This allows users to loop through performing different options until exiting
        while selection != 'exit':
            old_selection = selection
            self._print_divider()
            keys = options.keys()
            keys.sort()
            print(colorize.HEADER + "\n\n\nSelect what you would like to do" + colorize.ENDC)
            for option in keys:
                print(colorize.OKBLUE + "\tEnter `{0}` to `{1}`".format(option, options[option]['display']) + colorize.ENDC)
            if old_selection != 'main':
                print(colorize.OKBLUE + "\tEnter `{0}` to `{1}`".format('main', 'return to main') + colorize.ENDC)
            print(colorize.WARNING + "\tEnter `{0}` to `{1}`".format('exit', 'exit') + colorize.ENDC)
            selection = raw_input('Select: ')

            try:
                if selection == 'main':
                    options = self.options
                elif old_selection == 'main':
                    options = options[selection]['func']
                else:
                    if selection in options.keys():
                        options[selection]['func']()
            except Exception as e:
                print(e)

    @staticmethod
    def _print_divider():
        print("_"*100)


if __name__== "__main__":
    m = Main()
    m.run()
