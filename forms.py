from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, BooleanField, RadioField, SelectField, PasswordField
from wtforms.validators import InputRequired, Optional, Email

states = ["TX", "AL", "AK", "AZ", "CA", "CO", "CT", "DC", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WI", "WY"]

schools_list = [
    ('tamu', 'Texas A&M University'), 
    ('uh', 'University of Houston'), 
    ('unt', 'University of North Texas'), 
    ('uta', 'University of Texas at Arlington'), 
    ('ut', 'University of Texas at Austin'), 
    ('utd', 'University of Texas at Dallas'), 
    ('utep', 'University of Texas at El Paso'), 
    ('utrgv', 'University of Texas, Rio Grande Valley'), 
    ('utsa', 'University of Texas at San Antonio')]

class UserForm(FlaskForm):
    """Form for adding/editing new users"""

    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name")
    gender = RadioField("Gender", choices=[('Male', 'Male'), ('Female', 'Female')], validators=[InputRequired()])
    school_code = SelectField("School", choices=schools_list)
    email = StringField("Email Address (Used to login)", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])

class SchoolForm(FlaskForm):
    """Form for adding/editing new schools"""

    school_code = StringField("School Code")
    school_name = StringField("School Name", validators=[InputRequired()])
    city = StringField("City")
    state = SelectField("State", choices=[(st, st) for st in states], validators=[InputRequired()])

class KnowledgeBowlForm(FlaskForm):
    """Form for adding Knowledge Bowl team"""

    school_code = SelectField("School", choices=schools_list)
    captain = SelectField("Captain") # choices=users_list (based on school)
    player2 = SelectField("Player 2") # choices=users_list (based on school)
    player3 = SelectField("Player 3") # choices=users_list (based on school)
    player4 = SelectField("Player 4") # choices=users_list (based on school)
    
class LoginForm(FlaskForm):
    """Form for loging a user in"""

    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])