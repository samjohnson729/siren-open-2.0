from flask import render_template
from app import app, db, utils
from app.models import *
import numpy as np

STATISTICS = {
    'score': {
        'label': 'Score',
        'type': 'int',
    },
    'score-to-par': {
        'label': 'Score to Par',
        'type': 'int',
        'formatting_function': utils.format_plus_minus,
    },
    'strokes-gained': {
        'label': 'Strokes Gained',
        'type': 'float',
        'formatting_function': utils.format_plus_minus,
    },
    #'z-score': {
    #    'label': 'Z-Score',
    #    'type': 'float',
    #    'aggregate_function': utils.aggregate_z_score,
    #}
}

def render_leaderboard(params: dict = {}):

    # query all the relevant rounds
    rounds = db.session.query(Round)
    if 'year' in params:
        rounds = rounds.join(Tournament).filter(Tournament.year == params['year'])
    rounds = rounds.all()

    # create a dictionary containing results
    leaderboard = {}
    golfers = []
    courses = []
    years = reversed(sorted([t.year for t in db.session.query(Tournament).all()]))
    for r in rounds:
        g = r.golfer.name
        c = r.layout.course.name

        if g not in golfers: golfers.append(g)
        if c not in courses: courses.append(c)
        if g not in leaderboard: leaderboard[g] = {}
        if c not in leaderboard[g]: leaderboard[g][c] = {s:[] for s in STATISTICS}

        for statistic in STATISTICS:
            value = r.get_statistic(statistic=statistic)
            if value is not None:
                leaderboard[g][c][statistic].append(value)

    # aggregate results accross years and calculate totals for each golfer
    for g in leaderboard:
        totals = {}
        for s, s_data in STATISTICS.items():
            for c in leaderboard[g]:
                leaderboard[g][c][s] = np.mean(leaderboard[g][c][s]) if len(leaderboard[g][c][s]) > 0 else None
            totals_list = [leaderboard[g][c][s] for c in leaderboard[g] if leaderboard[g][c][s] is not None]
            totals_sum = sum(totals_list) if len(totals_list) > 0 else None
            if totals_sum is not None and 'aggregate_function' in s_data:
                totals[s] = s_data['aggregate_function'](**{'golfer': g, 'year': params.get('year')})
            else:
                totals[s] = totals_sum
        leaderboard[g]['total'] = totals

    # format data (decimal places, +/-, etc...)
    for g in leaderboard:
        for s, s_data in STATISTICS.items():
            for c in leaderboard[g]:

                if leaderboard[g][c][s] is None:
                    leaderboard[g][c][s] = ''
                    continue
                elif 'year' in params and s_data['type'] == 'int':
                    leaderboard[g][c][s] = round(leaderboard[g][c][s])
                else:
                    leaderboard[g][c][s] = round(leaderboard[g][c][s], 1)

                if 'formatting_function' in s_data:
                    leaderboard[g][c][s] = s_data['formatting_function'](leaderboard[g][c][s])

    return render_template(
        'stats/leaderboard.html',
        leaderboard=leaderboard,
        golfers=golfers,
        courses=courses,
        years=years,
        statistics_dict=STATISTICS,
        year=params.get('year'),
        statistic=params.get('statistic')
    )

def render_scorecard(params: dict = {}):

    course = params.get('course', 'Fox Run')

    # query all the relevant rounds
    hole_scores = db.session.query(HoleScore).join(Round).join(Layout).join(Course).filter((Course.name == course))
    if 'year' in params:
        hole_scores = hole_scores.join(Tournament).filter(Tournament.year == params['year'])
    hole_scores = hole_scores.all()

    # create a dictionary containing results
    scorecard = {}
    golfers = []
    holes = []
    years = reversed(sorted([t.year for t in db.session.query(Tournament).all()]))
    courses = [c.name for c in db.session.query(Course).all()]
    for hs in hole_scores:
        g = hs.round.golfer.name
        h = hs.hole.number

        if g not in golfers: golfers.append(g)
        if h not in holes: holes.append(h)
        if g not in scorecard: scorecard[g] = {}
        if h not in scorecard[g]: scorecard[g][h] = {s:[] for s in STATISTICS}

        for statistic in STATISTICS:
            value = hs.get_statistic(statistic=statistic)
            if value is not None:
                scorecard[g][h][statistic].append(value)
    
    # aggregate results accross years and calculate totals for each golfer
    for g in scorecard:
        totals = {}
        for s in STATISTICS:
            for h in scorecard[g]:
                scorecard[g][h][s] = np.mean(scorecard[g][h][s]) if len(scorecard[g][h][s]) > 0 else None
            totals_list = [scorecard[g][h][s] for h in scorecard[g] if scorecard[g][h][s] is not None]
            totals[s] = sum(totals_list) if len(totals_list) > 0 else None
        scorecard[g]['total'] = totals

    # format data (decimal places, +/-, etc...)
    for g in scorecard:
        for s, s_data in STATISTICS.items():
            for h in scorecard[g]:

                if scorecard[g][h][s] is None:
                    scorecard[g][h][s] = ''
                    continue
                elif 'year' in params and s_data['type'] == 'int':
                    scorecard[g][h][s] = round(scorecard[g][h][s])
                else:
                    scorecard[g][h][s] = round(scorecard[g][h][s], 1)

                if 'formatting_function' in s_data:
                    scorecard[g][h][s] = s_data['formatting_function'](scorecard[g][h][s])

    return render_template(
        'stats/scorecard.html',
        scorecard=scorecard,
        golfers=golfers,
        courses=courses,
        holes=sorted(holes),
        years=years,
        statistics_dict=STATISTICS,
        year=params.get('year'),
        course=params.get('course'),
        statistic=params.get('statistic')
    )

def render_player(params: dict = {}):

    courses = []
    years = []
    golfers = [g.name for g in db.session.query(Golfer).all()]
    golfer = params.get('golfer', 'Ian Snyder')

    # build summary results
    rounds = db.session.query(Round).join(Golfer).filter(Golfer.name == golfer).all()

    summary = {}
    for r in rounds:
        y = r.tournament.year
        c = r.layout.course.name

        if y not in years:years.append(y)
        if c not in courses:courses.append(c)
        if y not in summary:summary[y] = {}
        if c not in summary[y]:summary[y][c] = {s:None for s in STATISTICS}

        for statistic in STATISTICS:
            value = r.get_statistic(statistic=statistic)
            if value is not None:
                summary[y][c][statistic] = value

    for y in summary:
        totals = {}
        for s in STATISTICS:
            totals_list = [summary[y][c][s] for c in summary[y] if summary[y][c][s] is not None]
            totals[s] = sum(totals_list) if len(totals_list) > 0 else None
        summary[y]['total'] = totals

    for y in summary:
        for s, s_data in STATISTICS.items():
            for c in summary[y]:

                if summary[y][c][s] is None:
                    summary[y][c][s] = ''
                    continue
                elif s_data['type'] == 'int':
                    summary[y][c][s] = round(summary[y][c][s])
                else:
                    summary[y][c][s] = round(summary[y][c][s], 1)

                if 'formatting_function' in s_data:
                    summary[y][c][s] = s_data['formatting_function'](summary[y][c][s])

    # build detail results
    hole_scores = db.session.query(HoleScore).join(Round).join(Golfer).filter(Golfer.name == golfer).all()

    detailed = {}
    for hs in hole_scores:
        c = hs.round.layout.course.name
        y = hs.round.tournament.year
        h = hs.hole.number

        if c not in detailed: detailed[c] = {}
        if y not in detailed[c]: detailed[c][y] = {}
        if h not in detailed[c][y]: detailed[c][y][h] = {s:None for s in STATISTICS}

        for statistic in STATISTICS:
            value = hs.get_statistic(statistic=statistic)
            if value is not None:
                detailed[c][y][h][statistic] = value

    for c in detailed:
        for y in detailed[c]:
            totals = {}
            for s in STATISTICS:
                totals_list = [detailed[c][y][h][s] for h in detailed[c][y] if detailed[c][y][h][s] is not None]
                totals[s] = sum(totals_list) if len(totals_list) > 0 else None
            detailed[c][y]['total'] = totals

    for c in detailed:
        for y in detailed[c]:
            for s, s_data in STATISTICS.items():
                for h in detailed[c][y]:

                    if detailed[c][y][h][s] is None:
                        detailed[c][y][h][s] = ''
                        continue
                    elif s_data['type'] == 'int':
                        detailed[c][y][h][s] = round(detailed[c][y][h][s])
                    else:
                        detailed[c][y][h][s] = round(detailed[c][y][h][s], 1)

                    if 'formatting_function' in s_data:
                        detailed[c][y][h][s] = s_data['formatting_function'](detailed[c][y][h][s])

    return render_template(
        'stats/golfer.html',
        golfer=golfer,
        golfers=golfers,
        courses=courses,
        years=years,
        summary=summary,
        detailed=detailed,
        statistics_dict=STATISTICS,
        statistic=params.get('statistic'),
    )

def render_course(params: dict = {}):

    summary_by_course = {}
    detail_by_course = {}

    for course in db.session.query(Course).all():

        rounds = utils.flatten([[r for r in l.rounds if r.is_completed()] for l in course.layouts])
        holes = utils.flatten([[h for h in l.holes] for l in course.layouts])

        high_score = max([r._get_score() for r in rounds])
        high_rounds = [r for r in rounds if r._get_score() == high_score]
        low_score = min([r._get_score() for r in rounds])
        low_rounds = [r for r in rounds if r._get_score() == low_score]

        easiest_hole = {'hole': None, 'score': np.inf}
        hardest_hole = {'hole': None, 'score': -np.inf}
        for l in course.layouts:
            for h in l.holes:
                average_score = np.mean([hs._get_score_to_par() for hs in h.scores if hs.score is not None])
                if average_score < easiest_hole['score']:
                    easiest_hole = {'hole': h, 'score': average_score}
                if average_score > hardest_hole['score']:
                    hardest_hole = {'hole': h, 'score': average_score}

        detail_by_course[course.name] = {}
        summary_by_course[course.name] = [
            {
                'statistic': 'Low Score',
                'value': low_score,
                'comments': [f'{r.golfer.name} ({r.tournament.year})' for r in low_rounds]
            },
            {
                'statistic': 'High Score',
                'value': high_score,
                'comments': [f'{r.golfer.name} ({r.tournament.year})' for r in high_rounds]
            },
            {
                'statistic': 'Average Score',
                'value': round(np.mean([r._get_score() for r in rounds]), 1)
            },
            {
                'statistic': 'Standard Deviation',
                'value': round(np.std([r._get_score() for r in rounds]), 1)
            },
            {
                'statistic': 'Easiest Hole',
                'value': easiest_hole['hole'].number,
                'comments': [utils.format_plus_minus(round(easiest_hole['score'], 2))]
            },
            {
                'statistic': 'Hardest Hole',
                'value': hardest_hole['hole'].number,
                'comments': [utils.format_plus_minus(round(hardest_hole['score'], 2))]
            }
        ]

        for hole in holes:

            detail_by_course[course.name][hole.number] = {
                'distance': hole.distance,
                'par': hole.par,
                'low': min([hs.score for hs in hole.scores if hs.is_completed()]),
                'average': round(np.mean([hs.score for hs in hole.scores if hs.is_completed()]), 2),
                'high': max([hs.score for hs in hole.scores if hs.is_completed()]),
            }


    return render_template(
        'stats/course.html',
        courses=[c.name for c in db.session.query(Course).all()],
        summary_by_course=summary_by_course,
        detail_by_course=detail_by_course
    )
