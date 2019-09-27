import datetime as dt
import sqlite3
from typing import Optional, Tuple

from anpy import AbstractDataHandler
from anpy import Record
from anpy import Session


class SQLDataHandler(AbstractDataHandler):

    def __init__(self, db: sqlite3.Connection):
        self.db: sqlite3.Connection = db
        self._create_tables()
        db.commit()

    def new_category(self, name: str):
        name = name.strip()
        if not name:
            raise ValueError
        probe = self.db.execute(
            'SELECT name FROM categories WHERE name = ? AND active',
            [name]).fetchone()
        if probe:
            raise RuntimeError('Active category with that name exists')

        self.db.execute(
            'INSERT OR REPLACE INTO categories(name) VALUES (?)',
            [name]
        )
        self.db.commit()

    def set_category_activation(self, name: str, status: bool):
        if name in self.all_categories:
            self.db.execute('UPDATE categories SET active = ? where name = ?',
                            [status, name])
        else:
            raise ValueError('Does not exist')

    @property
    def all_categories(self) -> Tuple[str]:
        cur = self.db.execute('SELECT name FROM categories')
        return tuple(str(tup[0]) for tup in cur.fetchall())

    @property
    def active_categories(self) -> Tuple[str]:
        cur = self.db.execute(
            'SELECT name FROM categories WHERE active')
        return tuple(str(tup[0]) for tup in cur.fetchall())

    def start(self, name: str, start: Optional[dt.datetime] = None):
        """Record the beginning of a working session.

        If there is no datetime object passed in, the datetime associated with
        the current instant will be used instead.
        """
        if start is None:
            start = dt.datetime.now()

        if self.is_active_session():
            raise RuntimeError('Current session still running')

        if name not in self.active_categories:
            raise ValueError('Given ID does not exist.')

        self.db.execute('INSERT OR REPLACE INTO beginnings(name, time_start) '
                        + 'VALUES (?, ?)', [name, start.timestamp()])
        self.db.commit()

    def cancel(self):
        """Cancel the current working session that is running"""
        assert self.is_active_session(), 'No active session'
        self._mark_done_or_cancel()

    def complete(self, end: dt.datetime = None):
        """Record the end of a current working session.

        If there is no datetime object passed in, the datetime associated with
        the current instant will be used instead.
        """
        if end is None:
            end = dt.datetime.now()

        if self.is_active_session():
            session = self.get_most_recent_session()
            self._mark_done_or_cancel()
            self.db.execute('INSERT INTO records(name, time_start, time_end) '
                            + 'VALUES (?, ?, ?)',
                            [session.name,
                             session.time_start.timestamp(),
                             end.timestamp()])
            self.db.commit()
        else:
            raise RuntimeError('No running session')
        pass

    def rename_category(self, old_name: str, new_name: str):
        if old_name in self.all_categories:
            self.db.execute('UPDATE categories SET name = ? WHERE name = ?',
                            [new_name, old_name])
            self.db.execute('UPDATE beginnings SET name = ? WHERE name = ?',
                            [new_name, old_name])
            self.db.execute('UPDATE records SET name = ? WHERE name = ?',
                            [new_name, old_name])
        else:
            raise ValueError('Given category does not exist')

    def _create_tables(self):
        self.db.execute(
            'CREATE TABLE IF NOT EXISTS categories(name UNIQUE, active DEFAULT 1);'
        )
        self.db.execute(
            'CREATE TABLE IF NOT EXISTS beginnings(name, time_start, done_or_canceled DEFAULT 0);'
        )
        self.db.execute(
            'CREATE TABLE IF NOT EXISTS records(name, time_start, time_end, ignored DEFAULT 0);'
        )
        self.db.commit()

    def _mark_done_or_cancel(self):
        cur = self.db.execute(
            'SELECT ROWID FROM beginnings ORDER BY time_start DESC LIMIT 1')
        row = cur.fetchone()[0]
        self.db.execute('DELETE FROM beginnings')
        # self.db.execute(
        #    'UPDATE beginnings SET done_or_canceled = 1 WHERE ROWID = ?',
        #    [row])
        self.db.commit()

    def is_active_session(self):
        recent_session = self.get_most_recent_session()
        if recent_session:
            return not recent_session.done_or_canceled
        return False

    def get_most_recent_session(self):
        cur = self.db.execute(
            'SELECT cat.name, b.time_start, b.done_or_canceled '
            + 'FROM categories AS cat, beginnings as b WHERE cat.name = b.name ORDER BY time_start DESC LIMIT 1'
        )
        result = cur.fetchone()

        if result:
            return Session(result[0],
                           dt.datetime.fromtimestamp(result[1]),
                           bool(result[2]))
        else:
            return None

    def get_records_between(self, start: dt.datetime, end: dt.datetime):
        assert start < end, 'Invalid times'
        records = self.db.execute(
            'SELECT c.name, r.time_start, r.time_end '
            + 'FROM categories as c, records as r '
            + 'WHERE c.name = r.name AND r.time_start >= ? '
            + 'AND r.time_start < ? ORDER BY r.time_start', [start.timestamp(),
                                                             end.timestamp()]
        ).fetchall()
        return [Record(tup[0],
                       dt.datetime.fromtimestamp(tup[1]),
                       dt.datetime.fromtimestamp(tup[2]))
                for tup in records]
