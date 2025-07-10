from flask import render_template
from app import db
from app.models import *

CURRENT_YEAR = 2025

def render_live_summary(course: str):
    tournament = db.session.query(Tournament).filter(Tournament.year == CURRENT_YEAR).first()
    all_courses = sorted(set([r.layout.course.name for r in tournament.rounds]))

    hole_scores = (
        db.session.query(HoleScore)
        .join(Hole)
        .join(Round)
        .join(Layout)
        .join(Course)
        .join(Tournament)
    ).filter(
        (Course.name == course) &
        (Tournament.year == CURRENT_YEAR)
    ).all()
    num_holes = len(hole_scores[0].round.layout.holes)
    scores = {}
    for hs in hole_scores:
        if hs.hole.number not in scores:
            scores[hs.hole.number] = {}
        scores[hs.hole.number][hs.round.golfer.name] = {'par': hs.hole.par, 'score': hs.score}

    score_summary = {}
    for hs in hole_scores:
        if hs.round.golfer.name not in score_summary:
            score_summary[hs.round.golfer.name] = {'par': 0, 'total': 0}
        if hs.score:
            score_summary[hs.round.golfer.name]['par'] += int(hs.hole.par)
            score_summary[hs.round.golfer.name]['total'] += int(hs.score)

    return render_template(
        'live/live_summary.html',
        all_courses=all_courses,
        course=course,
        num_holes=num_holes,
        scores=scores,
        score_summary=score_summary
    )

def render_live_detail(course: str, hole: int):

    tournament = db.session.query(Tournament).filter(Tournament.year == CURRENT_YEAR).first()
    all_courses = sorted(set([r.layout.course.name for r in tournament.rounds]))

    hole_scores = (
        db.session.query(HoleScore)
        .join(Hole)
        .join(Round)
        .join(Layout)
        .join(Course)
        .join(Tournament)
    ).filter(
        (Course.name == course) &
        (Tournament.year == CURRENT_YEAR) &
        (Hole.number == int(hole))
    ).all()
    num_holes = len(hole_scores[0].round.layout.holes)
    hole = hole_scores[0].hole

    return render_template(
        'live/live_detail.html',
        all_courses=all_courses,
        course=course,
        num_holes=num_holes,
        hole=hole,
        hole_scores=hole_scores
    )
