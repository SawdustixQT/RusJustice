import mysql.connector as conn

# Переменные для подключения к базе MySQL
DB_HOST = ""  # Название хоста
DB_USER = ""  # Имя пользователя
DB_PASSWORD = ""  # Пароль пользователя
DB_NAME = ""  # Название базы данных

def db_connection(db_host, db_user, db_passwd, db_name):
    try:
        connection = conn.connect(
            host=db_host,
            user=db_user,
            password=db_passwd,
            database=db_name
        )
        return connection
    except conn.Error as e:
        print(e)


def create_db(db_host, db_user, db_passwd, db_name):
    try:
        connection = conn.connect(
            host=db_host,
            user=db_user,
            password=db_passwd
        )
        create_db_query = f'''CREATE DATABASE IF NOT EXISTS {db_name}'''
        with connection.cursor() as cursor:
            cursor.execute(create_db_query)
    except conn.Error as e:
        print(e)


def create_tables(db_host, db_user, db_passwd, db_name):
    try:
        connection = db_connection(db_host, db_user, db_passwd, db_name)

        create_table_journals_query = '''
        CREATE TABLE IF NOT EXISTS journals(
            id INT AUTO_INCREMENT,
            filename VARCHAR(60) NOT NULL,
            date DATE NOT NULL,
            file LONGBLOB NOT NULL,
            PRIMARY KEY (id) 
        );
        '''

        with connection.cursor() as cursor:
            cursor.execute(create_table_journals_query)
            connection.commit()
        connection.close()
    except conn.Error as e:
        print(e)


def main():
    create_db(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
    create_tables(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)


if __name__ == '__main__':
    main()
