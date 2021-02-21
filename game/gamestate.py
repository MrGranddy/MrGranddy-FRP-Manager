import datetime

class GameState:
    def __init__(self):

        self.game_name = ""
        self.save_name = ""
        self.number_of_characters = 0
        self.characters = []
        self.creation_date = None

    def add_setup_data(self, game_name, number_of_characters):

        self.game_name = game_name
        self.save_name = "_".join(game_name.lower().split()) + ".json"
        self.number_of_characters = number_of_characters
        self.create_date = datetime.datetime.now()
        self.characters = []

    def add_character(self, character):
        self.characters.append( character )

game_state = GameState()
