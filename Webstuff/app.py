from flask import Flask, render_template, request, redirect, flash, url_for
import database.database as db
from utils import Field
from config import Config
from forms import LoginForm
from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)
login = LoginManager()
app.config['SECRET_KEY'] = Config.SECRET_KEY
attributes = ["Feldnummer", "Frucht", "Vorfrucht", "Zyklus", "Kalk", "Dünger", "pflügen", "walzen", "Status",
              "Feldgröße(in ha)"]


def json_to_field(json: dict) -> Field:
    fieldnumber = json["fieldnumber"]
    newFieldData = {
        "crop": json["crop"],
        "precrop": json["precrop"],
        "cycle": json["cycle"],
        "lime": json["lime"],
        "fertilizer": json["fertilizer"],
        "plow": json["plow"],
        "roll": json["roll"],
        "status": json["status"],
        "fieldsize": json["fieldsize"],
    }
    return Field(fieldnumber, newFieldData)


def fieldCheck(fields) -> bool:
    if type(fields) == list:
        return True
    elif type(fields) == tuple:
        return False
    else:
        TypeError("Database return is funky")


@app.route("/", methods=["GET", "POST"])
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.jinja', title='Sign In', form=form)

#@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
    global searchTerm
    data = db.Database("../database/main.db")
    if request.method == "GET":
        fields = data.readall()
        fields_type = fieldCheck(fields)
        return render_template('index.jinja', attributes=attributes, fields=fields, fields_type=fields_type)
    else:
        searchTerm = request.get_json()
        return redirect(url_for("attributesSearch"))


@app.route("/attributesSearch", methods=["GET", "POST"])
def attributesSearch():
    data = db.Database("../database/main.db")

    #print(searchTerm)
    fields = data.read_by_attribute(json_to_field(searchTerm["text"]))
    fields_type = fieldCheck(fields)
    return render_template('index.jinja', attributes=attributes, fields=fields, fields_type=fields_type)


@app.route("/search", methods=["POST"])
def search():
    data = db.Database("../database/main.db")
    search_query = request.form["search_query"]
    fields = data.read(search_query)
    fields_type = fieldCheck(fields)
    if fields is not None:
        return render_template('index.jinja', attributes=attributes, fields=fields, fields_type=fields_type)
    else:
        fields = data.readall()
        fields_type = fieldCheck(fields)
        return render_template('index.jinja', attributes=attributes, fields=fields, fields_type=fields_type,
                               notFound="Searchterm not found")


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template("add.jinja", attributes=attributes)
    else:
        data = db.Database("../database/main.db")
        #print(request.get_json())
        newField = request.get_json()
        data.create(json_to_field(newField["text"]))
        return redirect("index", code=302)


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    data = db.Database("../database/main.db")
    if request.method == "GET":
        fields = data.read(id)
        fields_type = fieldCheck(fields)
        return render_template('edit.jinja', attributes=attributes, fields=fields, fields_type=fields_type)
    else:
        editField = request.get_json()
        #print(editField["text"])
        #print(len(editField["text"]))
        if len(editField["text"]) == 10:
            editField = json_to_field(editField["text"])
            data.update(editField.fieldnumber, editField.raw_dict())
        else:
            data.delete(editField["text"]["fieldnumber"])

        return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True
    )
