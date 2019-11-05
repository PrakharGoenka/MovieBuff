import pandas as pd
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    user_id = StringField('User Id', validators=[DataRequired()])
    submit = SubmitField('Get Recommendations')

class RateMovie(FlaskForm):
    user_id = StringField('User Id', validators=[DataRequired()])
    movie_id = StringField('Movie Id', validators=[DataRequired()])
    rating = StringField('Rating', validators=[DataRequired()])
    submit = SubmitField('Submit Rating')
