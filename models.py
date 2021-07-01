from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
# from wtforms.validators import InputRequired
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    db.app = app 
    db.init_app(app)


# Models

class School(db.Model):
    """School model"""

    __tablename__ = "schools"

    school_code = db.Column(db.Text, primary_key=True)
    school_name = db.Column(db.Text)
    city = db.Column(db.Text)
    state = db.Column(db.Text, default='TX')

    def __repr__(self):
        return f"<School {self.school_code} {self.school_name} {self.city} {self.state}>"

    def serialize_school(self):
        return {
            'school_code': self.school_code,  
            'school_name': self.school_name,
            'city': self.city,
            'state': self.state
        }

class User(db.Model):
    """User model"""

    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text)
    gender = db.Column(db.Text, nullable=False)
    school_code = db.Column(db.Text, db.ForeignKey('schools.school_code')) # ForeignKey to school_code 
    email = db.Column(db.Text, nullable=False)  # make unique=True
    password = db.Column(db.Text, nullable=False)

    school = db.relationship('School', backref="users")

    @classmethod
    def register(cls, first_name, last_name, gender, school_code, email, password):
        """Register user w/ hashed password & return user"""

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8") # convert to unicode string

        return cls (first_name=first_name, last_name=last_name, gender=gender, school_code=school_code, email=email, password=hashed_utf8)

    @classmethod
    def authenticate(cls, email, password):
        """Validate that user exists & password is correct. 
        Return user if valid; else return false"""

        u = User.query.filter_by(email=email).first()

        if u and bcrypt.check_password_hash(u.password, password):
            return u
        else:
            return False

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name} {self.gender} {self.school_code} {self.email} {self.password}>"

    def serialize_user(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'gender': self.gender,
            'school_code': self.school_code,
            'email': self.email,
            'password': self.password
        }

# class KnowledgeBowl(db.Model):
#     """Knowledge Bowl model"""

#     __tablename__ = "k_bowl"

#     id = db.Column(db.Integer, autoincrement=True, primary_key=True)    
#     comp_name = db.Column(db.Text)
#     school_code = db.Column(db.Text, db.ForeignKey('schools.school_code'))
#     captain = db.Column(db.Text, db.ForeignKey('users.id'))
#     player2 = db.Column(db.Text, db.ForeignKey('users.id'))
#     player3 = db.Column(db.Text, db.ForeignKey('users.id'))
#     player4 = db.Column(db.Text, db.ForeignKey('users.id'))

#     def __repr__(self):
#         return f"<Knowledge Bowl {self.id} {self.comp_name} {self.school_code} {self.captain} {self.player2} {self.player3} {self.player4}>"

class Competition(db.Model):
    """Competition model"""

    __tablename__ = "competitions"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    school_code = db.Column(db.Text, db.ForeignKey('schools.school_code'))
    comp_name = db.Column(db.Text)
    captain = db.Column(db.Integer, db.ForeignKey('users.id'))
    player = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f"<Competition {self.school_code} {self.comp_name} {self.captain} {self.player}>"
    
    def serialize_competition(self):
        return {
            'id': self.id,
            'school_code': self.school_code,  
            'comp_name': self.comp_name,
            'captain': self.captain,  
            'player': self.player
        }