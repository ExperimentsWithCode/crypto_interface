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
            'save_mention_bodies': 'mention_bodies'
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

    def save_summaries(self, summaries):
        log.debug('{PSQL} == SAVE market summaries ==')
        fmt_str = "({volume},{last},{opensellorders},{bid},{openbuyorders},'{marketname}',{ask},{basevolume},'{saved_timestamp}',{ticker_nonce})"
        columns = "volume,last,opensellorders,bid,openbuyorders,marketname,ask,basevolume,saved_timestamp,ticker_nonce"
        values = AsIs(','.join(fmt_str.format(**summary) for summary in summaries))
        params = {
            "columns": AsIs(columns),
            "values": values
        }
        query = """ INSERT INTO """ + self.table_name('save_summaries') + """ (%(columns)s) VALUES %(values)s ; """
        self._exec_query(query, params)

    def save_markets(self, markets):
        log.debug('{PSQL} == SAVE markets ==')
        fmt_str = "('{marketcurrency}','{basecurrency}','{marketcurrencylong}','{basecurrencylong}',{mintradesize},'{marketname}',{isactive},'{logourl}')"
        columns = "marketcurrency,basecurrency,marketcurrencylong,basecurrencylong,mintradesize,marketname,isactive,logourl"
        values = AsIs(','.join(fmt_str.format(**market) for market in markets))
        params = {
            "columns": AsIs(columns),
            "values": values
        }
        query = """ INSERT INTO """ + self.table_name('save_markets') + """ (%(columns)s) VALUES %(values)s ; """
        self._exec_query(query, params)

    def save_currencies(self, markets):
        log.debug('{PSQL} == SAVE currencies ==')
        fmt_str = "('{currency}','{currencylong}',{minconfirmation},{txfee},{isactive},'{cointype}','{baseaddress}')"
        columns = "currency,currencylong,minconfirmation,txfee,isactive,cointype,baseaddress"
        values = AsIs(','.join(fmt_str.format(**market) for market in markets))
        params = {
            "columns": AsIs(columns),
            "values": values
        }
        query = """ INSERT INTO """ + self.table_name('save_currencies') + """ (%(columns)s) VALUES %(values)s ; """
        self._exec_query(query, params)

    def save_historical_data(self, data):
        log.debug('{PSQL} == SAVE historical data ==')
        fmt_str = '(%s,%s,%s,%s,%s,%s,%s,%s)'
        columns = 'timestamp,open,high,low,close,volume_btc,volume_usd,weighted_price'
        values = AsIs(','.join(fmt_str % tuple(row) for row in data))
        params = {
            "columns": AsIs(columns),
            "values": values
        }
        query = """ INSERT INTO btc_historical (%(columns)s) VALUES %(values)s ; """
        self._exec_query(query, params)

    def get_historical_data(self, start_date, end_date):
        log.debug('{PSQL} == GET historical data ==')
        params = {
            "start_date": mktime(start_date.timetuple()),
            "end_date": mktime(end_date.timetuple())
        }
        query = """
            SELECT open, high, low, close, volume_btc, volume_usd, timestamp FROM btc_historical
            WHERE timestamp >= %(start_date)s AND timestamp < %(end_date)s
            ORDER BY timestamp ASC ;
        """
        return self._fetch_query(query, params)

    def get_market_summaries_by_timestamp(self, target_timestamp):
        log.debug('{PSQL} == GET market summaries ==')
        params = {
            'target_timestamp': target_timestamp
        }
        query = """
            SELECT marketname, last, bid, ask, saved_timestamp FROM market_summaries
            WHERE saved_timestamp = {target_timestamp} ;
        """
        return self._fetch_query(query, params)

    def get_market_summaries_by_ticker(self, tick, markets):
        market_names = tuple(markets['marketname'].values)
        log.debug('{PSQL} == GET market summaries by ticker ==')
        params = {
            'ticker_nonce': tick,
            'market_names': market_names
        }
        query = """
            SELECT marketname, last, bid, ask, saved_timestamp, volume FROM fixture_market_summaries
            WHERE ticker_nonce = %(ticker_nonce)s AND marketname IN %(market_names)s
            ;
        """
        return self._fetch_query(query, params)
