import psycopg2
from datetime import datetime
import pytz
import pandas as pd
import lpr_const as lpr

class SQLighter:

    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = psycopg2.connect(
            database=database,
            user=lpr.user,
            password=lpr.password,
            host=lpr.host,
            port=lpr.port
        )

        self.cursor = self.connection.cursor()


    def send_base_reg (self):
            self.cursor.execute("SELECT user_id, times, username, first_name, last_name, status from subscriptions_reg")
            res = pd.DataFrame()
            rows = self.cursor.fetchall()
            for row in rows:
                user_id = row[0]
                times = row[1]
                username = row[2]
                first_name = row[3]
                last_name = row[4]
                status = row[5]

                res = res.append(pd.DataFrame([[user_id, times, username, first_name, last_name, status]],
                                             columns=['user_id', 'times', 'username', 'first_name', 'last_name_id',
                                                      'status']), ignore_index=True)

            res.to_excel('result_reg.xlsx')

    def send_base_mos (self):
            self.cursor.execute("SELECT user_id, times, username, first_name, last_name, status from subscriptions_msk")
            res = pd.DataFrame()
            rows = self.cursor.fetchall()
            for row in rows:
                user_id = row[0]
                times = row[1]
                username = row[2]
                first_name = row[3]
                last_name = row[4]
                status = row[5]

                res = res.append(pd.DataFrame([[user_id, times, username, first_name, last_name, status]],
                                             columns=['user_id', 'times', 'username', 'first_name', 'last_name_id',
                                                      'status']), ignore_index=True)

            res.to_excel('result_mos.xlsx')

    def subscriber_exists(self, username):
        """Проверяем, есть ли уже юзер в базе"""
        with self.connection:
            result = self.cursor.execute("select exists(select 1 from subscriptions_reg where user_id = %s)",
                                         (str(username),))

            return self.cursor.fetchone()[0]

    def subscriber_exists_username_reg(self, username):
        """Проверяем, есть ли уже юзер в базе"""
        with self.connection:
            result = self.cursor.execute("select exists(select 1 from subscriptions_reg where username = %s)",
                                         (str(username),))

            return self.cursor.fetchone()[0]

    def subscriber_exists_username_msk(self, username):
        """Проверяем, есть ли уже юзер в базе"""
        with self.connection:
            result = self.cursor.execute("select exists(select 1 from subscriptions_msk where username = %s)",
                                         (str(username),))

            return self.cursor.fetchone()[0]

    def get_subscriptions(self):
        self.cursor.execute("SELECT user_id, times, username, first_name, last_name, status from subscriptions_reg")
        rows = self.cursor.fetchall()
        great_dict = {}
        user_ids = ()
        status = ()
        for row in rows:
            user_id = row[0]
            status = row[5]


        print (type(great_dict))
        return great_dict



    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()

