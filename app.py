from flask import Flask, abort
from flask import render_template, request, jsonify, make_response
from scrap_reddit import get_goals_scored

app = Flask(__name__)
@app.route("/")
def main_page():
    goals = get_goals_scored()
    return render_template('index.html', goals=goals)