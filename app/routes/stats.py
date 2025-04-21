from flask import request
from app import app
from app.handlers import *

@app.route('/stats/leaderboard', methods=['GET', 'POST'])
def stats_leaderboard():
    return render_leaderboard(params=request.args.to_dict())

@app.route('/stats/scorecard', methods=['GET', 'POST'])
def stats_scorecard():
    return render_scorecard(params=request.args.to_dict())

@app.route('/stats/breakdown', methods=['GET', 'POST'])
def stats_breakdown():
    return render_breakdown(params=request.args.to_dict())

@app.route('/stats/golfer', methods=['GET', 'POST'])
def stats_golfer():
    return render_golfer(params=request.args.to_dict())

@app.route('/stats/course', methods=['GET', 'POST'])
def stats_course():
    return render_course(params=request.args.to_dict())
