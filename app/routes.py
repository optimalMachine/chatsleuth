from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='ChatSleuth에 오신 것을 환영합니다')