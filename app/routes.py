from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm, RateMovie
from app.mv import MovieRecommender
from app.user import User

@app.route('/', methods = ['GET', 'POST'])
def get_recommendations():
    form = LoginForm()

    if form.validate_on_submit():
        mr = MovieRecommender()
        movies = mr.prediction_movie(int(form.user_id.data)) 
        return render_template('results.html',user_id = form.user_id.data, movies = movies)
    return render_template('login.html', title = 'Sign In', form = form)

@app.route('/rate', methods = ['GET', 'POST'])
def rate_movie():

    form = RateMovie()
    if form.validate_on_submit():
        user_id = int(form.user_id.data)
        movie_id = int(form.movie_id.data)
        rating = int(form.rating.data)
        user = User()
        user.newMovieRating(user_id, movie_id, rating)
        flash('Successfully submitted rating')
        return redirect(url_for('get_recommendations'))

    return render_template('rate.html', title = 'Rate Movie', form = form)
