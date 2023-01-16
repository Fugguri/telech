import pymysql
from config import host, user, password


class Database:
    def __init__(self, db_name):
        self.connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=db_name,
        )
        self.connection.autocommit(True)

    def create_tables(self):

        with self.connection.cursor() as cursor:
            cursor.execute("""CREATE TABLE IF NOT EXISTS users
            (id INT PRIMARY KEY AUTO_INCREMENT,
            telegram_id BIGINT UNIQUE NOT NULL,
            full_name TEXT,
            username TEXT,
            chat_amount INT UNIQUE NOT NULL DEFAULT 0,
            subscription TEXT,
            subscription_type TEXT
        );""")
            self.connection.commit()

        with self.connection.cursor() as cursor:
            cursor.execute("""CREATE TABLE IF NOT EXISTS chats_or_channels
        (id INT PRIMARY KEY AUTO_INCREMENT,
            chat_id BIGINT UNIQUE NOT NULL,
            chat_name TEXT,
            chat_subs_amount INT,
            chat_link TEXT);""")
            self.connection.commit()
        with self.connection.cursor() as cursor:
            cursor.execute("""CREATE TABLE IF NOT EXISTS event
        (id INT PRIMARY KEY AUTO_INCREMENT,
            chat_id BIGINT UNIQUE NOT NULL,
            chat_name TEXT,
            chat_subs_amount BIGINT,
            chat_link TEXT);""")
            self.connection.commit()
        with self.connection.cursor() as cursor:
            cursor.execute("""CREATE TABLE IF NOT EXISTS admin
        (id INT PRIMARY KEY AUTO_INCREMENT,
            admin_id BIGINT,
            event_amout BIGINT,
            report_amount BIGINT,
            user_amount BIGINT
        );""")
            self.connection.commit()
        with self.connection.cursor() as cursor:
            create = """    CREATE TABLE IF NOT EXISTS users_chats
                    (id INT PRIMARY KEY AUTO_INCREMENT,
                    user_id INT NOT NULL,
                    chat_id INT NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES users(id),
                    FOREIGN KEY(chat_id) REFERENCES chats_or_channels(id)
                    );
                """
            cursor.execute(create)
            self.connection.commit()

    def create_user(self, telegram_id, full_name: str, username: str,):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            cursor.execute(
                'INSERT IGNORE INTO users (telegram_id, full_name, username) VALUES(%s, %s, %s)', (telegram_id, full_name, username))
            self.connection.commit()
            self.connection.close()

    def create_chat_or_channel(self, chat_link):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            cursor.execute(
                'INSERT IGNORE INTO chats_or_channels (chat_link) VALUES(%s)', (chat_link,))
            self.connection.commit()
            self.connection.close()

    def add_chat(self, telegram_id: int, chat_link, chat_num, chat_subs_amount, chat_name):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            cursor.execute(
                f'''
                CREATE TABLE IF NOT EXISTS chat_{str(chat_num)[1:]}
                (id INT PRIMARY KEY AUTO_INCREMENT,
                user_id BIGINT,
                username TEXT,
                full_name TEXT ,
                status TEXT,
                date TEXT,
                subs_amount BIGINT);''')
            self.connection.commit()
        with self.connection.cursor() as cursor:

            cursor.execute(
                'INSERT IGNORE INTO chats_or_channels (chat_link,chat_id,chat_subs_amount,chat_name) VALUES(%s,%s,%s,%s)', (chat_link, chat_num, chat_subs_amount, chat_name))
            self.connection.commit()

            cursor.execute(
                "SELECT id FROM users WHERE telegram_id=(%s)", (telegram_id,))
            user_id = cursor.fetchone()[0]
            print(chat_name)
            cursor.execute(
                "SELECT id FROM chats_or_channels WHERE chat_name=(%s)", (chat_name,))
            chat_id = cursor.fetchone()[0]
            cursor.execute(
                'INSERT IGNORE INTO users_chats(user_id, chat_id) VALUES (%s,%s)', (user_id, chat_id))
            self.connection.commit()

    def all_chats(self, telegram_id):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            keywords = cursor.execute(
                '''SELECT chat_name
                    FROM chats_or_channels
                    WHERE id IN (SELECT chat_id FROM users_chats WHERE user_id =(SELECT id FROM users WHERE telegram_id=(%s))) ''', (telegram_id,))
            keywords = cursor.fetchall()
            self.connection.commit()
            self.connection.close()
            return [i[0] for i in keywords]

    def add_event(self, chat_id, user_id, username, full_name, status, date, subs_amount):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            table_name = f"chat_{str(chat_id)[1:]}"
            cursor.execute(
                '''INSERT IGNORE INTO ''' + table_name + '''(user_id, username, full_name, status, date, subs_amount)
                VALUES (%s,%s,%s,%s,%s,%s) ''',
                (user_id, username, full_name, status, date, subs_amount))

            self.connection.commit()
            self.connection.close()

    def user_event(self, user_id):
        result = {}
        self.connection.ping()
        with self.connection.cursor() as cursor:
            sql = "SELECT chat_id,chat_name FROM chats_or_channels WHERE id in(SELECT chat_id FROM users_chats WHERE user_id = (SELECT user_id FROM users WHERE telegram_id=(%s)))"
            cursor.execute(
                sql, (user_id))
            chats = cursor.fetchall()
        with self.connection.cursor() as cursor:
            for chat_id in chats:
                sql = "SELECT * FROM chat_"+str(chat_id[0])[1:]
                cursor.execute(sql)
                result[chat_id[1]] = cursor.fetchall()
        return result
