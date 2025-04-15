from app import app
from app.handlers import *

@app.route('/media')
def media():
    return render_media()