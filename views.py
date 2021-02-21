import sys
from flask import render_template, request, redirect, url_for, session
import datetime
import json
import os

from game.character import Character

from game.gamestate import game_state

from game.save import save_game

from game.util import generate_character_avatar
from game.util import get_cover_art_names

def home():
    if request.method == "GET":
        return render_template(
            "home.html",
        )

def game():

    if request.method == "GET":
        return render_template(
            "game.html",
        )

def game_setup():

    cover_art_names = [ url_for("static", filename="cover_arts/" + x) for x in get_cover_art_names()]
    
    if request.method == "GET":
        return render_template(
            "game_setup.html",
            img_names=cover_art_names,
        )

def set_setup_data():

    if request.method == "POST":
        name = request.form['input_game_name']
        num_chars = int(request.form['input_num_chars'])

        game_state.add_setup_data(name, num_chars)

        save_game()
        
        return redirect(url_for('character_creation'))

def add_character():

    if request.method == "POST":

        if game_state.number_of_characters <= len(game_state.characters):
            return "FAIL"

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

def character_creation():

    if request.method == "GET":

        if game_state.number_of_characters <= 0:
            return "FAIL"

        new_char = Character()
        main_skills = [ (key.upper(), val) for key, val in  new_char.main_skills.items() ]
        sub_skills = [[ (mkey.upper(), key.upper(), val) for key, val in  mval.items() ] for mkey, mval in new_char.sub_skills.items()]
        spare_skill_points = [ (key.upper(), val) for key, val in new_char.spare_skill_points.items()]

        return render_template(
            "character_creation.html",
            main_skills=main_skills,
            sub_skills=sub_skills,
            spare_skill_points=spare_skill_points,
        )

def receive_character_avatar():

    data = json.loads(request.data.decode())
    _class = data["class"]
    gender = data["gender"]
    img_str, head_name, body_name = generate_character_avatar(_class, gender)

    return json.dumps( { "img_str": img_str.decode('utf8'), "body_name": body_name, "head_name": head_name } )

