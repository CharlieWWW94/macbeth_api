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
    request_arguments = []
    every_quotation = []
    quotations_to_return = []

    for entry in request.args:
        request_arguments.append(entry)

    if 'act' in request_arguments:
        if request.args['act'] == 'All':
            request_arguments.remove('act')
        else:
            for entry in Quotation.query.filter_by(act=request.args['act']).all():
                every_quotation.append(entry)

    if 'scene' in request_arguments:
        if request.args['scene'] == 'All':
            request_arguments.remove('scene')
        else:
            for entry in Quotation.query.filter_by(scene=request.args['scene']).all():
                every_quotation.append(entry)

    if 'character' in request_arguments:
        if request.args['character'] == 'All':
            request_arguments.remove('character')
        else:
            for entry in Quotation.query.filter_by(character=request.args['character']).all():
                every_quotation.append(entry)

    if 'theme' in request_arguments:
        if request.args['theme'] == 'All':
            request_arguments.remove('theme')
        else:
            for entry in Quotation.query.filter_by(theme_1=request.args['theme']).all():
                every_quotation.append(entry)
            for entry in Quotation.query.filter_by(theme_2=request.args['theme']).all():
                every_quotation.append(entry)
            for entry in Quotation.query.filter_by(theme_3=request.args['theme']).all():
                every_quotation.append(entry)

    if len(every_quotation) > 0:
        for entry in every_quotation:
            if entry not in quotations_to_return and every_quotation.count(entry) == len(request_arguments):
                quotations_to_return.append(entry)
    else:
        return jsonify({'quotations': [entry.to_dict() for entry in Quotation.query.all()]})

    return jsonify({'quotations': [entry.to_dict() for entry in quotations_to_return]})


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5001)
