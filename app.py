from flask import Flask, request, render_template, redirect, flash, session, jsonify
# from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, School, User, Competition
from forms import SchoolForm, UserForm, CompetitionForm, LoginForm
from sqlalchemy import func

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///showdown_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "MSALSCShowdownApp"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def home():
    """Shows home page"""

    return render_template('home_page.html')


########### SCHOOL ROUTES ###########

@app.route('/school/new', methods=["GET", "POST"])
def add_school():
    """Shows form to add new school"""

    form = SchoolForm()

    if form.validate_on_submit():
        school_code = form.school_code.data
        school_name = form.school_name.data
        city = form.city.data
        state = form.state.data

        school = School(school_code=school_code, school_name=school_name, city=city, state=state)
        db.session.add(school)
        db.session.commit()
        return redirect("/school/registered")

    else:
        return render_template('add_school_form.html', form=form)

@app.route('/school/registered')
def list_schools():
    """Show registered schools"""

    schools = School.query.all()
    total_count = School.query.count()

    registered_schools = db.session \
        .query(School.school_code, School.school_name, School.city, School.state, func.count(User.id).label("total_students")) \
        .join(User) \
        .group_by(School.school_code, School.school_name, School.city, School.state) \
        .all()

    return render_template('registered_schools.html', schools=schools, total_count=total_count, registered_schools=registered_schools)

@app.route('/school/<string:school_code>', methods=["GET", "POST"])
def get_school(school_code):
    """Show information about one school"""

    school = School.query.get_or_404(school_code)

    # POST request
    form = CompetitionForm()

    if form.validate_on_submit():
        school_code = form.school_code.data
        comp_name = form.comp_name.data
        player = form.player.data

        comp = Competition(school_code=school_code, comp_name=comp_name, player=player)
        db.session.add(comp)
        db.session.commit()
        return redirect("/school/{}".format(school_code))

    else:
        return render_template('show_school.html', school=school, form=form)


########### USER ROUTES ###########

@app.route('/user/new', methods=["GET", "POST"])
def add_user():
    """Shows form to add new user"""

    form = UserForm()

    # grab list of schools from db and dynamically add to choice of schools
    # schools_list = db.session.query(School.school_code, School.school_name)
    # form.school_code.choices = schools_list
    
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        gender = form.gender.data
        school_code = form.school_code.data
        email = form.email.data
        password = form.password.data

        new_user = User.register(first_name, last_name, gender, school_code, email, password)

        db.session.add(new_user)
        db.session.commit()

        return redirect("/user/registered")

    else:
        return render_template('add_user_form.html', form=form)

@app.route('/user/registered')
def list_users():
    """Show registered users"""

    form = UserForm()

    users = User.query.all()
    count = User.query.count()

    return render_template('registered_users.html', users=users, count=count, form=form)

@app.route('/user/registered', methods=["POST"])
def add_user_on_list():
    """Shows form to add new user"""

    form = UserForm()

    # grab list of schools from db and dynamically add to choice of schools
    # schools_list = db.session.query(School.school_code, School.school_name)
    # form.school_code.choices = schools_list
    
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        gender = form.gender.data
        school_code = form.school_code.data
        email = form.email.data
        password = form.password.data

        new_user = User.register(first_name, last_name, gender, school_code, email, password)
        
        db.session.add(new_user)
        db.session.commit()

        return redirect("/user/registered")

    else:
        return render_template('add_user_form.html', form=form)

@app.route('/user/<int:id>')
def show_user(id):
    """Show user profile"""

    user = User.query.get_or_404(id)
    
    # PREPOPULATE FORM WITH EXISTING DATA
    # EDIT THE FORM
    # db.session. (user)
    # db.session.commit()

@app.route('/user/<int:id>', methods=["DELETE"])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify(message="deleted")

@app.route('/login', methods=["GET", "POST"])
def login_user():
    form = LoginForm()
    
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.authenticate(email, password)

        if user:
            flash(f"Welcome Back, {user.email}!", "primary")
            session['user_id'] = user.id
            return redirect('/')
        else:
            form.email.errors = ["Invalid email/password"]

    return render_template('login.html', form=form)

@app.route('/secret')
def secret():
    """Test Logins"""

    return render_template('secret.html')

######################################################################

# RESTful API with naming convention (GET; get all schools)
@app.route('/api/school')
def list_all_schools_demo():
    all_schools = [school.serialize_school() for school in School.query.all()]
    return jsonify(schools=all_schools)

# RESTful API with naming convention (GET; get one school)
@app.route('/api/school/<string:school_code>')
def get_one_school_demo(school_code):
    school = School.query.get_or_404(school_code)
    return jsonify(school=school.serialize_school())

# RESTful API with naming convention (POST; create new school)
@app.route('/api/school', methods=["POST"])
def create_school():
    new_school = School(school_code=request.json["school_code"], school_name=request.json["school_name"], city=request.json["city"], state=request.json["state"])    # assumes school_name is passed into the request
    db.session.add(new_school)
    db.session.commit()
    response_json = jsonify(school=new_school.serialize_school()) # respond with json
    return (response_json, 201) # respond with json and status code as a tuple

# RESTful API with naming convention (PATCH; update one school)
@app.route('/api/school/<string:school_code>', methods=["PATCH"])
def update_school(school_code):
    school = School.query.get_or_404(school_code)
    school.school_name = request.json.get('school_name', school.school_name)
    school.city = request.json.get('city', school.city)
    db.session.commit()
    return jsonify(school=school.serialize_school())

# RESTful API with naming convention (DELETE; delete one school)
@app.route('/api/school/<string:school_code>', methods=["DELETE"])
def delete_school(school_code):
    school = School.query.get_or_404(school_code)
    db.session.delete(school)
    db.session.commit()
    return jsonify(message="deleted")