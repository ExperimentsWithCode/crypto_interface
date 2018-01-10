from reddit_reader import RedditReader
from crypto import Crypto

subs = ['cryptocurrency']
c = Crypto()
r = RedditReader(c, subs)
r.update()