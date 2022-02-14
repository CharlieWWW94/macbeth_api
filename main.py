from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database Connection...

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///macbeth.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)


# Quotation Table...
class Quotation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    act = db.Column(db.Integer, nullable=False)
    scene = db.Column(db.Integer, nullable=False)
    character = db.Column(db.String(100), nullable=False)
    quotation = db.Column(db.String, unique=True, nullable=False)
    theme_1 = db.Column(db.String(100), nullable=False)
    theme_2 = db.Column(db.String(100), nullable=True)
    theme_3 = db.Column(db.String(100), nullable=True)


db.create_all()

@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
