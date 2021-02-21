import os
import json

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
        }

        dictified_characters.append( character_dict )

    return dictified_characters



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
