from flask import render_template
from app import app
from app.forms import LoginForm
from app.mv import MovieRecommender

@app.route('/')
@app.route('/index')
def index():
    return render_template('base.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        mr = MovieRecommender()
        movies = mr.prediction_movie(370) 
        return render_template('results.html',user_id = form.user_id.data, movies = movies)
    return render_template('login.html', title = 'Sign In', form = form)