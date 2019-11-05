from flask import render_template, flash, redirect, url_for
import pickle
from app import app
from app.forms import Recommendations, RateMovie, RegisterUser
from app.mv import MovieRecommender
from app.user import *

@app.route('/', methods = ['GET', 'POST'])
def get_recommendations():
    form = Recommendations()

    if form.validate_on_submit():
        try:
            with open ('./csv/users', 'rb') as infile:
                users = pickle.load(infile)
        except EnvironmentError:
            print(EnvironmentError)
        username = form.username.data
        password = form.password.data
        if(username not in users or users[username][1] != password):
            flash('Invalid Credentials')
            return redirect('/')
        user_id = users[username][0]
        mr = MovieRecommender()
        movies = mr.prediction_movie(user_id) 
        return render_template('results.html',username = username, movies = movies)
    return render_template('get_recommendations.html', title = 'Get Recommendations', form = form)

@app.route('/rate', methods = ['GET', 'POST'])
def rate_movie():

    form = RateMovie()
    if form.validate_on_submit():
        try:
            with open ('./csv/users', 'rb') as infile:
                users = pickle.load(infile)
        except EnvironmentError:
            print(EnvironmentError)
        username = form.username.data
        password = form.password.data
        if(username not in users or users[username][1] != password):
            flash('Invalid Credentials')
            return redirect('/rate')
        user_id = users[username][0]
        movie_id = int(form.movie_id.data)
        rating = int(form.rating.data)
        newMovieRating(user_id, movie_id, rating)
        flash('Successfully submitted rating')
        return redirect(url_for('get_recommendations'))

    return render_template('rate.html', title = 'Rate Movie', form = form)

@app.route('/register', methods = ['GET', 'POST'])
def register_user():

    form = RegisterUser()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        status, message = createNewUser(username, password)

        if status == False:
            flash(message)
            return redirect(url_for('register_user'))

        flash(message)
        return redirect(url_for('get_recommendations'))

    return render_template('register.html', title = 'Register User', form = form)


