from app import app, db
from app.models import *
from app.handlers import *

@app.route('/update_score', methods=['GET', 'POST'])
def update_score():
    try:
        payload = request.values.to_dict()
        hs = db.session.query(HoleScore).filter(
            (HoleScore.hole_id == payload['hole_id']) &
            (HoleScore.round_id == payload['round_id'])
        ).first()
        hs.score = payload['score'] if int(payload['score']) > 0 else None
        db.session.commit()
        return redirect(request.referrer)
    except Exception as e:
        return f"Error: {e}"