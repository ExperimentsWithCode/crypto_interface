import praw
from praw.models import MoreComments
import os
from collections import defaultdict
from scanner import Scanner

ACCEPTABLE_NEIGHBORS = [' ', '.', '/', '-', '!', ',', '?', '_']


class RedditReader(Scanner):
    def __init__(self, _crypto, config):
        Scanner.__init__(self, _crypto)
        self.reddit = praw.Reddit(
            client_id=os.getenv('REDDIT_API', 'ZLQ1i92zSxaWSQ'),
            client_secret=os.getenv('REDDIT_SECRET', 'Da5pUrfOmsnxbhZ8gA_iKFNSB8o'),
            user_agent='python:crypto-sleuth:0.0.1 (by /u/rlawford)'
        )
        self.subs = config['subs']
        self.sub = self.reddit.subreddit('+'.join(self.subs))

    def _update_threads(self):
        self.submissions = self.sub.rising()
        self.current_thread = 0

    def _cycle_threads(self):
        count = 1
        self._print_formatter('subTitle', 1, "Display Threads")
        for submission in self.submissions:
            self.get_submissions()
            self._print_formatter('subTitle', 1, "Display Threads")
            self._print_formatter('cycle', 1, 'Thread', count, submission.num_comments)
            self._cycle_replies(submission)
            count += 1

    def _cycle_replies(self, thread):
        # self._print_formatter('subTitle', 0, "Display Replies")
        count = 1
        thread.comments.replace_more(limit=None)
        for comment in thread.comments.list():
            self._check_for_nod(comment.body)
            # self._print_formatter('cycle', 2, 'Reply', count)
            count += 1
            self._check_for_nod(comment.body)

    def get_submissions(self):
        for submission in self.submissions:
            submission.comments.replace_more(limit=None)
            for comment in submission.comments.list():
                self._check_for_nod(comment.body)
