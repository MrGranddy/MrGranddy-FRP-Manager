import sys
from flask import render_template, request, redirect, url_for, session
import datetime
import json
import os
import numpy as np

from game.character import Character

from game.gamestate import game_state

from game.save import save_game, load_game

from game.util import generate_character_avatar, generate_avatar_icon, get_character_avatar
from game.util import get_cover_art_names
from game.util import get_character_by_name

def home():
    return render_template( "home.html", game_loaded=game_state.game_name != "")

def game():

    if game_state.number_of_characters != len(game_state.characters):
        return redirect(url_for("character_creation"))

    icons = [ generate_avatar_icon(character.head_name, character.body_name).decode("utf-8")
                for character in game_state.characters ]

    return render_template(
        "game.html",
        characters=game_state.characters,
        icons=icons,
    )

def game_setup():

    cover_art_path = url_for( "static", filename="cover_arts/" + np.random.choice(get_cover_art_names()) )
    
    return render_template(
        "game_setup.html",
        cover_art_path=cover_art_path,
    )

def character_creation():

    if request.method == "GET":

        if game_state.number_of_characters == len( game_state.characters ):
            return redirect(url_for("game"))
        elif game_state.number_of_characters <= 0:
            return redirect(url_for("home"))

        new_char = Character()
        main_skills = [ (key.upper(), val) for key, val in  new_char.main_skills.items() ]
        sub_skills = [[ (mkey.upper(), key.upper(), val) for key, val in  mval.items() ] for mkey, mval in new_char.sub_skills.items()]
        spare_skill_points = [ (key.upper(), val) for key, val in new_char.spare_skill_points.items()]

        return render_template(
            "character_page.html",
            main_skills=main_skills,
            sub_skills=sub_skills,
            spare_skill_points=spare_skill_points,
            button_state=int(game_state.number_of_characters - 1 != len(game_state.characters)),
            character_name=None,
            character_class=None,
            character_gender=None,
            character_avatar=None,
        )

def character_page(name):

    character = get_character_by_name(name)

    if character == None:
        return redirect(url_for("game"))

    main_skills = [ (key.upper(), val) for key, val in  character.main_skills.items() ]
    sub_skills = [[ (mkey.upper(), key.upper(), val) for key, val in  mval.items() ] for mkey, mval in character.sub_skills.items()]
    spare_skill_points = [ (key.upper(), val) for key, val in character.spare_skill_points.items()]

    return render_template(
        "character_page.html",
        main_skills=main_skills,
        sub_skills=sub_skills,
        spare_skill_points=spare_skill_points,
        button_state=2,
        character_name=name,
        character_class=character._class.capitalize(),
        character_gender=character.gender.capitalize(),
        character_avatar=get_character_avatar(character.head_name, character.body_name).decode("utf-8"),
    )

def character_level_up(name):
    
    c = get_character_by_name(name)
    c.level_up()

    save_game()

    return redirect(url_for("game"))

def load_game_view():

    if request.method == "GET":
        return render_template( "load.html" )

    elif request.method == "POST":

        file_name = os.path.split( request.form["load-file-input"] )[-1]
        load_game( file_name )
        return redirect(url_for('character_creation'))

# POST
def receive_character_avatar():

    data = json.loads(request.data.decode())
    _class = data["class"]
    gender = data["gender"]
    img_str, head_name, body_name = generate_character_avatar(_class, gender)

    return json.dumps( { "img_str": img_str.decode('utf8'), "body_name": body_name, "head_name": head_name } )

# POST
def set_setup_data():

    name = request.form['input_game_name']
    num_chars = int(request.form['input_num_chars'])

    game_state.add_setup_data(name, num_chars)

    save_game()
    
    return redirect(url_for('character_creation'))

# POST
def add_character():

    new_char = Character()
    status = new_char.character_setup(request.form)

    if status != 0:
        return "FAIL"

    game_state.add_character(new_char)
    save_game()

    if game_state.number_of_characters == len(game_state.characters):
        return redirect(url_for("game"))
    else:
        return redirect(url_for('character_creation'))

# POST
def update_character():

    name = request.form["input_name_update"]

    c = get_character_by_name(name)

    if c == None:
        return redirect(url_for("game"))

    status = c.character_update(request.form)

    if status != 0:
        return "FAIL"

    save_game()

    return redirect(url_for("game"))
