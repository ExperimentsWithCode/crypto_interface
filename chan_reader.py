# source https://github.com/bibanon/BASC-py4chan/

import basc_py4chan
from collections import defaultdict
from crypto import Crypto
import os

class ChanReader():
    def __init__(self, _crypto, _board="biz"):
        self.crypto = _crypto
        self.board = basc_py4chan.Board(_board)
        self.all_thread_ids = self.board.get_all_thread_ids()
        self.counts = defaultdict(lambda: {'count': 0} )
        self.post_ids = defaultdict(lambda: False )
        self.options = {'a': {'display': 'Update Datastore', 'func': self.update},
                        'b': {'display': 'Display Counts', 'func': self.displayCounts},
                        }


    def update(self):
        self._printFormatter('title', 0, "Update Datastore")
        self._updateThreads()
        self._cycleThreads()
        print("\n\nDone Updating")
        print("!"*100+"\n")

    def displayCounts(self):
        self._printFormatter('subTitle', 0, "Display Counts")
        keys = self.counts.keys()
        keys.sort()
        for currency in keys:
            self._printFormatter('displayCounts', 1, currency, self.counts[currency]['count'])

    def _cycleThreads(self):
        count = 1
        self._printFormatter('subTitle', 1, "Dispaly Threads")
        for idx in self.all_thread_ids:
            thread = self.board.get_thread(idx)
            # os.system('clear')
            self._printFormatter('subTitle', 1, "Dispaly Threads")
            self._printFormatter('cycle', 1, 'Thread', count, self.all_thread_ids, thread.id)
            self._cycleReplies(thread)
            count += 1

    def _cycleReplies(self, thread):
        self._printFormatter('subTitle', 0, "Display Replies")
        count = 1
        for reply in thread.replies:
            # os.system('clear')
            self._printFormatter('cycle', 2, 'Reply', count, self.all_thread_ids, reply.post_id)
            count += 1
            if not self.post_ids[reply.post_id]:
                self.post_ids[reply.post_id] = True
                self._checkForNod(reply.text_comment)

    def _updateThreads(self):
        self.all_thread_ids = self.board.get_all_thread_ids()
        self.current_thread = 0


    def _printFormatter(self, _type, indent=0, header=None, x=None, y=None, z=None):
        if _type == "cycle":
            print("{0}{1}: {2} of {3} - {4}".format("\t" * indent, header, x, len(y), z))
        elif _type == "displayCounts":
            print("{0}{1}: {2} mentions".format("\t" * 2, header, x ))
        elif _type == "subTitle":
            print("{0}{1}".format("_"*100+"\n\t" * 1, "Display Counts"))
        elif _type == "title":
            print("{0}{1}".format("_"*100+"\n\t" * 0, header))
        else:
            print("failed to print")


    def _checkForNod(self, content):
        # Checks to see if any currency stored in crypto is mentioned.
        for currency in self.crypto.currencies.keys():
            if currency in content:
                self.counts[currency]['count'] += 1
            elif self.crypto.currencies[currency]['CurrencyLong'] in content:
                self.counts[currency]['count'] += 1





#
#
# b = basc_py4chan.Board('b')
# threads = b.get_threads()
# print("Got %i threads" % len(threads))
# first_thread = threads[0]
# print("First thread: %r" % first_thread)
# print("Replies: %r" % first_thread.replies)
# print("Updating first thread...")
# first_thread.update()
# print("First thread now: %r" % first_thread)
# for post in first_thread.replies:
#
# board = basc_py4chan.Board('v')
# all_thread_ids = board.get_all_thread_ids()
# first_thread_id = all_thread_ids[0]
# thread = board.get_thread(first_thread_id)
#     # thread information
#     print(thread)
#     print('Sticky?', thread.sticky)
#     print('Closed?', thread.closed)
#     # topic information
#     topic = thread.topic
#     print('Topic Repr', topic)
#     print('Postnumber', topic.post_number)
#     print('Timestamp',  topic.timestamp)
#     print('Datetime',   repr(topic.datetime))
#     print('Subject',    topic.subject)
#     print('Comment',    topic.text_comment)
#     print('Replies',    thread.replies)
#     # file information
#     for f in thread.file_objects():
#         print('Filename', f.filename)
#         print('  Filemd5hex', f.file_md5_hex)
#         print('  Fileurl', f.file_url)
#         print('  Thumbnailurl', f.thumbnail_url)
#         print()
