from flask import Flask
from flask import render_template
import database.database as db


app = Flask(__name__)


@app.route("/", methods=["GET"])
@app.route("/index")
def index():
    user = {'username': 'Miguel'}
    attributes = ["Feldnummer", "Frucht", "Vorfrucht", "Zyklus", "Kalk", "Dünger", "pflügen", "walzen", "Status", "Feldgröße"]
    data = db.Database("../database/main.db")
    testfield = data.readall()

    return render_template('index.jinja', attributes = attributes, testfield = testfield)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True
    )
