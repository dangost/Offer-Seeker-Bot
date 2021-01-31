class SearchSetting:
    def __init__(self, chat_id):
        self.chat_id = chat_id,
        self.name = ""
        self.price = ""
        self.links = []
        self.region = None
        self.cat = None
        self.is_searchable = False

    def to_string(self):
        return f"{self.name}\t{self.price}"
