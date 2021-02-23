import os
import numpy as np
import json
import matplotlib.pyplot as plt
from PIL import Image

import base64
from io import BytesIO

from .gamestate import game_state

heads_dir = os.path.join( "static", "avatar", "head" )
bodies_dir = os.path.join( "static", "avatar", "body" )
with open( os.path.join( "static", "avatar", "body_coords.json" ), "r" ) as f:
    body_coords = json.load(f)
male_heads = ["devlet", "efe", "idris_usta", "mali", "ronaldinho", "sabri", "ulug", "yhs", "sahin"]
female_heads = ["deniz", "hannah", "meral", "nevsin", "muge", "dany", "aleyna"]

def generate_character_avatar(_class, gender):

    if gender == "male" or gender == "female":
        body_name = gender + "_" + _class + ".png"
    else:
        body_name = np.random.choice(["male", "female"]) + "_" + _class + ".png"

    if gender == "male":
        head_name = np.random.choice(male_heads) + ".png"
    elif gender == "female":
        head_name = np.random.choice(female_heads) + ".png"
    else:
        head_name = np.random.choice(female_heads + male_heads) + ".png"

    body_coord = body_coords[ body_name ]
    head_shape = ( body_coord[1] - body_coord[0], body_coord[3] - body_coord[2] )
    left, right, top, bottom = body_coord

    head_img = np.array( Image.open( os.path.join( heads_dir, head_name ) ).resize(head_shape) )
    body_img = np.array( Image.open( os.path.join( bodies_dir, body_name ) ).convert("RGBA") )
    body_img[ top:bottom, left:right, : ][head_img[:,:,3] != 0] = head_img[head_img[:,:,3] != 0]

    body_img = Image.fromarray(body_img)

    w, h = body_img.size
    min_len = np.min([w,h])
    ratio = 600 / min_len
    body_img = body_img.resize((int(w*ratio), int(h*ratio)))

    buffered = BytesIO()
    body_img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue())

    return ( img_str, head_name, body_name )

def generate_avatar_icon(head_name, body_name):

    body_coord = body_coords[ body_name ]
    head_shape = ( body_coord[1] - body_coord[0], body_coord[3] - body_coord[2] )
    left, right, top, bottom = body_coord

    head_img = np.array( Image.open( os.path.join( heads_dir, head_name ) ).resize(head_shape) )
    body_img = np.array( Image.open( os.path.join( bodies_dir, body_name ) ).convert("RGBA") )
    body_img[ top:bottom, left:right, : ][head_img[:,:,3] != 0] = head_img[head_img[:,:,3] != 0]
    icon = Image.fromarray(body_img[ top:bottom, left:right, : ])

    buffered = BytesIO()
    icon.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue())

    return img_str

def get_character_avatar(head_name, body_name):

    body_coord = body_coords[ body_name ]
    head_shape = ( body_coord[1] - body_coord[0], body_coord[3] - body_coord[2] )
    left, right, top, bottom = body_coord

    head_img = np.array( Image.open( os.path.join( heads_dir, head_name ) ).resize(head_shape) )
    body_img = np.array( Image.open( os.path.join( bodies_dir, body_name ) ).convert("RGBA") )
    body_img[ top:bottom, left:right, : ][head_img[:,:,3] != 0] = head_img[head_img[:,:,3] != 0]
    body_img = Image.fromarray(body_img)

    w, h = body_img.size
    min_len = np.min([w,h])
    ratio = 600 / min_len
    body_img = body_img.resize((int(w*ratio), int(h*ratio))) 

    buffered = BytesIO()
    body_img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue())

    return img_str

def get_cover_art_names():
    return os.listdir( os.path.join("static", "cover_arts") )

def get_character_by_name(name):

    for character in game_state.characters:
        if character.character_name == name:
            return character

    return None