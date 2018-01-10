import os
from collections import defaultdict

ACCEPTABLE_NEIGHBORS = [' ', '.', '/', '-', '!', ',', '?', '_']


class Scanner():
    def __init__(self, _crypto):
        self.crypto = _crypto
        self.counts = defaultdict(lambda: {'count': 0, 'comments': []} )
        self.post_ids = defaultdict(lambda: False )
        self.options = {'a': {'display': 'Update Datastore', 'func': self.update},
                        'b': {'display': 'Display Counts', 'func': self.display_counts},
                        'c': {'display': 'Get Comments by Coin', 'func': self.get_comments},
                        }

    def update(self):
        self._print_formatter('title', 0, "Update Datastore")
        self._update_threads()
        self._cycle_threads()
        print("\n\nDone Updating")
        print("!"*100+"\n")

    def display_counts(self):
        self._print_formatter('subTitle', 0, "Display Counts")
        keys = self.counts.keys()
        keys.sort()
        for currency in keys:
            self._print_formatter('displayCounts', 1, currency, self.counts[currency]['count'])

    def get_comments(self):
        currency = raw_input("select a currency: ")
        self._print_formatter('subTitle', 0, "Get Comments on {0}".format(currency))
        selection = ''
        i = 0
        while selection != 'q' and i < len(self.counts[currency]['comments']):
            i0 = i
            while i <= i0 + 5 and i < len(self.counts[currency]['comments']):
                try:
                    print(" - " * 100)
                    self._print_formatter('displayCounts', 1, currency, self.counts[currency]['comments'][i])
                except Exception as e:
                    print('Failed to print comment')
                    print(e.message, e.args)
                i += 1
            selection = raw_input(': ')

    def _print_formatter(self, _type, indent=0, header=None, x=None, y=None, z=None):
        if _type == "cycle":
            print("{0}{1}: {2} of {3} - {4}".format("\t" * indent, header, x, y, z))
        elif _type == "displayCounts":
            print("{0}{1}: {2} mentions".format("\t" * 2, header, x ))
        elif _type == "subTitle":
            print("{0}{1}".format("_"*100+"\n\t" * 1, header))
        elif _type == "title":
            print("{0}{1}".format("_"*100+"\n\t" * 0, header))
        else:
            print("failed to print")

    def _update_threads(self):
        raise Exception('UPDATE_THREADS function should be overwritten')

    def _cycle_threads(self):
        raise Exception('CYCLE_THREADS function should be overwritten')

    def _check_for_nod(self, content):
        # Checks to see if any currency stored in crypto is mentioned.
        for currency in self.crypto.currencies.keys():
            content = content.lower()
            cur1 = currency.lower()
            cur2 = self.crypto.currencies[currency]['CurrencyLong'].lower()
            if cur1 in content:
                if self._check_for_word(content, cur1):
                    self.counts[currency]['count'] += 1
                    self.counts[currency]['comments'].append(content)
            elif cur2  in content:
                if self._check_for_word(content, cur2):
                    self.counts[currency]['count'] += 1
                    self.counts[currency]['comments'].append(content)

    @staticmethod
    def _check_for_word(content, substring):
        # Checks if nod at cypto is isolated, or just a substring of a larger word.
        start = content.find(substring)
        end = start + len(substring)
        index = 0
        while content.find(substring, index) >= 0 and end + 1 < len(content):
            if start == 0:
                if content[end + 1] in ACCEPTABLE_NEIGHBORS:
                    return True
            elif end == len(content):
                if content[start - 1] in ACCEPTABLE_NEIGHBORS:
                    return True
            else:
                if content[start - 1] in ACCEPTABLE_NEIGHBORS and content[end + 1] in ACCEPTABLE_NEIGHBORS:
                    return True
            index = end
            start = content.find(substring, end)
            end = start + len(substring)
        return False
