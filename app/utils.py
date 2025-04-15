from app import db
from app.models import *
import numpy as np

def format_plus_minus(number):
    if number > 0:
        return f"+{number}"
    elif number == 0:
        return 'E'
    else:
        return str(number)
    
def flatten(xss):
    return [
        x
        for xs in xss
        for x in xs
    ]

def aggregate_z_score(**kwargs):

    if len(kwargs) == 2 and 'golfer' in kwargs and 'year' in kwargs:
        
        if kwargs['year'] is not None:
            hole_scores = (
                db.session.query(HoleScore)
                .join(Round)
                .join(Golfer)
                .join(Tournament)
            ).filter(
                (Golfer.name == kwargs['golfer']) &
                (Tournament.year == kwargs['year'])
            ).all()
        else:
            hole_scores = (
                db.session.query(HoleScore)
                .join(Round)
                .join(Golfer)
            ).filter(
                (Golfer.name == kwargs['golfer'])
            ).all()

        hole_scores = [hs for hs in hole_scores if hs.is_completed()]
        total = sum([hs._get_score() for hs in hole_scores])
        mu = sum([hs.hole._get_mean() for hs in hole_scores])
        sigma_2 = sum([hs.hole._get_variance() for hs in hole_scores])
        return (mu - total) / np.sqrt(sigma_2)
