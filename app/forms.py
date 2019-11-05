import pandas as pd
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired

class Recommendations(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField('Get Recommendations')

class RateMovie(FlaskForm):

    movies = pd.read_csv('./csv/movies.csv', encoding="Latin1")
    movie_list = list()

    for index, rows in movies.iterrows():
        movie_list.append((str(rows.movieId), rows.title))

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])    
    movie_id = SelectField('Movie Id', choices = movie_list, validators=[DataRequired()])
    rating = IntegerField('Rating', validators=[DataRequired()])
    submit = SubmitField('Submit Rating')

class RegisterUser(FlaskForm):

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()]) 
    submit = SubmitField('Register')   
