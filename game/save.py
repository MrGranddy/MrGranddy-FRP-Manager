import os
import json
import datetime

from .character import Character
from .gamestate import game_state

def dictify_characters(characters):

    dictified_characters = []

    for character in characters:

        character_dict = {
            "character_name": character.character_name,
            "level": character.level,
            "hp": character.hp,
            "spare_skill_points": character.spare_skill_points,
            "main_skills": character.main_skills,
            "sub_skills": character.sub_skills,
            "head_name": character.head_name,
            "body_name": character.body_name,
            "class": character._class,
            "gender": character.gender,
        }

        dictified_characters.append( character_dict )

    return dictified_characters

def dedictify_characters(characters):

    dedictified_characters = []

    for character in characters:

        c = Character()

        c.character_name = character["character_name"]
        c.level = character["level"]
        c.hp = character["hp"]
        c.spare_skill_points = character["spare_skill_points"]
        c.main_skills = character["main_skills"]
        c.sub_skills = character["sub_skills"]
        c.head_name = character["head_name"]
        c.body_name = character["body_name"]
        c._class = character["class"]
        c.gender = character["gender"]

        dedictified_characters.append(c)

    return dedictified_characters


def save_game():

    save_file = {
        "game_name": game_state.game_name,
        "save_name": game_state.save_name,
        "number_of_characters": game_state.number_of_characters,
        "characters": dictify_characters( game_state.characters ),
        "creation_date": str(game_state.create_date),
    }

    with open( os.path.join("game", "saves", save_file["save_name"]), "w") as f:
        json.dump(save_file, f)

def load_game(save_name):

    with open( os.path.join("game", "saves", save_name), "r") as f:
        save_file = json.load(f)

    game_state.game_name = save_file["game_name"]
    game_state.save_name = save_file["save_name"]
    game_state.number_of_characters = save_file["number_of_characters"]
    game_state.characters = dedictify_characters( save_file["characters"] )
    game_state.create_date = datetime.datetime.fromisoformat(save_file["creation_date"])