from flask import Flask, render_template, request, redirect, flash, url_for
from database import database as db
from utils import Field
from config import Config
from forms import LoginForm, RegisterForm, EditProfileForm
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
        #print(form.username.data)
        if data.check_user(form.username.data, form.password.data):
            user = User(form.username.data)
            remember_me = form.remember_me.data
            login_user(user, remember_me)
            return redirect(url_for('index'))
    return render_template('login.jinja', title='Sign In', form=form)


@app.route("/index", methods=["GET", "POST"])
@login_required
def index():
    global searchTerm
    data = db.Database("database/main.db")
    if request.method == "GET":
        fields = data.readall()
        fields_type = fieldCheck(fields)
        user_role = data.get_role(current_user.id)
        return render_template('index.jinja', attributes=attributes, fields=fields, fields_type=fields_type, user=current_user.id, role=user_role)
    else:
        searchTerm = request.get_json()
        return redirect(url_for("attributesSearch"))


@app.route("/register", methods=["GET", "POST"])
@login_required
def register():
    data = db.Database("database/main.db")
    user_role = data.get_role(current_user.id)
    if data.get_role(current_user.id):
        form = RegisterForm()
        if form.validate_on_submit():
            data.add_user(form.username.data, form.password.data, form.role.data)
            return redirect(url_for('dashboard'))
        return render_template('register.jinja', title='Register', form=form, user=current_user.id, role=user_role)
    return redirect(url_for('index'))

@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    data = db.Database("database/main.db")
    if not data.get_role(current_user.id):
        return redirect(url_for('index'))
    users = data.get_all_users()
    users_type = fieldCheck(users)
    user_role = data.get_role(current_user.id)
    return render_template("dashboard.jinja",users_type=users_type, user=current_user.id, users=users, role=user_role)


@app.route("/edituser/<username>", methods=["GET", "POST"])
@login_required
def edituser(username):
    data = db.Database("database/main.db")
    if not (data.get_role(current_user.id) or username == current_user.id):
        return redirect(url_for('index'))
    form = EditProfileForm()
    if form.validate_on_submit():
        data.edit_user(username, form.password.data)
        return redirect(url_for('dashboard'))
    user_role = data.get_role(current_user.id)
    return render_template('editUser.jinja', form=form, user=current_user.id, username=username, role=user_role)


@app.route("/deleteuser/<username>", methods=["GET", "POST"])
@login_required
def deleteuser(username):
    data = db.Database("database/main.db")
    if not data.get_role(current_user.id):
        return redirect(url_for('index'))
    if current_user.id == username:
        return redirect(url_for('dashboard'))
    data.delete_user(username)
    return redirect(url_for('dashboard'))

@app.route("/attributesSearch", methods=["GET", "POST"])
@login_required
def attributesSearch():
    if request.method == "GET":
        return redirect(url_for('index'))
    data = db.Database("database/main.db")
    newfield = {
        "crop": request.form.get("crop"),
        "precrop": request.form.get("precrop"),
        "cycle": request.form.get("cycle"),
        "lime": request.form.get("lime"),
        "fertilizer": request.form.get("fertilizer"),
        "plow": request.form.get("plow"),
        "roll": request.form.get("roll"),
        "status": request.form.get("status"),
    }
    fields = data.read_by_attribute(newfield)
    fields_type = fieldCheck(fields)
    user_role = data.get_role(current_user.id)
    return render_template('index.jinja', attributes=attributes, fields=fields, fields_type=fields_type, user=current_user.id, role=user_role)


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
    user_role = data.get_role(current_user.id)
    if fields is not None:
        return render_template('index.jinja', attributes=attributes, fields=fields, fields_type=fields_type, user=current_user.id, role=user_role)
    else:
        fields = data.readall()
        fields_type = fieldCheck(fields)
        return render_template('index.jinja', attributes=attributes, fields=fields, fields_type=fields_type,
                               notFound="Searchterm not found", user=current_user.id, role=user_role)


@app.route("/add", methods=["GET", "POST"])
@login_required
@cross_origin()
def add():
    data = db.Database("database/main.db")
    user_role = data.get_role(current_user.id)
    if request.method == "GET":
        return render_template('add.jinja', attributes=attributes, user=current_user.id, role=user_role)
    else:
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
    user_role = data.get_role(current_user.id)
    if request.method == "GET":
        fields_type = fieldCheck(fields)
        return render_template('edit.jinja', attributes=attributes, fields=fields, fields_type=fields_type, user=current_user.id, role=user_role)
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
        port=5000,
        debug=True
    )
