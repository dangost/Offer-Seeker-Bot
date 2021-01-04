class User:
    def __init__(self, chat_id, key):
        self.chat_id = chat_id
        self.key = key
        self.search_settings = []
        self.reg_step = 0

        # # reg_steps:
        # 0 - starting - choose region
        # 1 - choose cat
        # 2 - choose name
        # 3 - choose price
