from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Blood Donation Management System Running"})

@app.route('/donors')
def donors():
    return jsonify({"donors": ["A+", "B+", "O-"]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)