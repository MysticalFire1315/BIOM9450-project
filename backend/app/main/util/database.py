import logging
import textwrap
import time
from contextlib import contextmanager

from psycopg2 import errorcodes, errors, pool
from psycopg2.extras import LoggingConnection, LoggingCursor


# Logging psycopg2 -> https://stackoverflow.com/a/14095624
class LoggingConnection2(LoggingConnection):
    def filter(self, msg, curs):
        t = (time.time() - curs.timestamp) * 1000
        return f"Query executed in: {t:.2f} ms. {curs.rowcount} row(s) affected."

    def cursor(self, *args, **kwargs):
        kwargs.setdefault("cursor_factory", LoggingCursor2)
        return super(LoggingConnection, self).cursor(*args, **kwargs)


class LoggingCursor2(LoggingCursor):
    def execute(self, query, vars=None):
        logger = logging.getLogger("psycopg2")
        if isinstance(query, str):
            query = self.mogrify(query, vars)

        query = query.decode("utf-8") if isinstance(query, bytes) else query
        query = textwrap.dedent(query)
        query = f"\n{query}" if query[0] != "\n" else query
        query = f"{query}\n" if query[-1] != "\n" else query
        logger.info(query)

        try:
            self.timestamp = time.time()
            return LoggingCursor.execute(self, query)
        except Exception as exc:
            logging.error(f"{exc.__class__.__name__}: {exc}")
            raise exc

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
    connection_factory=LoggingConnection2,
)

UniqueViolation = errors.lookup(errorcodes.UNIQUE_VIOLATION)
NotNullViolation = errors.lookup(errorcodes.NOT_NULL_VIOLATION)


@contextmanager
def db_get_cursor():
    try:
        con = postgreSQL_pool.getconn()
        con.initialize(logging.getLogger("psycopg2"))
        cur = con.cursor()
        yield cur
        con.commit()
    except Exception as err:
        con.rollback()
        raise err
    finally:
        cur.close()
        postgreSQL_pool.putconn(con)
