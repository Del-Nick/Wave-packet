import time
import traceback

import pymysql
from sshtunnel import SSHTunnelForwarder
from config import *

server = SSHTunnelForwarder(
    ssh_address=(ssh_host, ssh_port),
    ssh_username=ssh_username,
    ssh_password=ssh_password,
    remote_bind_address=(db_host, db_port))

server.start()


class User:
    def __init__(self, id: int, username: str):
        self.id = id
        self.username = username
        self.nickname = None
        self.status = None
        self.usergroup = None
        self.action = None
        self.new_user = False

        self.admin = True if username in allowed_users else False

        self.conn = self.connection()

        self.collect_data()

    def connection(self):
        try:
            conn = pymysql.connect(
                db=db_name,
                host=db_host,
                user=ssh_username,
                password=db_password,
                port=server.local_bind_port)
            return conn

        except pymysql.err.OperationalError:
            traceback.print_exc()

    def collect_data(self):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute('SELECT * FROM Wave WHERE id = %s', (self.id,))
                values = cursor.fetchone()

                if values is None:
                    self.add_new_user()
                else:
                    self.status, self.usergroup, self.action, self.nickname, self.admin = values[2:]

                return True
        except:
            traceback.print_exc()

    def add_new_user(self):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute('INSERT INTO Wave (id, username, nickname, status, usergroup, action, admin)'
                               'VALUES (%s, %s, %s, %s, %s, %s, %s)',
                               (self.id, self.username, self.nickname, self.status, self.usergroup, 'registration',
                                self.admin))
                self.conn.commit()

                self.action = 'registration'
                self.new_user = True
        except:
            traceback.print_exc()

    def update(self):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute('UPDATE Wave SET nickname=%s, status=%s, usergroup=%s, action=%s, admin=%s '
                               'WHERE id = %s',
                               (self.nickname, self.status, self.usergroup, self.action, self.admin, self.id,))
                self.conn.commit()
                return True
        except:
            traceback.print_exc()

    def delete_user(self):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute('DELETE FROM Wave WHERE id = %s', (self.id,))
                self.conn.commit()
                return True
        except:
            traceback.print_exc()

