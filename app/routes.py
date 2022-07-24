from flask import render_template, request, jsonify, request
from app import app
from app import database as db_helper
 
@app.route("/")
def homepage():
   q = request.args.get('q')
   return render_template("home.html", nam=db_helper.search_review(q))