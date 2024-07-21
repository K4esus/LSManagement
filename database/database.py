import sqlite3

from utils import Field


class Database:
    def __init__(self, path):
        self.path = path
        self.conn: sqlite3.Connection = sqlite3.connect(path)
        self.cursor: sqlite3.Cursor = self.conn.cursor()

    def setup(self):
        cursor = self.conn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS felddaten "
            "(fieldnumber INTEGER PRIMARY KEY, crop TEXT,precrop TEXT,cycle TEXT,lime TEXT,"
            "fertilizer TEXT,plow TEXT,roll TEXT,status TEXT,fieldsize REAL)"
        )

    def create(self, field: Field):
        self.cursor.execute("INSERT INTO felddaten VALUES (?,?,?,?,?,?,?,?,?,?)",
                            (
                                field.fieldnumber,
                                field.crop,
                                field.precrop,
                                field.cycle,
                                field.lime,
                                field.fertilizer,
                                field.plow,
                                field.roll,
                                field.status,
                                field.fieldsize)
                            )
        self.conn.commit()

    def read(self, fieldnumber: int):
        return self.cursor.execute("SELECT * FROM felddaten WHERE fieldnumber=?",
                                   (fieldnumber,)).fetchone()

    def readall(self):
        return self.cursor.execute("SELECT * FROM felddaten").fetchall()

    def minimize_field(self, field: Field):
        minimized = []
        for key, value in field.items():
            if value != "":
                minimized.append((key, value))

        return minimized

    def read_by_attribute(self, field: Field):
        search = ""
        counter = 0
        mini = self.minimize_field(field)
        for key, value in mini:
            counter += 1
            if counter == len(mini):
                search += f"{key}='{value}' "
            else:
                search += f"{key}='{value}' AND "
        if len(search) > 0:
            return self.cursor.execute("SELECT * FROM felddaten WHERE " + search).fetchall()
        else:
            return self.readall()

    """
            :param fieldnumber: primary key, defines what field we update
            :param variable: stores the data of the field,
                             none = no update, value = update
                             crop: what crop is on the field
                             precrop: what previous crop was on the field
                             cycle: in what fruitcycle is this field
                             lime: JA = dont need lime NEIN = needs lime
                             fertilizer: JA = dont need fertilizer NEIN = needs fertilizer
                             plow: JA = dont need plow NEIN = needs plow
                             roll: JA = dont need roll NEIN = needs roll
                             status: what happens on the field
                             fieldsize: size of the field

            :return:
            """

    def update(
            self,
            fieldnumber: int,
            variable: dict
    ):
        for key, value in variable.items():
            if value is not None:
                self.cursor.execute(f"UPDATE felddaten SET '{key}'=? WHERE fieldnumber=?", (value, fieldnumber))
        self.conn.commit()

    def delete(self, fieldnumber: int):
        self.cursor.execute("Delete from felddaten WHERE fieldnumber=?", (fieldnumber,))
        self.conn.commit()