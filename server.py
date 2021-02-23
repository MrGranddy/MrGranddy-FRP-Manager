from flask import Flask
import sys
import views

def create_app():
    app = Flask(__name__, static_folder="static")

    app.add_url_rule( "/", view_func=views.home, methods=["GET"] )
    app.add_url_rule( "/game", view_func=views.game, methods=["GET"])
    app.add_url_rule( "/game_setup", view_func=views.game_setup, methods=["GET"] )
    app.add_url_rule( "/character_creation", view_func=views.character_creation, methods=["GET"] )
    app.add_url_rule( "/character/<name>", view_func=views.character_page, methods=["GET"] )
    app.add_url_rule( "/character_level_up/<name>", view_func=views.character_level_up, methods=["GET"] )

    app.add_url_rule( "/load_game", view_func=views.load_game_view, methods=["GET", "POST"] )

    app.add_url_rule( "/receive_character_avatar", view_func=views.receive_character_avatar, methods=["POST"] )
    app.add_url_rule( "/set_setup_data", view_func=views.set_setup_data, methods=["POST"] )
    app.add_url_rule( "/add_character", view_func=views.add_character, methods=["POST"] )
    app.add_url_rule( "/update_character", view_func=views.update_character, methods=["POST"] )

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
