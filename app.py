import sqlite3
import os
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Create DB if not exists
def init_db():
    conn = sqlite3.connect('donors.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS donors (id INTEGER PRIMARY KEY, blood TEXT)')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    conn = sqlite3.connect('donors.db')
    c = conn.cursor()
    c.execute("SELECT blood FROM donors")
    donors = [row[0] for row in c.fetchall()]
    conn.close()
    return render_template("index.html", donors=donors)

@app.route('/add', methods=['POST'])
def add_donor():
    blood = request.form.get("blood_group")
    if blood:
        conn = sqlite3.connect('donors.db')
        c = conn.cursor()
        c.execute("INSERT INTO donors (blood) VALUES (?)", (blood,))
        conn.commit()
        conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))