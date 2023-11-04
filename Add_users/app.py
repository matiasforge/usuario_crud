from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'users',
}

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        email TEXT
    )
''')
conn.commit()

@app.route('/users')
def read_all_users():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return render_template('add_user.html', users=users)


@app.route('/users/<int:user_id>')
def show_one_user(user_id):
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    return render_template('edit_user.html', user=user)


@app.route('/users/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        cursor.execute("INSERT INTO users (first_name, last_name, email) VALUES (%s, %s, %s)", (first_name, last_name, email))
        conn.commit()
        return redirect(url_for('read_all_users'))
    return render_template('add_user.html')


@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        cursor.execute("UPDATE users SET first_name = %s, last_name = %s, email = %s WHERE id = %s", (first_name, last_name, email, user_id))
        conn.commit()
        return redirect(url_for('read_all_users'))
    cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()
    return render_template('edit_user.html', user=user)

@app.route('/users/<int:user_id>/delete', methods=['GET', 'POST'])
def delete_user(user_id):
    if request.method == 'POST':
        cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
        conn.commit()
        return redirect(url_for('add_user'))
    cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()
    return render_template('delete_user.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)
