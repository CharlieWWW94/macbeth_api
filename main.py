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


# add quotations to db...
@app.route("/add", methods=["GET", "POST"])
def add_quotation():
    new_id = len(Quotation.query.all()) + 1

    new_quotation = Quotation(id=new_id,
                              act=int(request.form.get("act")),
                              scene=int(request.form.get("scene")),
                              character=request.form.get("character"),
                              quotation=request.form.get("quotation"),
                              theme_1=request.form.get("theme_1"),
                              theme_2=request.form.get("theme_2"),
                              theme_3=request.form.get("theme_3"),
                              )

    db.session.add(new_quotation)
    db.session.commit()
    return jsonify({"response": {"success": "Successfully added new quotation"}})


if __name__ == "__main__":
    app.run(debug=True)
