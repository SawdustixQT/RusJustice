from flask import Flask, render_template, redirect, request, flash, send_from_directory, url_for, send_file
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
import os
import pprint
import mysql.connector as conn  # База данных
from io import BytesIO
from database.init_db import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

# Приложение
JOURNAL_UPLOAD_FOLDER = 'uploads\\journals'
app = Flask(__name__)
app.config['JOURNAL_UPLOAD_FOLDER'] = JOURNAL_UPLOAD_FOLDER


# Подключение к базе данных
def db_connection(db_host=DB_HOST, db_user=DB_USER, db_passwd=DB_PASSWORD, db_name=DB_NAME):
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


# Главная страница
@app.route('/', methods=['GET', 'POST'])
def main_page():
    if request.method == 'POST':
        print(1)
    return render_template("main_page.html")


# Страница "О журнале"
@app.route('/pages/about')
def about():
    return render_template('pages/about.html')


def convert_date(file_path):
    # sub_date = file_path[file_path.find('_') + 1:file_path.rfind('.')]
    # date = sub_date.split('_')
    # year = date[0]
    # mounth = str(int(date[1]) * 3)
    year = '2025'
    mounth = '01'
    day = '1'
    return f'{year}-{mounth}-{day}'


def convert_to_blob(file_path):
    with open(file_path, 'rb') as file:
        blob = file.read()
    return blob


# Страница "Журналы"
@app.route('/pages/journals', methods=['GET', 'POST'])
def journals():
    if request.method == 'POST':
        if 'journal' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['journal']
        # Сохранение файла в директорию
        if file:
            filename = file.filename
            file_path = os.path.join(app.root_path, app.config['JOURNAL_UPLOAD_FOLDER'], filename)
            file.save(file_path)
            #
            file_date = convert_date(file_path)
            file_blob = convert_to_blob(file_path)
            print(file_date)
            # Запись файла в базу данных
            # db_con = db_connection()
            # insert_cursor = db_con.cursor()
            # insert_sql = "INSERT INTO journals(filename, date, file) VALUES(%s, %s, %s)"
            # insert_val = (filename, file_date, file_blob)
            # insert_cursor.execute(insert_sql, insert_val)
            # db_con.commit()
            # db_con.close()

    # db_con = db_connection()
    # journals_cursor = db_con.cursor()
    # journals_cursor.execute('SELECT * FROM journals')
    #list_of_journals = journals_cursor.fetchall()
    # db_con.close()
    count_of_journals = 0 #len(list_of_journals)  # Получения из БД количества журналов
    if count_of_journals == 0:
        print('Нет журналов')
    corrected_list_of_journals =[]# [list(i)[1] for i in list_of_journals]
    return render_template('pages/journals.html', count_of_journals=count_of_journals,
                           journals=corrected_list_of_journals)


# Страница "Контакты"
@app.route('/pages/contacts')
def contacts():
    return render_template('pages/contacts.html')


# Страница "Редколлегия"
@app.route('/pages/editorial_board')
def editorial_board():
    return render_template('pages/editorial_board.html')


# Страница "Публикационная этика"
@app.route('/pages/publication_policy')
def publication_policy():
    return render_template('pages/publication_policy.html')


# Страница "Редакционная политика"
@app.route('/pages/editorial_policy')
def publications():
    return render_template('pages/publications.html')


# Страница "Авторам"
@app.route('/pages/to_authors')
def to_authors():
    return render_template('pages/to_authors.html')


# Страница ошибки 404
@app.errorhandler(404)
def page_404(e):
    return render_template("404.html")


# Функция для открытия журнала в формате pdf
@app.route('/uploads/journals/<string:journal_filename>', methods=['GET', 'POST'])
def journal_pdf(journal_filename):
    return send_from_directory(app.config['JOURNAL_UPLOAD_FOLDER'], journal_filename, mimetype='application/pdf',
                               download_name=journal_filename)


if __name__ == '__main__':
    app.run(debug=True)
