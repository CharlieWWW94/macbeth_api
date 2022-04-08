from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import ast

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

    def to_dict(self):
        entry_dict = {}

        for column in self.__table__.columns:
            entry_dict[column.name] = getattr(self, column.name)

        return entry_dict


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


# Get all quotations...

@app.route("/all", methods=["GET"])
def all_quotations():
    all_quotations_dict = {"quotations": []}

    for entry in Quotation.query.all():
        print(entry.to_dict())
        all_quotations_dict["quotations"].append(entry.to_dict())

    return jsonify(all_quotations_dict)


@app.route("/search", methods=["GET"])
def search():
    every_quotation = []
    quotations_to_return = []

    requests_as_dict = request.args.to_dict()
    theme = []
    request_dict_keys = [key for key in requests_as_dict.keys()]

    if 'id' in request_dict_keys:
        id_list = request.args.getlist('id')
        for given_id in id_list:
            quotations_to_return.append(Quotation.query.filter_by(id=given_id).first().to_dict())
        return jsonify({'quotations': quotations_to_return})

    else:

        for key in request_dict_keys:
            if requests_as_dict[key] == 'All':
                del requests_as_dict[key]
            elif key == 'theme':
                theme.append(requests_as_dict[key])
                del requests_as_dict[key]
        if requests_as_dict:
            for entry in Quotation.query.filter_by(**requests_as_dict):
                every_quotation.append(entry.to_dict())
        else:
            for entry in Quotation.query.all():
                every_quotation.append(entry.to_dict())
        if len(theme) != 0:
            for entry in every_quotation:
                if entry['theme_1'] == theme[0] or entry['theme_2'] == theme[0] or entry['theme_3'] == theme[0]:
                    quotations_to_return.append(entry)
            return jsonify({'quotations': quotations_to_return})
        else:
            return jsonify({'quotations': every_quotation})


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5001)
