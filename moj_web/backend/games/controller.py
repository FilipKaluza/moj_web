from flask import Blueprint, render_template

games = Blueprint("games", __name__) 

@games.route('/games/')
def view_gameslist():
    return render_template("games/chore_door.jinja")

@games.route('/games/choredoor/')
def play_choredoor():
    return render_template("games/chore_door.jinja")