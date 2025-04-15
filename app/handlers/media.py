from flask import render_template
from app import app, db
from app.models import *
import os, random

def render_media():
    media_by_year = {}
    for t in db.session.query(Tournament).all()[::-1]:
        try:
            files = os.listdir(os.path.join(os.getcwd(), 'app', 'static', 'media', str(t.year)))
            random.shuffle(files)
            media_by_year[str(t.year)] = files
        except:
            pass
    return render_template('media.html', media_by_year=media_by_year)