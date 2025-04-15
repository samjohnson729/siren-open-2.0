from flask import request
from app import app
from app.handlers import *

@app.route('/stats')
def stats():
    return render_template('stats/stats.html')

@app.route('/stats/leaderboard', methods=['GET', 'POST'])
def stats_leaderboard():
    return render_leaderboard(params=request.args.to_dict())

@app.route('/stats/scorecard', methods=['GET', 'POST'])
def stats_scorecard():
    return render_scorecard(params=request.args.to_dict())

@app.route('/stats/golfer', methods=['GET', 'POST'])
def stats_player():
    return render_player(params=request.args.to_dict())

@app.route('/stats/course', methods=['GET', 'POST'])
def stats_course():
    return render_course(params=request.args.to_dict())
