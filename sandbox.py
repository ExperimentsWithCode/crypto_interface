from bot.crypto import Crypto
from bot.reader.reddit_reader import RedditReader
from db.pg import PostgresConnection
from main import Main

# db = PostgresConnection()
# subs = ['cryptocurrency']
# c = Crypto(db)
# c._get_coins()
# # chan = ChanReader(c, {'board': 'biz'}, pg)
# # chan.update()
# r = RedditReader(c, {'subs': subs}, db)
# r.update()


m = Main()
m._get_coins()
m.set_filters()
m.print_filtered_coins()
