from flask import render_template, request, jsonify, redirect, url_for
from app import app
from app import database as db_helper

@app.route("/delete/<string:review_id>", methods=['POST'])
def delete(review_id):
    """ recieved post requests for entry delete """

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
    db_helper.insert_review(data)
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)

@app.route("/")
def homepage():
#    q = request.args.get('q')
   """ returns rendered homepage """
   reviews = db_helper.fetch_reviews()
   courses, _ = db_helper.fetch_courses()
   instructors, _ = db_helper.fetch_instructors()
#    name = db_helper.search_reviews(q)
   
   return render_template("index.html", reviews=reviews, courses=courses, instructors=instructors)
# @app.route("/result")
# def result():

@app.route("/avg_ratings")
def avg_ratings_page():
    """ returns each CRN along with its average rating """
    avg_ratings = db_helper.get_avg_ratings()
    instructors, _ = db_helper.fetch_instructors()
    return render_template("avg_ratings.html", avg_ratings=avg_ratings, instructors=instructors)

@app.route("/highest_ratings")
def highest_ratings_page():
    """ returns each CRN along with its average rating """
    ratings = db_helper.get_highest_ratings()
    
    return render_template("highest_ratings.html", ratings=ratings)