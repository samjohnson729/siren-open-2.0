import os
if os.path.exists('./database.db'):
    os.remove('./database.db')

import pandas as pd
from app import app, db
from app.models import *
import sqlalchemy as sa

app.app_context().push()
db.create_all()


# load historical statistics
detailed = pd.read_csv('./detailed.csv').sort_values(['Year', 'Event', 'Name', 'Hole'])

# create all records for historical data
tournaments = {}
courses = {}
layouts = {}
holes = {}
golfers = {}
rounds = {}
hole_scores = {}

for year in detailed.Year.unique():
    df = detailed[
        (detailed.Year == year)
    ].copy()

    # Tournament
    tournament_id = year
    if tournament_id not in tournaments:
        t = Tournament(year=int(year))
        db.session.add(t)
        db.session.commit()
        tournaments[tournament_id] = t
    else:
        t = tournaments.get(tournament_id)


    for event in df.Event.unique():
        df = detailed[
            (detailed.Year == year) &
            (detailed.Event == event)
        ].copy()

        # Course
        course_id = event
        if course_id not in courses:
            c = Course(name=event)
            db.session.add(c)
            db.session.commit()
            courses[course_id] = c
        else:
            c = courses.get(course_id)

        # Layout
        layout_id = f"{event} - {df.groupby('Hole')[['Par', 'Distance']].apply(lambda x: x.iloc[0]).to_json()}"
        if layout_id not in layouts:
            l = Layout(course_id=c.id, year=int(year))
            db.session.add(l)
            db.session.commit()
            layouts[layout_id] = l
        else:
            l = layouts.get(layout_id)

        for name in df.Name.unique():
            df = detailed[
                (detailed.Year == year) &
                (detailed.Event == event) &
                (detailed.Name == name)
            ].copy()

            # Golfer
            golfer_id = name
            if golfer_id not in golfers:
                g = Golfer(name=name)
                db.session.add(g)
                db.session.commit()
                golfers[golfer_id] = g
            else:
                g = golfers.get(golfer_id)

            # Round
            round_id = f"{year} - {event} - {name}"
            if round_id not in rounds:
                r = Round(tournament_id=t.id, golfer_id=g.id, layout_id=l.id)
                db.session.add(r)
                db.session.commit()
                rounds[round_id] = r
            else:
                r = rounds.get(round_id)


            for hole_number in df.Hole.unique():
                df = detailed[
                    (detailed.Year == year) &
                    (detailed.Event == event) &
                    (detailed.Name == name) &
                    (detailed.Hole == hole_number)
                ].copy()

                # Hole
                hole_id = f"{c.name} - {hole_number} - {df.Par.iloc[0]} - {df.Distance.iloc[0] if pd.notna(df.Distance.iloc[0]) else 0}"
                if hole_id not in holes:
                    h = Hole(number=int(hole_number), par=int(df.Par.iloc[0]))
                    l.holes.append(h)
                    if pd.notna(df.Distance.iloc[0]):
                        h.distance = int(df.Distance.iloc[0])
                    db.session.add(h)
                    db.session.commit()
                    holes[hole_id] = h
                else:
                    h = holes.get(hole_id)
                    l.holes.append(h)

                # Hole Score
                hole_score_id = f"{r.id} - {hole_number}"
                if hole_score_id not in hole_scores:
                    hs = HoleScore(round_id=r.id, hole_id=h.id, score=int(df.Score.iloc[0]))
                    db.session.add(hs)
                    db.session.commit()
                    hole_scores[hole_score_id] = hs
                else:
                    hs = hole_scores.get(hole_score_id)


# create 2025 initial records
t = Tournament(year=2025)
db.session.add(t)

g = Golfer(name='Dan Sievert')
db.session.add(g)
g = Golfer(name='Matt Kiloran')
db.session.add(g)
db.session.commit()

for g in db.session.query(Golfer).all():
    for c in db.session.query(Course).all():
        if c.name == 'Tjiny Acres':
            continue

        l: Layout = c.layouts[-1]
        r = Round(tournament_id=t.id, golfer_id=g.id, layout_id=l.id)
        db.session.add(r)
        db.session.commit()
        for h in l.holes:
            hs = HoleScore(round_id=r.id, hole_id=h.id)
            db.session.add(hs)
            db.session.commit()

db.session.commit()

# load historical statistics for 2022 Moose Mulligan
t = db.session.query(Tournament).filter(Tournament.year == 2022).first()
l = db.session.query(Layout).join(Course).filter(Course.name == 'Moose Mulligan').first()

summary = pd.read_csv('./summary.csv').sort_values(['Year', 'Event', 'Name'])
for i, row in summary.iterrows():
    g = db.session.query(Golfer).filter(Golfer.name == row['Name']).first()
    r = Round(
        tournament_id=t.id,
        layout_id=l.id,
        golfer_id=g.id,
        _total_score=row['Score']
    )
    db.session.add(r)
db.session.commit()
