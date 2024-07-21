import database as db
from utils import Field

field_data = {"crop":"LEER",
         "precrop":"WEIZEN",
         "cycle":"H1.1",
         "lime":"NEIN",
         "fertilizer":"NEIN",
         "plow":"NEIN",
         "roll":"NEIN",
         "status":"SCWARZ",
         "fieldsize":37.41
}


def test_db():
    testfield = Field(999, field_data)
    data = db.Database("../database/main.db")
    data.create(testfield)
    print(data.read(999))
    field_data["crop"] = "WEIZEN"
    data.update(999, field_data)
    print(data.read(999))
    data.delete(999)


if __name__ == '__main__':
    test_db()