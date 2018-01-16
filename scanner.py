import os
from collections import defaultdict

ACCEPTABLE_NEIGHBORS = [' ', '.', '/', '-', '!', ',', '?', '_']


class Scanner():
    def __init__(self, _crypto, pg):
        self.pg = pg
        self.crypto = _crypto
        self.counts = defaultdict(lambda: {'count': 0, 'comments': []})
        self.mentions = defaultdict(
            lambda: {
                'thread_id': None,
                'parent_id': None,
                'body': '',
                'is_thread_title': False,
                'is_thread_body': False,
                'is_comment_body': False,
                'coins_mentioned': defaultdict(lambda: 0)}
        )
        self.post_ids = defaultdict(lambda: False )
        self.options = {'a': {'display': 'Update Datastore', 'func': self.update},
                        'b': {'display': 'Display Counts', 'func': self.display_counts},
                        'c': {'display': 'Get Comments by Coin', 'func': self.get_comments},
                        }

    def save_mentions(self):
        mention_body_ids = self.mentions.keys()
        comments = []
        mentions = []
        for id in mention_body_ids:
            mention = self.mentions[id]
            comment_record = {
                'mention_body_id': id,
                'thread_id': mention['thread_id'],
                'parent_id': mention['parent_id'],
                'body': mention['body'].replace("'", "")
            }
            comments.append(comment_record)
            num_mentions_by_coin = mention['coins_mentioned']
            coins = num_mentions_by_coin.keys()
            for coin in coins:
                mention_record = {
                    'is_thread_title': mention['is_thread_title'],
                    'is_thread_body': mention['is_thread_body'],
                    'is_comment_body': mention['is_comment_body'],
                    'mention_body_id': id,
                    'coin_id': coin,
                    'num_mentions': num_mentions_by_coin[coin]
                }
                mentions.append(mention_record)
        self.pg.save_mentions(mentions)
        self.pg.save_mention_bodies(comments)

    def update(self):
        self._print_formatter('title', 0, "Update Datastore")
        self._update_threads()
        self._cycle_threads()
        self.save_mentions()
        print("\n\nDone Updating")
        print("!"*100+"\n")

    def display_counts(self):
        self._print_formatter('subTitle', 0, "Display Counts")
        keys = self.counts.keys()
        keys.sort()
        for symbol in keys:
            self._print_formatter('displayCounts', 1, symbol, self.counts[symbol]['total_count'])

    def get_comments(self):
        coin = raw_input("select a coin: ")
        self._print_formatter('subTitle', 0, "Get Comments on {0}".format(coin))
        selection = ''
        i = 0
        while selection != 'q' and i < len(self.counts[coin]['comments']):
            i0 = i
            while i <= i0 + 5 and i < len(self.counts[coin]['comments']):
                try:
                    print(" - " * 100)
                    self._print_formatter('displayCounts', 1, coin, self.counts[coin]['comments'][i])
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

    def _check_for_nod(self, content, comment_id, thread_id, parent_id):
        # Checks to see if any currency stored in crypto is mentioned.
        for currency in self.crypto.currencies.keys():
            content = content.lower()
            cur1 = currency.lower()
            cur2 = self.crypto.currencies[currency]['CurrencyLong'].lower()
            if cur1 in content and self._check_for_word(content, cur1):
                self._record_nod(comment_id, content, thread_id, cur1, parent_id)
            elif cur2 in content and self._check_for_word(content, cur2):
                self._record_nod(comment_id, content, thread_id, cur1, parent_id)

    def _record_nod(self, mention_id, content, thread_id, coin, parent_id):
        self.mentions[mention_id]['thread_id'] = thread_id
        self.mentions[mention_id]['body'] = content
        self.mentions[mention_id]['coins_mentioned'][coin] += 1
        self.mentions[mention_id]['is_comment_body'] = True
        self.mentions[mention_id]['mention_body_id'] = mention_id
        self.mentions[mention_id]['parent_id'] = parent_id

        self.counts[coin]['count'] += 1
        self.counts[coin]['comments'].append(content)

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
