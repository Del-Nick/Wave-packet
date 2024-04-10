import json
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


def connection():
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

        self.conn = connection()

        self.collect_data()

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


class Lab:

    def __init__(self, id: int = None, full_name: str = None, callback_name: str = None):
        self.id = id
        self.full_name = full_name
        self.short_name = None
        self.callback_name = callback_name
        self.about = None
        self.main_picture = None
        self.areas = None
        self.contacts = None
        self.courseworks = None

        # self.conn = user.conn
        self.conn = connection()
        self.collect_data()

    def collect_data(self):
        try:
            with self.conn.cursor() as cursor:
                if self.callback_name is not None:
                    cursor.execute('SELECT * FROM Labs WHERE callback_name = %s', (self.callback_name,))

                elif self.id is not None:
                    cursor.execute('SELECT * FROM Labs WHERE id = %s', (self.id,))

                else:
                    cursor.execute('SELECT * FROM Labs WHERE full_name = %s', (self.full_name,))

                values = cursor.fetchone()

                if values is not None:
                    if self.id is None:
                        self.id = values[0]
                    if self.full_name is None:
                        self.full_name = values[1]
                    if self.callback_name is None:
                        self.callback_name = values[3]

                    self.short_name = values[2]
                    self.about = values[4]
                    self.main_picture = values[5]
                    self.areas = None if values[6] is None else json.loads(values[6])
                    self.contacts = values[7]
                    self.courseworks = None if values[8] is None else json.loads(values[8])



                return True

        except:
            traceback.print_exc()
            return False

    def add_new_lab(self):
        try:
            labs = AllLabs()
            self.id = 0 if len(labs.labs) == 0 else max(labs[:][0]) + 1
            with self.conn.cursor() as cursor:
                cursor.execute('INSERT INTO Labs (id, full_name, short_name, callback_name, about, main_picture, '
                               'areas, contacts, courseworks) '
                               'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                               (self.id,
                                self.full_name,
                                self.short_name,
                                self.callback_name,
                                self.about,
                                self.main_picture,
                                self.areas,
                                self.contacts,
                                self.courseworks,))
                self.conn.commit()
            return True

        except:
            traceback.print_exc()
            return False

    def update_lab(self):
        try:
            with self.conn.cursor() as cursor:
                if self.id is not None:
                    cursor.execute('UPDATE Labs SET full_name=%s, short_name=%s, callback_name=%s, about=%s, '
                                   'main_picture=%s, areas=%s, contacts=%s, courseworks=%s, WHERE id = %s',
                                   (self.full_name,
                                    self.short_name,
                                    self.callback_name,
                                    self.about,
                                    self.main_picture,
                                    self.areas,
                                    self.contacts,
                                    self.courseworks,
                                    self.callback_name,))
                    self.conn.commit()
                    return True

                elif self.callback_name is not None:
                    cursor.execute(
                        'UPDATE Labs SET full_name=%s, short_name=%s, about=%s, main_picture=%s, areas=%s, '
                        'contacts=%s, courseworks=%s, WHERE id = %s',
                        (self.full_name,
                         self.short_name,
                         self.about,
                         self.main_picture,
                         self.areas,
                         self.contacts,
                         self.courseworks,
                         self.callback_name,))
                    self.conn.commit()
                    return True

                else:
                    return False

        except:
            traceback.print_exc()
            return False

    def delete_lab(self):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute('DELETE from Labs WHERE id=%s', (self.id,))
                self.conn.commit()
                return True

        except:
            traceback.print_exc()
            return False


class AllLabs:
    def __init__(self, user: User = None):
        self.labs = None
        self.conn = connection()
        self.get_all_group_names()

    def get_all_group_names(self):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute('SELECT id, full_name, short_name, callback_name FROM Labs')
                self.labs = cursor.fetchall()
        except:
            traceback.print_exc()