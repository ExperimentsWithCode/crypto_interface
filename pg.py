import datetime
from time import mktime

import pandas as pd
import psycopg2
from psycopg2.extensions import AsIs
import os
from logger import Logger

log = Logger('pg connection')


class PostgresConnection:
    def __init__(self):
        self.conn = None
        self.cur = None
        self.run_type = os.getenv('RUN_TYPE', 'BACKTEST')
        self.table_names = {
            'save_mentions': 'coin_mentions',
            'save_mention_bodies': 'mention_bodies',
            'coins': 'coins'
        }

    def table_name(self, table_type):
        return self.table_names[table_type]

    def _exec_query(self, query, params):
        ###
        # EXECUTES A QUERY ON THE DATABASE, RETURNS NO DATA
        ###
        self.conn = psycopg2.connect("dbname=crypto-community-explorer user=patrickmckelvy")
        self.cur = self.conn.cursor()
        try:
            self.cur.execute(query, params)
        except Exception as e:
            log.error('*** POSTGRES ERROR ***')
            log.error(e)

        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def _fetch_query(self, query, params):
        ###
        # EXECUTES A FETCHING QUERY ON THE DATABASE, RETURNS A DATAFRAME
        ###
        self.conn = psycopg2.connect("dbname=cryptobot user=patrickmckelvy")
        self.cur = self.conn.cursor()
        result = None
        try:
            self.cur.execute(query, params)
            column_names = [desc[0] for desc in self.cur.description]
            result = pd.DataFrame(self.cur.fetchall(), columns=column_names)
        except Exception as e:
            log.error('*** POSTGRES ERROR ***')
            log.error(e)

        self.conn.commit()
        self.cur.close()
        self.conn.close()
        return result

    def save_mentions(self, mentions):
        fmt_str = "('{coin_id}','{mention_body_id}',{is_thread_title},{is_thread_body},'{is_comment_body}',{num_mentions})"
        columns = "coin_id, mention_body_id, is_thread_title, is_thread_body, is_comment_body, num_mentions"
        values = AsIs(','.join(fmt_str.format(**mention) for mention in mentions))
        params = {
            "columns": AsIs(columns),
            "values": values
        }
        query = """ INSERT INTO """ + self.table_name('save_mentions') + """ (%(columns)s) VALUES %(values)s; """
        self._exec_query(query, params)
        return values

    def save_mention_bodies(self, mention_bodies):
        fmt_str = "('{thread_id}','{mention_body_id}','{parent_id}','{body}')"
        columns = "thread_id, mention_body_id, parent_id, body"
        values = AsIs(','.join(fmt_str.format(**body) for body in mention_bodies))
        params = {
            "columns": AsIs(columns),
            "values": values
        }
        query = """ INSERT INTO """ + self.table_name('save_mention_bodies') + """ (%(columns)s) VALUES %(values)s; """
        self._exec_query(query, params)
        return values

    def save_coins(self, coin_data):
        fmt_str = """(
            '{Currency}',
            '{CurrencyLong}',
            {price_btc},
            {price_eth},
            {price_usd},
            {mkt_cap},
            '{Notice}',
            {TxFee},
            {CoinType},
            {MinConfirmation},
            {BaseAddress},
            {IsActive}
        )"""
        columns = """
            Currency,
            CurrencyLong,
            price_btc,
            price_eth,
            price_usd,
            mkt_cap,
            Notice,
            CoinType,
            MinConfirmation,
            BaseAddress,
            IsActive
        """
        values = AsIs(','.join(fmt_str.format(**coin) for coin in coin_data))
        params = {
            "columns": AsIs(columns),
            "values": values
        }
        query = """ INSERT INTO """ + self.table_name('coins') + """ (%(columns)s) VALUES %(values)s; """
        self._exec_query(query, params)
        return values

    def get_coins_by_market_cap(self, mkt_cap, greater_less):
        query = """
            SELECT * FROM """ + self.table_name('coins') + """ WHERE mkt_cap """ + greater_less + str(mkt_cap)
        return self._fetch_query(query, {})
