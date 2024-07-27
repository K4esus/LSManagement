from flask import Flask, render_template, request, redirect, flash, url_for
from database import database as db
from utils import Field
from config import Config
from forms import LoginForm
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
login = LoginManager()
app.config['SECRET_KEY'] = Config.SECRET_KEY
attributes = ["Feldnummer", "Frucht", "Vorfrucht", "Zyklus", "Kalk", "Dünger", "pflügen", "walzen", "Status",
              "Feldgröße(in ha)"]


# Flask-Login konfigurieren
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# User-Klasse erstellen
class User(UserMixin):
    def __init__(self, username):
        self.id = username


@login_manager.user_loader
def load_user(user_id):
    data = db.Database("database/main.db")
    if data.get_user(user_id):
        return User(user_id)
    return None


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
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    data = db.Database("database/main.db")
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        if data.check_user(form.username.data, form.password.data):
            user = User(form.username.data)
            remember_me = form.remember_me.data
            login_user(user, remember_me)
            return redirect(url_for('index'))
    return render_template('login.jinja', title='Sign In', form=form)


#@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
@login_required
def index():
    global searchTerm
    data = db.Database("database/main.db")
    if request.method == "GET":
        fields = data.readall()
        fields_type = fieldCheck(fields)
        return render_template('index.jinja', attributes=attributes, fields=fields, fields_type=fields_type)
    else:
        searchTerm = request.get_json()
        return redirect(url_for("attributesSearch"))


@app.route("/attributesSearch", methods=["GET", "POST"])
@login_required
def attributesSearch():
    data = db.Database("database/main.db")

    #print(searchTerm)
    fields = data.read_by_attribute(json_to_field(searchTerm["text"]))
    fields_type = fieldCheck(fields)
    return render_template('index.jinja', attributes=attributes, fields=fields, fields_type=fields_type)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/search", methods=["POST"])
@login_required
def search():
    data = db.Database("database/main.db")
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
@login_required
@cross_origin()
def add():
    if request.method == "GET":
        return render_template('add.jinja', attributes=attributes)
    else:
        data = db.Database("database/main.db")
        fieldnumber = request.form.get("fieldnumber")
        newfield = {
            "crop": request.form.get("crop"),
            "precrop": request.form.get("precrop"),
            "cycle": request.form.get("cycle"),
            "lime": request.form.get("lime"),
            "fertilizer": request.form.get("fertilizer"),
            "plow": request.form.get("plow"),
            "roll": request.form.get("roll"),
            "status": request.form.get("status"),
            "fieldsize": request.form.get("fieldsize")
        }
        field = Field(fieldnumber, newfield)
        data.create(field)
        return redirect(url_for('index'))


@app.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
@cross_origin()
def edit(id):
    data = db.Database("database/main.db")
    fields = data.read(id)
    if request.method == "GET":
        fields_type = fieldCheck(fields)
        return render_template('edit.jinja', attributes=attributes, fields=fields, fields_type=fields_type)
    else:
        fieldnumber = fields[0]
        newfield = {
            "crop": request.form.get("crop"),
            "precrop": request.form.get("precrop"),
            "cycle": request.form.get("cycle"),
            "lime": request.form.get("lime"),
            "fertilizer": request.form.get("fertilizer"),
            "plow": request.form.get("plow"),
            "roll": request.form.get("roll"),
            "status": request.form.get("status"),
            "fieldsize": fields[9]
        }
        data.update(fieldnumber, newfield)
        return redirect(url_for('index'))


@app.route("/delete/<int:id>", methods=["POST"])
@login_required
@cross_origin()
def delete(id):
    data = db.Database("database/main.db")
    data.delete(id)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True
    )
