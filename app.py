import sqlite3
import os
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Initialize DB
def init_db():
    conn = sqlite3.connect('donors.db')
    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS donors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        blood TEXT
    )
    ''')

    c.execute("SELECT COUNT(*) FROM donors")
    if c.fetchone()[0] == 0:
        c.executemany("INSERT INTO donors (name, age, blood) VALUES (?, ?, ?)", [
            ("Rahul Sharma", 22, "A+"),
            ("Priya Singh", 21, "B+"),
            ("Amit Kumar", 25, "O+"),
            ("Neha Verma", 23, "A-"),
            ("Rohan Das", 24, "B-"),
            ("Sneha Iyer", 22, "O-"),
            ("Arjun Mehta", 26, "AB+"),
            ("Pooja Reddy", 20, "AB-"),
            ("Karan Patel", 27, "A+"),
            ("Anjali Gupta", 21, "B+")
        ])

    conn.commit()
    conn.close()


# HOME + SEARCH
@app.route('/')
def home():
    search = request.args.get('blood')

    conn = sqlite3.connect('donors.db')
    c = conn.cursor()

    if search:
        c.execute("SELECT id, name, age, blood FROM donors WHERE blood = ?", (search,))
    else:
        c.execute("SELECT id, name, age, blood FROM donors")

    donors = c.fetchall()
    conn.close()

    return render_template("index.html", donors=donors)


# ADD
@app.route('/add', methods=['POST'])
def add_donor():
    name = request.form.get("name")
    age = request.form.get("age")
    blood = request.form.get("blood_group")

    if name and age and blood:
        conn = sqlite3.connect('donors.db')
        c = conn.cursor()
        c.execute("INSERT INTO donors (name, age, blood) VALUES (?, ?, ?)", (name, age, blood))
        conn.commit()
        conn.close()

    return redirect('/')


# DELETE
@app.route('/delete/<int:id>')
def delete_donor(id):
    conn = sqlite3.connect('donors.db')
    c = conn.cursor()
    c.execute("DELETE FROM donors WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')


# EDIT PAGE
@app.route('/edit/<int:id>')
def edit_page(id):
    conn = sqlite3.connect('donors.db')
    c = conn.cursor()
    c.execute("SELECT * FROM donors WHERE id=?", (id,))
    donor = c.fetchone()
    conn.close()
    return render_template("edit.html", donor=donor)


# UPDATE
@app.route('/update/<int:id>', methods=['POST'])
def update_donor(id):
    name = request.form.get("name")
    age = request.form.get("age")
    blood = request.form.get("blood_group")

    conn = sqlite3.connect('donors.db')
    c = conn.cursor()
    c.execute("UPDATE donors SET name=?, age=?, blood=? WHERE id=?",
              (name, age, blood, id))
    conn.commit()
    conn.close()

    return redirect('/')


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))