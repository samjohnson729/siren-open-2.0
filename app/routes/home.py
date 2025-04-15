from app import app
from app.handlers import *

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')