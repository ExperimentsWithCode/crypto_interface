from reddit_reader import RedditReader
from crypto import Crypto
from pg import PostgresConnection

subs = ['cryptocurrency']
c = Crypto()
pg = PostgresConnection()
r = RedditReader(c, {'subs': subs}, pg)
r.update()