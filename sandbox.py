from crypto import Crypto
from pg import PostgresConnection
from reader.chan_reader import ChanReader
from reader.reddit_reader import RedditReader

db = PostgresConnection()
subs = ['cryptocurrency']
c = Crypto(db)
pg = PostgresConnection()
# chan = ChanReader(c, {'board': 'biz'}, pg)
# chan.update()
r = RedditReader(c, {'subs': subs}, pg)
r.update()
