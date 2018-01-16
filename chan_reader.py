# source https://github.com/bibanon/BASC-py4chan/

import basc_py4chan
from collections import defaultdict
from crypto import Crypto
import os
from operator import itemgetter
from scanner import Scanner

ACCEPTABLE_NEIGHBORS = [' ', '.', '/', '-', '!', ',', '?', '_']

class ChanReader(Scanner):
    def __init__(self, _crypto, config, pg):
        Scanner.__init__(self, _crypto, pg)
        self.board = basc_py4chan.Board(config['board'])
        self.all_thread_ids = self.board.get_all_thread_ids()

    def update(self):
        self._print_formatter('title', 0, "Update Datastore")
        self._update_threads()
        self._cycle_threads()
        self.save_mentions()
        print("\n\nDone Updating")
        print("!"*100+"\n")

    def _update_threads(self):
        self.all_thread_ids = self.board.get_all_thread_ids()
        self.current_thread = 0

    def display_counts(self):
        self._print_formatter('subTitle', 0, "Display Counts")
        keys = self.counts.keys()
        keys.sort()
        for currency in keys:
            self._print_formatter('displayCounts', 1, currency, self.counts[currency]['count'])

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
        # self._print_formatter('subTitle', 0, "Display Replies")
        count = 1
        for reply in thread.replies:
            # os.system('clear')
            # self._print_formatter('cycle', 2, 'Reply', count, len(thread.replies), reply.post_id)
            count += 1
            if not self.post_ids[reply.post_id]:
                self.post_ids[reply.post_id] = True
                self._check_for_nod(reply.text_comment, reply.post_id, None, None)

    def _get_top_counts(self, limit=None):
        self._print_formatter('subTitle', 0, "Get Top Counts")
        keys = self.counts.keys()
        keys.self.sort() #key=lambda x: x[1]
        # sorted(keys, key=itemgetter('count') #fix
        for currency in keys:
            self._print_formatter('displayCounts', 1, currency, self.counts[currency]['count'])
