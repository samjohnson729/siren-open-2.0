from app import app
from app.handlers import *

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')