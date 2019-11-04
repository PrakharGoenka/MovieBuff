from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    user_id = StringField('User Id', validators=[DataRequired()])
    submit = SubmitField('Get Recommendations')