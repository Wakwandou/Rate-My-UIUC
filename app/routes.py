""" Specifies routing for the application"""
from flask import render_template, request, jsonify
from app import app
from app import database as db_helper

@app.route("/delete/<string:review_id>", methods=['POST'])
def delete(review_id):
    """ recieved post requests for entry delete """

    try:
        print(review_id)
        db_helper.remove_review_by_id(review_id)
        print("worked")
        result = {'success': True, 'response': 'Removed task'}
    except:
        print("failed")
        result = {'success': False, 'response': 'Something went wrong'}

    print(result)
    return jsonify(result)


@app.route("/edit/<int:task_id>", methods=['POST'])
def update(task_id):
    """ recieved post requests for entry updates """

    data = request.get_json()

    try:
        if "status" in data:
            db_helper.update_status_entry(task_id, data["status"])
            result = {'success': True, 'response': 'Status Updated'}
        elif "description" in data:
            db_helper.update_task_entry(task_id, data["description"])
            result = {'success': True, 'response': 'Task Updated'}
        else:
            result = {'success': True, 'response': 'Nothing Updated'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)


@app.route("/create", methods=['POST'])
def create():
    """ recieves post requests to add new task """
    data = request.get_json()
    db_helper.insert_new_task(data['description'])
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)


@app.route("/")
def homepage():
    """ returns rendered homepage """
    reviews = db_helper.fetch_reviews()
    courses = db_helper.fetch_courses()
    instructors = db_helper.fetch_instructors()
    return render_template("index.html", reviews=reviews, courses=courses, instructors=instructors)