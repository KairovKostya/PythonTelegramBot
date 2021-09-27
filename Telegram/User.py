class User:
    id: int
    first_name: str
    last_name: str

    def __init__(self, id=0, fn="", ln=""):
        self.id = id
        self.first_name = fn
        self.last_name = ln