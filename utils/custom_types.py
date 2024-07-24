class Field:
    def __init__(self, fieldnumber: int, field_data: dict):
        self.field_data: dict = field_data
        self.fieldnumber: int = fieldnumber
        self.crop: str = field_data["crop"]
        self.precrop: str = field_data["precrop"]
        self.cycle: str = field_data["cycle"]
        self.lime: str = field_data["lime"]
        self.fertilizer: str = field_data["fertilizer"]
        self.plow: str = field_data["plow"]
        self.roll: str = field_data["roll"]
        self.status: str = field_data["status"]
        self.fieldsize: float = field_data["fieldsize"]

    def raw_dict(self):
        return self.field_data

    def __str__(self):
        return f"Field {self.fieldnumber}: {self.field_data}"

    def __len__(self):
        return len(self.field_data)

    def items(self):
        temp = self.field_data
        temp["fieldnumber"] = self.fieldnumber
        return temp.items()


