# -*- coding:utf-8 -*-
import pymysql

"""DBHelper
    数据库操作工具类
"""


class DBHelper:
    """
    """

    def __init__(self, connection, autocommit=True):
        if connection is None:
            raise Exception("connection is not null.")
        self.conn = connection
        if not autocommit:
            self.conn.autocommit(True)

    def __del__(self):
        self.close()

    def close(self):
        """Closes this database connection."""
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def queryone(self, commandtext, *parameters):
        """Returns a row for the given query and parameters."""
        cursor = self.conn.cursor()
        try:
            cursor.execute(commandtext, *parameters)
            return cursor.fetchone()
        finally:
            cursor.close()

    def query(self, commandtext, *parameters):
        """Returns a row list for the given query and parameters."""
        cursor = self.conn.cursor()
        try:
            cursor.execute(commandtext, *parameters)
            return cursor.fetchall()
        finally:
            cursor.close()

    def querydic(self, commandtext, *parameters):
        """Returns a row list for the given query and parameters."""
        cursor = self.conn.cursor()
        try:
            cursor.execute(commandtext, *parameters)
            if cursor.description is None:
                return []
            column_names = [d[0] for d in cursor.description]
            return [Row(zip(column_names, row)) for row in cursor]
        finally:
            cursor.close()

    def execute(self, commandtext, *parameters):
        """Executes the given sql."""
        cursor = self.conn.cursor()
        try:
            cursor.execute(commandtext, *parameters)
        finally:
            cursor.close()

    def insert(self, commandtext, *parameters):
        """Executes the given sql."""
        cursor = self.conn.cursor()
        try:
            cursor.execute(commandtext, *parameters)
        finally:
            cursor.close()
        return cursor.lastrowid

    def executemany(self, sql, *parameters):
        """
            Executes the given query against all the given param sequences.
        """
        cursor = self.conn.cursor()
        try:
            cursor.executemany(sql, *parameters)
        finally:
            cursor.close()

    def commit(self):
        if not self.conn.get_autocommit():
            self.conn.commit()

    def rollback(self):
        if not self.conn.get_autocommit():
            self.conn.rollback()


class Row(dict):
    """A dict that allows for object-like property access syntax."""

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)
