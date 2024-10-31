from contextlib import contextmanager
from psycopg2 import errors, errorcodes, pool

import os
import time
from psycopg2.extras import LoggingConnection, LoggingCursor
import logging

from flask import current_app
import traceback

# Logging psycopg2 -> https://stackoverflow.com/a/14095624
class LoggingConnection2(LoggingConnection):
    def filter(self, msg, curs):
        t = (time.time() - curs.timestamp) * 1000
        try:
            return msg.decode() + os.linesep + f'Query executed in: {t:.2f} ms. {curs.rowcount} row(s) affected.'
        except Exception:
            # current_app.logger.error(traceback.format_exc())
            pass

    def cursor(self, *args, **kwargs):
        kwargs.setdefault('cursor_factory', LoggingCursor2)
        return super(LoggingConnection, self).cursor(*args, **kwargs)

class LoggingCursor2(LoggingCursor):
    def execute(self, query, vars=None):
        self.timestamp = time.time()
        return LoggingCursor.execute(self, query, vars)

    def callproc(self, procname, vars=None):
        self.timestamp = time.time()
        return LoggingCursor.execute(self, procname, vars)

postgreSQL_pool = pool.SimpleConnectionPool(
    1,
    20,
    # user="postgres",
    # password="postgres",
    # host="127.0.0.1",
    # port="5432",
    database="biom_project_test",
    connection_factory=LoggingConnection2
)

UniqueViolation = errors.lookup(errorcodes.UNIQUE_VIOLATION)
NotNullViolation = errors.lookup(errorcodes.NOT_NULL_VIOLATION)

@contextmanager
def db_get_cursor():
    try:
        con = postgreSQL_pool.getconn()
        con.initialize(current_app.logger)
        cur = con.cursor()
        yield cur
        con.commit()
    except Exception as err:
        con.rollback()
        raise err
    finally:
        cur.close()
        postgreSQL_pool.putconn(con)
