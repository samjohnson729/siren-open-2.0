from app import app
from app.handlers import *

@app.route('/live')
@app.route('/live/<course>')
def live_summary(course: str = 'Fox Run'):
    return render_live_summary(course=course)

@app.route('/live/<course>/<hole>')
def live_detail(course: str = 'Fox Run', hole: int = 1):
    return render_live_detail(course=course, hole=hole)