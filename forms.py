from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, BooleanField, RadioField, SelectField, PasswordField
from wtforms.validators import InputRequired, Optional, Email
from wtforms.widgets.core import Select

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

comps_list = [
    ('m_soccer', "Men's Soccer"),
    ('m_football', "Men's Football"),
    ('m_basketball', "Men's Basketball"),
    ('w_basketball', "Women's Basketball"),
    ('w_volleyball', "Women's Volleyball"),
    ('w_dodgeball', "Women's Dodgeball"),
    ('k_bowl', 'Knowledge Bowl')
]

class UserForm(FlaskForm):
    """Form for adding/editing new users"""

    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name")
    gender = RadioField("Gender", choices=[('Male', 'Male'), ('Female', 'Female')], validators=[InputRequired()])
    school_code = SelectField("School", choices=schools_list)
    email = StringField("Email Address", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])

class SchoolForm(FlaskForm):
    """Form for adding/editing new schools"""

    school_code = StringField("School Code")
    school_name = StringField("School Name", validators=[InputRequired()])
    city = StringField("City")
    state = SelectField("State", choices=[(st, st) for st in states], validators=[InputRequired()])
    
class CompetitionForm(FlaskForm):
    """Form for adding new competition roster"""

    school_code = SelectField("School", choices=schools_list)
    comp_name = SelectField("Competition", choices=comps_list)
    player = StringField("Player")

class LoginForm(FlaskForm):
    """Form for loging a user in"""

    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])