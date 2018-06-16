import praw

from bot.reader.reader_bass import Reader
from config import REDDIT_SECRET, REDDIT_API

ACCEPTABLE_NEIGHBORS = [' ', '.', '/', '-', '!', ',', '?', '_']


class RedditReader(Reader):
    def __init__(self, _crypto, config, pg):
        self.name = "Reddit"
        Reader.__init__(self, _crypto, pg)
        self.reddit = praw.Reddit(
            client_id=REDDIT_API,
            client_secret=REDDIT_SECRET,
            user_agent='python:crypto-sleuth:0.0.1 (by /u/rlawford)'
        )
        self.subs = config['subs']
        self.sub = self.reddit.subreddit('+'.join(self.subs))
        self.threads = None

    def _update_threads(self):
        self.threads = self.sub.top()
        self.current_thread = 0

    def _cycle_threads(self):
        count = 1
        self._print_formatter('subTitle', 1, "Display Threads")
        for thread in self.threads:
            self._print_formatter('subTitle', 1, "Display Threads")
            self._print_formatter('cycle', 1, 'Thread', count, "-('<')-", thread.num_comments)
            self._cycle_replies(thread)
            count += 1

    def _cycle_replies(self, thread):
        # self._print_formatter('subTitle', 0, "Display Replies")
        count = 1
        thread.comments.replace_more(limit=None)
        for comment in thread.comments.list():
            self.all_thread_text += comment.body.encode('utf-8') + " "
            self._check_for_nod(comment.body, comment.id, thread.id, comment.parent_id.split('_')[1])
            # self._print_formatter('cycle', 2, 'Reply', count)
            count += 1
