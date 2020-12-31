class Item:
    def __init__(self, name, photo, price, link):
        self.name = name
        self.photo = photo
        self.price = price
        self.link = link

    def to_string(self):
        return f"{self.name}\n{self.price}\n{self.link}"
