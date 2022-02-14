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
    list_of_quotations = []
    request_arguments = []

    for entry in request.args:
        request_arguments.append(entry)

    if 'scene' in request_arguments:
        if 'act' not in request_arguments:
            return jsonify({'Error': 'If searching by scene you must specify an act.'})
        else:
            if len(request_arguments) == 2:
                return jsonify({'quotations': [quotation.to_dict() for quotation in Quotation.query.filter_by(
                    act=request.args['act'],
                    scene=request.args['scene']).all()]}
                               )
            elif len(request_arguments) > 2:
                if 'character' in request_arguments:
                    character_quotations = [quotation for quotation in Quotation.query.filter_by(
                        act=request.args['act'],
                        scene=request.args['scene'],
                        character=request.args['character']).all()]

                    for entry in character_quotations:
                        list_of_quotations.append(entry)

                    if 'theme' not in request_arguments:
                        return jsonify({'quotations': [quotation.to_dict() for quotation in list_of_quotations]})
                    else:
                        for entry in list_of_quotations:
                            if request.args['theme'] != entry.theme_1 and entry.theme_2 != request.args[
                                'theme'] and entry.theme_3 != request.args['theme']:
                                list_of_quotations.remove(entry)

                        return jsonify({'quotations': [quotation.to_dict() for quotation in list_of_quotations]})

                else:
                    # and if you get a theme... we need to add to the list_of_quotations throughout this process.
                    pass

    return jsonify({'hello!': 'You seem to have got through. Well done.'})


if __name__ == "__main__":
    app.run(debug=True)
