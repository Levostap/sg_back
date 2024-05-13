from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)


def populate_gifts_table():
    conn = sqlite3.connect('gifts.db')
    c = conn.cursor()

    # Пример тестовых данных для товаров
    gifts_data = [
        ('Flower Bouquet', 'Beautiful bouquet of flowers', 'birthday', 25.99),
        ('Chocolate Box', 'Delicious assorted chocolates', 'valentine', 15.49),
        ('Scented Candle', 'Elegant scented candle in a glass jar', 'anniversary', 12.99),
        ('Teddy Bear', 'Cute and cuddly teddy bear', 'birthday', 20.00),
        ('Wristwatch', 'Stylish wristwatch with leather strap', 'anniversary', 49.99)
    ]

    # Вставляем тестовые данные в таблицу
    c.executemany("INSERT INTO gifts (name, description, category, price) VALUES (?, ?, ?, ?)", gifts_data)

    conn.commit()
    conn.close()


def create_gifts_table():
    conn = sqlite3.connect('gifts.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS gifts (
                 id INTEGER PRIMARY KEY,
                 name TEXT NOT NULL,
                 description TEXT,
                 category TEXT,
                 price REAL
                 )''')

    conn.commit()
    conn.close()


def create_users_table():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY,
                 username TEXT UNIQUE NOT NULL,
                 password TEXT NOT NULL,
                 email TEXT NOT NULL,
                 name TEXT,
                 cart TEXT
                 )''')

    conn.commit()
    conn.close()


# Функция для получения списка подарков
def get_gifts(category=None, price_range=None, sort_by=None, limit=None):
    conn = sqlite3.connect('gifts.db')
    c = conn.cursor()

    # Базовый SQL-запрос для выборки подарков
    sql_query = "SELECT * FROM gifts"

    # Формирование условий запроса
    conditions = []
    params = []

    if category:
        conditions.append("category = ?")
        params.append(category)
    if price_range:
        min_price, max_price = price_range.split('-')
        conditions.append("price BETWEEN ? AND ?")
        params.extend((min_price, max_price))
    if sort_by:
        sql_query += f" ORDER BY {sort_by}"
    if limit:
        sql_query += f" LIMIT {limit}"

    # Формирование полного SQL-запроса
    if conditions:
        sql_query += " WHERE " + " AND ".join(conditions)

    c.execute(sql_query, params)
    gifts_list = c.fetchall()
    conn.close()
    gifts = []
    meaning = ['id', 'name', 'description', 'category', 'price']
    for gift in gifts_list:
        gifts.append(dict(zip(meaning, gift)))

    return gifts


# Эндпоинт для получения списка подарков
@app.route('/api/gifts', methods=['GET'])
def api_get_gifts():
    category = request.args.get('category')
    price_range = request.args.get('price_range')
    sort_by = request.args.get('sort_by')
    limit = request.args.get('limit')

    gifts = get_gifts(category, price_range, sort_by, limit)

    return jsonify(gifts=gifts)


def get_gift_by_id(gift_id):
    conn = sqlite3.connect('gifts.db')
    c = conn.cursor()

    c.execute("SELECT * FROM gifts WHERE id=?", (gift_id,))
    gift = c.fetchone()
    conn.close()

    return gift


# Эндпоинт для получения информации о подарке по его идентификатору
@app.route('/api/gift/<int:gift_id>', methods=['GET'])
def api_get_gift_by_id(gift_id):
    gift = get_gift_by_id(gift_id)

    if gift:
        return jsonify(gift)
    else:
        return jsonify({'error': 'Gift not found'}), 404



@app.route('/api/ideas', methods=['GET'])
def getIdeas():
    ideas = [
        {"id": 1, "title": "Книга", "body": "Хорошая книга по интересующей теме"},
        {"id": 2, "title": "Подписка на стриминговый сервис", "body": "Месячная подписка на Netflix или Spotify"},
        {"id": 3, "title": "Кофейный абонемент", "body": "Абонемент на кофе в любимом кофейном магазине"},
        {"id": 4, "title": "Подарочный сертификат в кафе или ресторан",
         "body": "Вечер ужина в ресторане или уютное кафе"},
        {"id": 5, "title": "Уникальные кулинарные инструменты", "body": "Набор для приготовления суши или фондю"},
        {"id": 6, "title": "Путешествие", "body": "Короткое путешествие в ближайший город или курорт"},
    ]
    return jsonify(ideas)

# Функция для регистрации нового пользователя
def register_user(username, password, email, name):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # Проверяем, не существует ли уже пользователь с таким именем
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    existing_user = c.fetchone()

    if existing_user:
        conn.close()
        return jsonify({'error': 'Username already exists'}), 400

    # Вставляем нового пользователя в базу данных
    c.execute("INSERT INTO users (username, password, email, name) VALUES (?, ?, ?, ?)",
              (username, password, email, name))
    conn.commit()
    conn.close()

    return jsonify({'message': 'User registered successfully'})


# Эндпоинт для регистрации нового пользователя
@app.route('/api/register', methods=['POST'])
def api_register_user():
    data = request.json

    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    name = data.get('name')

    if not username or not password or not email or not name:
        return jsonify({'error': 'Missing required fields'}), 400

    return register_user(username, password, email, name)


if __name__ == '__main__':
    # populate_gifts_table()
    create_gifts_table()
    create_users_table()
    app.run(debug=True, host="0.0.0.0")
