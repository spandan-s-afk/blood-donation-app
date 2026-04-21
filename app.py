from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)

donor_list = ["A+", "B+", "O-"]

@app.route('/')
def home():
    return render_template("index.html", donors=donor_list)

@app.route('/add', methods=['POST'])
def add_donor():
    blood = request.form.get("blood_group")
    if blood:
        donor_list.append(blood)
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))