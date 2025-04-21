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

def aggregate_z_score(values, row_attrs:list, col_attrs:list):
    
    all_rounds = [r for r in db.session.query(Round).all() if r.is_completed()]
    
    if (
        (row_attrs[-2:] == ['golfer', 'name'] and col_attrs[-2:] == ['course', 'name']) or
        (row_attrs[-2:] == ['tournament', 'year'] and col_attrs[-2:] == ['course', 'name'])
    ):
        
        scores = {}
        for r in all_rounds:
            if r.layout.course.name not in scores:
                scores[r.layout.course.name] = []
            scores[r.layout.course.name].append(r._get_score())
            
        total_mu = 0
        total_var = 0
        for k,v in scores.items():
            if values.get(k) is not None:
                total_mu += np.mean(v)
                total_var += np.var(v)
            
        if total_mu > 0:
            total = sum(v for v in values.values() if v is not None)
            return (total_mu - total) / np.sqrt(total_var)
        
    elif (
        (row_attrs[-2:] == ['hole', 'number'] and col_attrs[-2:] == ['golfer', 'name'])
    ):
        
        scores = []
        for r in all_rounds:
            if r.layout.course.name != values['course']:
                continue
            
            scores.append(r._get_score())
            
        if values['total'] > 0:
            return (np.mean(scores) - values['total']) / np.std(scores)
        
    else:
        pass
            
