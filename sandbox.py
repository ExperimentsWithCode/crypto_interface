from reddit_reader import RedditReader
from crypto import Crypto
from pg import PostgresConnection
from chan_reader import ChanReader

subs = ['cryptocurrency']
c = Crypto()
pg = PostgresConnection()
chan = ChanReader(c, {'board': 'biz'}, pg)
chan.update()
r = RedditReader(c, {'subs': subs}, pg)
r.update()