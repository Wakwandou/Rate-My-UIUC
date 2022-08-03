from flask import render_template, request, jsonify, redirect, url_for, session
from app import app
from app import database as db_helper
import re

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        valid_login = db_helper.login_verification(username, password)
        
        if valid_login:
            session.permanent = True
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['username'] = username
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('login.html', msg=msg)

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "netid" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'netid' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        netid = request.form['netid']
    
        # If account exists show error and validation checks
        if db_helper.user_exists(username, netid):
            msg = 'Account already exists!'
        elif not re.match(r'[A-Za-z0-9]+', netid):
            msg = 'NetID must contain only characters and numbers!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not netid:
            msg = 'Please fill out the form!'
        elif db_helper.register_user(username, password, netid):
            msg = 'You have successfully registered!'
    
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'   

    return render_template('register.html', msg=msg)

@app.route('/')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        q = request.args.get('q')
        """ returns rendered homepage """
        keyword, searched_reviews = db_helper.search_reviews(q)
        return render_template("home.html", username=session['username'], reviews=searched_reviews, keyword=keyword)

        # return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        profile_info = db_helper.retrieve_profile(session['username'])
        reviews = db_helper.fetch_reviews_by_user(session['username'])
        print(reviews)
        # Show the profile page with account info
        return render_template('profile.html', profile=profile_info, reviews=reviews)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/review', methods=['GET', 'POST'])
def add_review():
    if 'loggedin' in session:
        profile_info = db_helper.retrieve_profile(session['username'])
        return render_template('review.html', username=session['username'])

@app.route("/delete/<string:review_id>", methods=['POST'])
def delete(review_id):
    """ recieved post requests for entry delete """
    print(review_id)
    try:
        db_helper.remove_review_by_id(review_id)
        result = {'success': True, 'response': 'Removed task'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)


@app.route("/edit/<string:review_id>", methods=['POST'])
def update(review_id):
    """ received post requests for entry updates """
    data = request.get_json()
    try:
        print(review_id)
        db_helper.update_review(review_id, data)
        result = {'success': True, 'response': 'Removed task'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)

@app.route("/create", methods=['POST'])
def create():
    """ receives post requests to add new task """
    data = request.get_json()
    print(data)
    db_helper.insert_review(session["username"], data)
    result = {'success': True, 'response': 'Done'}
    print(result)
    return jsonify(result)

@app.route("/search")
def homepage():
    q = request.args.get('q')
    """ returns rendered homepage """
    reviews = db_helper.fetch_reviews()
    courses, _ = db_helper.fetch_courses()
    instructors, _ = db_helper.fetch_instructors()
    keyword, searches = db_helper.search_reviews(q)
    if(keyword):
        reviews = searches
    return render_template("index.html", reviews=reviews, courses=courses, instructors=instructors, keyword=keyword)

@app.route("/avg_ratings")
def avg_ratings_page():
    """ returns each CRN along with its average rating """
    avg_ratings = db_helper.get_avg_ratings()
    instructors, _ = db_helper.fetch_instructors()
    return render_template("avg_ratings.html", avg_ratings=avg_ratings, instructors=instructors)

@app.route("/highest_ratings")
def highest_ratings_page():
    """ returns each course along with the professor with the highest average rating for it """
    ratings = db_helper.get_highest_ratings()
    
    return render_template("highest_ratings.html", ratings=ratings)
