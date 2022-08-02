from calendar import c
import random
from app import db

def user_exists(username, netid):
    conn = db.connect()
    conn.execute("use squad;")
    query = 'Select Username from Users WHERE Username="{}" OR NetID="{}";'.format(username, netid)
    result = conn.execute(query).fetchall()
    return bool(result)

def login_verification(username, password):
    if not user_exists(username, username):
        return False
    conn = db.connect()
    conn.execute("use squad;")
    query = 'Select Password from Users WHERE Username="{}";'.format(username)
    result = conn.execute(query).fetchall()[0]
    return password==result[0]

def register_user(username, password, netid):
    conn = db.connect()
    conn.execute("use squad;")
    query = 'Insert Into Users (NetID, Username, Password, IsGuest) VALUES ("{}", "{}", "{}", "{}");'.format(netid, username, password, 0)
    conn.execute(query)
    conn.close()
    return True

def retrieve_profile(username):
    if not user_exists(username, username):
        return []
    conn = db.connect()
    conn.execute("use squad;")
    query = 'Select Username, Password, NetID from Users WHERE Username="{}";'.format(username)
    result = conn.execute(query).fetchall()[0]
    print(result[0])
    return {"username": result[0], "password": result[1], "netid": result[2]}

def fetch_reviews_by_user(username) -> dict:
    """ Reads and returns a dictionary of reviews """
    conn = db.connect()
    conn.execute("use squad;")
    results = conn.execute ("""
        Select ReviewID, Rating, Comment, IsRecommended, RequiresTextbook, Username, Course, CourseName, Name 
        From Reviews r JOIN Courses c on r.CRN=c.CRN JOIN Instructors i on r.InstructorNetID=i.NetID 
        WHERE Username="{}"
    """.format(username)).fetchall()

    conn.close()
    user_reviews = []
    for result in results:
        review = {
            "ReviewID": result[0],
            "Rating": result[1],
            "Comment": result[2],
            "IsRecommended": "Yes" if result[3] else "No",
            "RequiresTextbook": "Yes" if result[4] else "No",
            "Username": result[5],
            "Course": result[6],
            "CourseName": result[7],
            "InstructorName": result[8]
        }
        user_reviews.append(review)
    return user_reviews

def validate_review(data: dict):
    """ Finds whether a associated course and instructor exists """
    _, courses = fetch_courses()
    _, instructors = fetch_instructors()

    CRN = courses[data['class']]
    InstructorNetID = instructors[data['instructor']]
    return CRN, InstructorNetID

def fetch_reviews() -> dict:
    """ Reads and returns a dictionary of reviews """
    conn = db.connect()
    conn.execute("use squad;")
    query_results = conn.execute("Select * from Reviews;").fetchall()
    conn.close()
    reviews = []
    for result in query_results:
        item = {
            "ReviewID": result[0],
            "Rating": result[1],
            "Comment": result[2],
            "IsRecommended": "Yes" if result[3] else "No",
            "RequiresTextbook": "Yes" if result[4] else "No",
            "Username": result[5],
            "CRN": result[6],
            "InstructorNetID": result[7]
        }
        reviews.append(item)
    return reviews

def fetch_courses() -> dict:
    """Reads and returns a dictionary of courses"""
    conn = db.connect()
    conn.execute("use squad;")
    query_results = conn.execute("Select * from Courses;").fetchall()
    conn.close()
    courses = {}
    course_to_crn = {} 
    
    for result in query_results:
        course = {
            "CourseName": result[1],
            "CourseNumber": result[2],
            "Description": result[3],
            "DeptAbv": result[4],
            "Course": result[4] + result[2]
        }
        courses[result[0]] = course
        course_to_crn[result[4] + result[2]] = result[0]

    return courses, course_to_crn

def fetch_instructors() -> dict:
    """ Reads and returns a dictionary of instructors """
    conn = db.connect()
    conn.execute("use squad;")
    query_results = conn.execute("Select * from Instructors;").fetchall()
    conn.close()
    instructors = {}
    name_to_netid = {}
    for result in query_results:
        instructor = {
            "Name": result[1],
            "DeptAbv": result[2]
        }
        instructors[result[0]] = instructor
        name_to_netid[result[1]] = result[0]

    return instructors, name_to_netid

# average ratings for each CRN 
def get_avg_ratings():
    conn = db.connect()
    conn.execute("use squad;")
    results = conn.execute ("""
        SELECT c.CRN, c.DeptAbv, c.CourseNumber, c.CourseName, c.Description, AVG(r.Rating), r.InstructorNetID 
        FROM Reviews r 
        LEFT JOIN Courses c ON r.CRN = c.CRN 
        LEFT JOIN Enrollments e ON c.CRN = e.CRN 
        GROUP BY c.CRN, r.InstructorNetID
        ORDER BY c.DeptAbv, c.CourseNumber; """).fetchall()
    conn.close()
    CRNs = []
    for result in results:
        CRN = {
            "CRN": result[0],
            "Course": result[1]+result[2],
            "CourseName": result[3],
            "Description": result[4],
            "avgRating": round(result[5],2),
            "InstructorNetID": result[6]
        }
        CRNs.append(CRN)

    return CRNs
    
# returns the most highly rated professors name and their rating for all courses (identified by the coursenumber and deptabv)
def get_highest_ratings():
    conn = db.connect()
    conn.execute("use squad;")
    results = conn.execute("""
        SELECT DISTINCT i.Name, s2.DeptAbv, s2.CourseNumber, s2.maxRating
        FROM (
                SELECT MAX(s1.avgRating) as maxRating, s1.DeptAbv, s1.CourseNumber
                FROM (
                        SELECT AVG(r.Rating) as avgRating, c.DeptAbv, c.CourseNumber, r.InstructorNetID, c.CourseName 
                        FROM Reviews r 
                        LEFT JOIN Courses c ON r.CRN = c.CRN 
                        GROUP BY c.DeptAbv, c.CourseNumber, r.InstructorNetID, c.CourseName
                    ) AS s1 
                GROUP BY s1.DeptAbv, s1.CourseNumber) AS s2 
                LEFT JOIN (
                            SELECT AVG(r2.Rating) as avgRating, c2.DeptAbv, c2.CourseNumber, r2.InstructorNetID 
                            FROM Reviews r2 LEFT JOIN Courses c2 ON r2.CRN = c2.CRN 
                            GROUP BY c2.DeptAbv, c2.CourseNumber, r2.InstructorNetID
                        ) AS s3 
                ON s2.maxRating = s3.avgRating AND s2.DeptAbv = s3.DeptAbv AND s2.CourseNumber = s3.CourseNumber 
                LEFT JOIN Instructors i 
                ON s3.InstructorNetID = i.NetID
                ORDER BY s2.DeptAbv, s2.CourseNumber;
                """).fetchall()
    conn.close()
    ratings = []

    for result in results:
        rating = {
            "deptAbv": result[1],
            "courseNum": result[2],
            # "courseName":result[4],
            "instructor": result[0],
            "avgRating": result[3]
        }
        ratings.append(rating)

    return ratings

def insert_review(data: dict):
    reviewID = random.randint(0, 10000)
    while(reviewID) in list(fetch_courses()):
        reviewID = random.randint(0, 10000)
        
    CRN, InstructorNetID = validate_review(data)
    recommended = int(data['recommended'])
    textbook = int(data['textbook'])

    conn = db.connect()
    conn.execute("use squad;")
    query = 'Insert Into Reviews (ReviewID, Rating, Comment, IsRecommended, RequiresTextbook, Username, CRN, InstructorNetID) VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}");'.format(reviewID, data['rating'], data['comment'], recommended, textbook, "username1", CRN, InstructorNetID)
    conn.execute(query)
    conn.close()

    # return task_id


def remove_review_by_id(review_id: str) -> None:
    """ remove entries based on review ID """
    conn = db.connect()
    conn.execute("use squad;")
    query = 'Delete From Reviews Where ReviewID="{}";'.format(review_id)
    conn.execute(query)
    db.session.commit()
    conn.close()

#updates review with ID of selectedReviewID
def update_review(review_id, data):
    
    CRN, InstructorNetID = validate_review(data)
    recommended = int(data['recommended'])
    textbook = int(data['textbook'])

    conn = db.connect()
    conn.execute("use squad;")
    query = 'UPDATE Reviews SET Rating = "{}", Comment = "{}", IsRecommended = "{}", RequiresTextbook = "{}", CRN = "{}", InstructorNetID = "{}" WHERE ReviewID = "{}";'.format(data['rating'], data['comment'], recommended, textbook, "username1", CRN, InstructorNetID, review_id)
    conn.execute(query)
    conn.commit()
    conn.close()

def search_reviews(keyword):
    conn = db.connect()
    conn.execute("use squad;")
    query = 'SELECT r.ReviewID, r.Rating, r.Comment, r.IsRecommended, r.RequiresTextbook, r.Username, r.CRN, r.InstructorNetID FROM Reviews r inner join Courses c on r.CRN = c.CRN inner join Departments d on d.DeptAbv = c.DeptAbv inner join Instructors i on i.NetID = r.InstructorNetID WHERE c.Course="{}" or r.Comment LIKE "{}" OR c.DeptAbv="{}" or i.Name="{}" or i.NetID="{}" or c.CRN="{}";'.format(keyword,keyword,keyword,keyword,keyword,keyword)

    results = conn.execute(query).fetchall()
    conn.close()

    reviews = []
    for result in results:
        item = {
            "ReviewID": result[0],
            "Rating": result[1],
            "Comment": result[2],
            "IsRecommended": "Yes" if result[3] else "No",
            "RequiresTextbook": "Yes" if result[4] else "No",
            "Username": result[5],
            "CRN": result[6],
            "InstructorNetID": result[7]
        }
        reviews.append(item)

    return keyword, reviews
