from bot.crypto import Crypto
from bot.reader.reddit_reader import RedditReader
from bot.reader.chan_reader import ChanReader
from db.pg import PostgresConnection
from main import Main

db = PostgresConnection()
subs = ['cryptocurrency']
c = Crypto(db)
c._get_coins()
chan = ChanReader(c, {'board': 'biz'}, db)
chan.update()
# r = RedditReader(c, {'subs': subs}, db)
# r.update()


# m = Main()
# m._get_coins()
# m.set_filters()
# m.print_filtered_coins()
