from crypto import Crypto
from chan_reader import ChanReader
from reddit_reader import RedditReader
from pg import PostgresConnection


REDDIT_SUBS = ['cryptocurrency']

class Main():
    def __init__(self, pg=None):
        if pg == None:
            pg = PostgresConnection()
        self.crypto = Crypto()
        self.chan_reader = ChanReader(self.crypto, {'board': 'biz'}, pg)
        self.reddit_reader = RedditReader(self.crypto, {'subs': REDDIT_SUBS}, pg)
        self.options = {'a': {'display': 'Crypto Interface', 'func': self.crypto.options},
                        'b': {'display': '4Chan Interface', 'func': self.chan_reader.options},
                        'r': {'display': 'Reddit Interface', 'func': self.reddit_reader.options}
                        }

    def run(self):
        # This function allows users to interact with the class object
        options = self.options
        selection = 'main'
        # This allows users to loop through performing different options until exiting
        while selection != 'exit':
            old_selection = selection
            self._printDivider()
            keys = options.keys()
            keys.sort()
            print("\n\n\nSelect what you would like to do")
            for option in keys:
                print("\tEnter `{0}` to `{1}`".format(option, options[option]['display']))
            if old_selection != 'main':
                print("\tEnter `{0}` to `{1}`".format('main', 'return to main'))
            print("\tEnter `{0}` to `{1}`".format('exit', 'exit'))
            selection = raw_input('Select: ')

            if selection == 'main':
                options = self.options
            elif old_selection == 'main':
                options = options[selection]['func']
            else:
                if selection in options.keys():
                    # This will run the function
                    options[selection]['func']()
                else:
                    print("Option not available")

    def _printDivider(self):
        print("_"*100)


if __name__== "__main__":
    m = Main()
    m.run()
