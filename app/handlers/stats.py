from flask import render_template
from sqlalchemy import func
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

def build_table(
    table_id:str,
    objects:list,
    row_attrs:list[str],
    col_attrs:list[str],
    year:int = None,
    statistic_key:str = 'score',
    total_column:bool = False,
    total_row:bool = False
):
    
    statistic = STATISTICS.get(statistic_key)
        
    match row_attrs[-2:]:
        case ['tournament', 'year']:
            top_left = 'Year'
        case ['hole', 'number']:
            top_left = '#'
        case ['golfer', 'name']:
            top_left = 'Golfer'
        case _:
            top_left = ''
    
    rows = []
    columns = []
    data = {}
    for o in objects:
        
        x, y = o, o
        for attr in row_attrs: x = getattr(x, attr)
        for attr in col_attrs: y = getattr(y, attr)
        
        if row_attrs[-1] == 'year':
            year = x
        elif col_attrs[-1] == 'year':
            year = y
        
        # transform golfer name into initials
        if row_attrs[-2:] == ['golfer', 'name']: x = ''.join([a[0] for a in x.split(' ')])
        if col_attrs[-2:] == ['golfer', 'name']: y = ''.join([a[0] for a in y.split(' ')])
        
        if x not in rows: rows.append(x)
        if y not in columns: columns.append(y)
        if x not in data: data[x] = {}
        if y not in data[x]: data[x][y] = []
        value = o.get_statistic(statistic_key)
        if (value := o.get_statistic(statistic_key)) is not None:
            data[x][y].append(value)
        
    for x in data:
        for y in data[x]:
            data[x][y] = np.mean(data[x][y]) if len(data[x][y]) > 0 else None
        if total_column:
            values = [v for v in data[x].values() if v is not None]
            data[x]['Σ'] = sum(values) if len(values) > 0 else None
    
    if total_column:
        columns.append('Σ')
    if total_row:
        data['Total'] = {}
        for c in columns:
            values = [data[x][c] for x in data if x != 'Total' and data[x][c] is not None]
            data['Total'][c] = sum(values) if len(values) > 0 else None
    
    for x in data:
        for y in data[x]:

            if data[x][y] is None:
                data[x][y] = ''
                continue
            elif year and statistic['type'] == 'int':
                data[x][y] = round(data[x][y])
            else:
                data[x][y] = round(data[x][y], 1)

            if 'formatting_function' in statistic:
                data[x][y] = statistic['formatting_function'](data[x][y])
        
    return render_template(
        'table.html',
        table_id=table_id,
        columns=columns,
        rows=rows,
        data=data,
        top_left=top_left,
        total_row=total_row
    )
    
def build_filter_buttons(
    year:int=False,
    course:str=False,
    golfer:bool=False,
    statistic:str=False,
    include_all_years:bool=False,
    include_all_courses:bool=False,
    include_all_golfers:bool=False,
):
    prefix = '<div style="display: flex;" id="filters">\n'
    suffix = '\n</div>'
    
    output = []
    
    if year is not False:
        output.append(render_template(
            'stats/year_dropdown.html',
            years=sorted([t.year for t in db.session.query(Tournament).all()])[::-1],
            year=year,
            include_all_years=include_all_years
        ))
        
    if course is not False:
        output.append(render_template(
            'stats/course_dropdown.html',
            courses=[c.name for c in db.session.query(Course).all()],
            course=course,
            include_all_courses=include_all_courses
        ))
        
    if golfer is not False:
        output.append(render_template(
            'stats/golfer_dropdown.html',
            golfers=[g.name for g in db.session.query(Golfer).all()],
            golfer=golfer,
            include_all_golfers=include_all_golfers
        ))
        
    if statistic is not False:
        output.append(render_template(
            'stats/statistic_dropdown.html',
            statistics_dict=STATISTICS,
            statistic_key=statistic        ))
        
    return prefix + '\n'.join(output) + suffix

def build_course_tabs():
    return render_template(
        'stats/course_tabs.html',
        courses=[c.name for c in db.session.query(Course).all()]
    )

def render_leaderboard(params: dict = {}):
    
    year = params.get('year')
    statistic_key = params.get('statistic', 'score')
    
    filter_buttons = build_filter_buttons(year=year, statistic=statistic_key, include_all_years=True)
    
    objects = db.session.query(Round)
    if year: objects = objects.join(Tournament).filter(Tournament.year == year)
    objects = objects.all()
    
    table = build_table(
        table_id='stats-leaderboard',
        objects=objects,
        row_attrs=['golfer', 'name'],
        col_attrs=['layout', 'course', 'name'],
        year=year,
        statistic_key=statistic_key,
        total_column=True
    )

    return render_template(
        'stats/leaderboard.html',
        filter_buttons=filter_buttons,
        table=table
    )

def render_scorecard(params: dict = {}):

    course = params.get('course', 'Fox Run')
    year = params.get('year')
    statistic_key = params.get('statistic', 'score')
    
    filter_buttons = build_filter_buttons(
        year=year,
        course=course,
        statistic=statistic_key,
        include_all_years=True
    )

    # query all the relevant rounds
    hole_scores = db.session.query(HoleScore).join(Round).join(Layout).join(Course).filter((Course.name == course))
    if year: hole_scores = hole_scores.join(Tournament).filter(Tournament.year == year)
    hole_scores = hole_scores.all()
    
    table = build_table(
        table_id='stats-scorecard',
        objects=hole_scores,
        row_attrs=['hole', 'number'],
        col_attrs=['round', 'golfer', 'name'],
        year=year,
        statistic_key=statistic_key,
        total_row=True
    )

    return render_template(
        'stats/scorecard.html',
        filter_buttons=filter_buttons,
        table=table
    )

def render_breakdown(params: dict = {}):
    
    year = params.get('year')
    course = params.get('course')
    golfer = params.get('golfer')
    
    filter_buttons = build_filter_buttons(
        year=year,
        course=course,
        golfer=golfer,
        include_all_years=True,
        include_all_courses=True,
        include_all_golfers=True
    )
    
    hole_scores = db.session.query(HoleScore).all()
    if year:
        hole_scores = [hs for hs in hole_scores if hs.round.tournament.year == int(year)]
    if course:
        hole_scores = [hs for hs in hole_scores if hs.round.layout.course.name == course]
    if golfer:
        hole_scores = [hs for hs in hole_scores if hs.round.golfer.name == golfer]
    hole_scores = [hs._get_score_to_par() for hs in hole_scores if hs.is_completed()]
    
    breakdown = {
        'Eagle': sum([hs < -1 for hs in hole_scores]),
        'Birdie': hole_scores.count(-1),
        'Par': hole_scores.count(0),
        'Bogey': hole_scores.count(1),
        'Double Bogey': hole_scores.count(2),
        'Triple+ Bogey': sum([hs > 2 for hs in hole_scores])
    }
    
    return render_template(
        'stats/breakdown.html',
        filter_buttons=filter_buttons,
        breakdown=breakdown
    )

def render_golfer(params: dict = {}):
    
    golfer = params.get('golfer', 'Ian Snyder')
    statistic_key = params.get('statistic', 'score')
    
    filter_buttons = build_filter_buttons(
        golfer=golfer,
        statistic=statistic_key
    )
    
    # build profile
    g = db.session.query(Golfer).filter(Golfer.name == golfer).first()
    profile = {
        'First Tournament': g.get_first_tournament(),
        'Number of Tournaments': g.get_number_of_tournaments(),
        'Tournament Wins': g.get_tournament_wins(),
        'Event Wins': g.get_event_wins(),
        'Total Holes': g.get_total_holes(),
        'Total Strokes': g.get_total_strokes(),        
    }
    
    # get radar skill breakdown values
    radar_data = g.get_radar_data()
    
    # build summary table
    rounds = db.session.query(Round).join(Golfer).filter(Golfer.name == golfer).all()
    summary_table = build_table(
        table_id='stats-golfer-summary',
        objects=rounds,
        row_attrs=['tournament', 'year'],
        col_attrs=['layout', 'course', 'name'],
        statistic_key=statistic_key,
        total_column=True
    )
    
    # course tabs
    course_tabs = build_course_tabs()

    # build detail results
    detail_tables = []
    for i, course in enumerate(db.session.query(Course).all()):
        hole_scores = (
            db.session.query(HoleScore)
            .join(Round)
            .join(Golfer)
            .join(Layout)
            .join(Course)
            .filter((Golfer.name == golfer) & (Course.name == course.name))
        ).all()

        detail_tables.append(build_table(
            table_id=f'stats-golfer-detail-{i}',
            objects=hole_scores,
            row_attrs=['hole', 'number'],
            col_attrs=['round', 'tournament', 'year'],
            statistic_key=statistic_key,
            total_row=True
        ))

    return render_template(
        'stats/golfer.html',
        filter_buttons=filter_buttons,
        golfer=golfer,
        profile=profile,
        radar_data=radar_data,
        summary_table=summary_table,
        course_tabs=course_tabs,
        detail_tables=detail_tables
    )

def render_course(params: dict = {}):
    
    # course tabs
    course_tabs = build_course_tabs()
    
    summaries = []
    details = []
    for i, course in enumerate(db.session.query(Course).all()):

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

        detail = {}
        summary = [
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
        summaries.append(render_template(
            'stats/course_summary.html',
            summary=summary
        ))
        
        for hole in holes:

            detail[hole.number] = {
                'distance': hole.distance,
                'par': hole.par,
                'low': min([hs.score for hs in hole.scores if hs.is_completed()]),
                'average': round(np.mean([hs.score for hs in hole.scores if hs.is_completed()]), 2),
                'high': max([hs.score for hs in hole.scores if hs.is_completed()]),
            }
        detail = render_template(
            'stats/course_detail.html',
            table_id=f"stats-course-detail-{i}",
            detail=detail
        )
        details.append(detail)

    return render_template(
        'stats/course.html',
        course_tabs=course_tabs,
        summaries=summaries,
        details=details
    )
