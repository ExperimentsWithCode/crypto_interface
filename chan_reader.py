# source https://github.com/bibanon/BASC-py4chan/

import basc_py4chan
from collections import defaultdict
from crypto import Crypto
import os
from operator import itemgetter
from scanner import Scanner

ACCEPTABLE_NEIGHBORS = [' ', '.', '/', '-', '!', ',', '?', '_']
class ChanReader():
    def __init__(self, _crypto, _board="biz"):
        self.crypto = _crypto
        self.board = basc_py4chan.Board(_board)
        self.all_thread_ids = self.board.get_all_thread_ids()
        self.counts = defaultdict(lambda: {'count': 0, 'comments': []} )
        self.post_ids = defaultdict(lambda: False )
        self.options = {'a': {'display': 'Update Datastore', 'func': self.update},
                        'b': {'display': 'Display Counts', 'func': self._displayCounts},
                        'c': {'display': 'Display Comments by Coin', 'func': self._displayComments},
                        }
        self.all_thread_ids = self.board.get_all_thread_ids()

    def update(self):
        self._print_formatter('title', 0, "Update Datastore")
        self._update_threads()
        self._cycle_threads()
        print("\n\nDone Updating")
        print("!"*100+"\n")

    def _displayCounts(self):
        self._printFormatter('subTitle', 0, "Display Counts")
        keys = self.counts.keys()
        keys.sort()
        for currency in keys:
            self._printFormatter('displayCounts', 1, currency, self.counts[currency]['count'])
            
    def _update_threads(self):
        self.all_thread_ids = self.board.get_all_thread_ids()
        self.current_thread = 0

    def _cycle_threads(self):
        count = 1
        self._print_formatter('subTitle', 1, "Display Threads")
        for idx in self.all_thread_ids:
            thread = self.board.get_thread(idx)
            # os.system('clear')
            self._print_formatter('subTitle', 1, "Display Threads")
            self._print_formatter('cycle', 1, 'Thread', count, len(self.all_thread_ids), thread.id)
            self._cycle_replies(thread)
            count += 1

    def _cycle_replies(self, thread):
        self._print_formatter('subTitle', 0, "Display Replies")
        count = 1
        for reply in thread.replies:
            # os.system('clear')
            self._print_formatter('cycle', 2, 'Reply', count, len(thread.replies), reply.post_id)
            count += 1
            if not self.post_ids[reply.post_id]:
                self.post_ids[reply.post_id] = True
                self._check_for_nod(reply.text_comment)

    # def _DisplayTopCounts(self, limit=None):
    #     self._printFormatter('subTitle', 0, "Get Top Counts")
    #     keys = self.counts.keys()
    #     keys.self.sort() #key=lambda x: x[1]
    #     # sorted(keys, key=itemgetter('count') #fix
    #     for currency in keys:
    #         self._printFormatter('displayCounts', 1, currency, self.counts[currency]['count'])

    def _display_comments(self):
        currency = raw_input("select a currency: ")
        self._printFormatter('subTitle', 0, "Get Comments on {0}".format(currency))
        selection = ''
        i = 0
        while selection != 'q' and i < len(self.counts[currency]['comments']):
            i0 = i
            while i <= i0 + 5 and i < len(self.counts[currency]['comments']):
                try:
                    print(" - " * 100)
                    self._printFormatter('displayCounts', 1, currency, self.counts[currency]['comments'][i])
                except Exception as e:
                    print('Failed to print comment')
                    print(e.message, e.args)
                i += 1
            selection = raw_input(': ')


    def _update_threads(self):
        self.all_thread_ids = self.board.get_all_thread_ids()
        self.current_thread = 0


    def _print_formatter(self, _type, indent=0, header=None, x=None, y=None, z=None):
        if _type == "cycle":
            print("{0}{1}: {2} of {3} - {4}".format("\t" * indent, header, x, len(y), z))
        elif _type == "displayCounts":
            print("{0}{1}: {2} mentions".format("\t" * 2, header, x ))
        elif _type == "subTitle":
            print("{0}{1}".format("_"*100+"\n\t" * 1, header))
        elif _type == "title":
            print("{0}{1}".format("_"*100+"\n\t" * 0, header))
        else:
            print("failed to print")


    def _check_for_nod(self, content):
        # Checks to see if any currency stored in crypto is mentioned.
        for currency in self.crypto.currencies.keys():
            content = content.lower()
            cur1 = currency.lower()
            cur2 = self.crypto.currencies[currency]['CurrencyLong'].lower()
            if cur1 in content:
                if self._checkIndividualWord(content, cur1):
                    self.counts[currency]['count'] += 1
                    self.counts[currency]['comments'].append(content)
            elif cur2  in content:
                if self._checkIndividualWord(content, cur2):
                    self.counts[currency]['count'] += 1
                    self.counts[currency]['comments'].append(content)

    def _check_individual_word(self, content, substring):
        # Checks if nod at cypto is isolated, or just a substring of a larger word.
        start = content.find(substring)
        end = start + len(substring)
        index = 0
        loops = 0
        while content.find(substring, index) >= 0 and end + 1 < len(content):
            if start == 0:
                if content[end + 1] in ACCEPTABLE_NEIGHBORS:
                    return True
            elif end == len(content):
                if content[start - 1] in ACCEPTABLE_NEIGHBORS:
                    return True
            else:
                if (content[start - 1] in ACCEPTABLE_NEIGHBORS and
                    content[end + 1] in ACCEPTABLE_NEIGHBORS):
                    return True
            index = end
            start = content.find(substring, end)
            end = start + len(substring)
        return False

    def _get_top_counts(self, limit=None):
        self._print_formatter('subTitle', 0, "Get Top Counts")
        keys = self.counts.keys()
        keys.self.sort() #key=lambda x: x[1]
        # sorted(keys, key=itemgetter('count') #fix
        for currency in keys:
            self._print_formatter('displayCounts', 1, currency, self.counts[currency]['count'])
