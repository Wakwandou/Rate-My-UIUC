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
    return {"username": result[0], "password": result[1], "netid": result[2]}

def fetch_reviews_by_user(username) -> dict:
    """ Reads and returns a dictionary of reviews """
    conn = db.connect()
    conn.execute("use squad;")
    results = conn.execute ("""
        Select ReviewID, Rating, Comment, IsRecommended, RequiresTextbook, Username, Course, CourseName, Name 
        From Reviews r JOIN Courses c on r.CRN=c.CRN JOIN Instructors i on r.InstructorNetID=i.NetID 
        WHERE Username="{}"
        ORDER BY Course, Rating DESC
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

def fetch_courses() -> dict:
    """Reads and returns a dictionary of courses"""
    conn = db.connect()
    conn.execute("use squad;")
    query_results = conn.execute("Select DISTINCT * from Courses;").fetchall()
    conn.close()
    course_names = []
    course_to_crn = {} 
    
    for result in query_results:
        course_names.append(result[5])
        course_to_crn[result[5]] = result[0]

    return course_names, course_to_crn

def fetch_instructors() -> dict:
    """ Reads and returns a dictionary of instructors """
    conn = db.connect()
    conn.execute("use squad;")
    query_results = conn.execute("Select DISTINCT * from Instructors;").fetchall()
    conn.close()
    instructors_names = []
    name_to_netid = {}
    for result in query_results:
        instructors_names.append(result[1])
        name_to_netid[result[1]] = result[0]
    return instructors_names, name_to_netid

def fetch_keywords():
    conn = db.connect()
    conn.execute("use squad;")
    query1 = conn.execute("Select DISTINCT Name from Instructors;").fetchall()
    query2 = conn.execute("Select DISTINCT Course from Courses;").fetchall()
    query3 = conn.execute("Select DISTINCT DeptAbv from Departments;").fetchall()
    instructors = []
    courses = []
    depts = []
    for result in query1:
        instructors.append(result[0])
    for result in query2:
        courses.append(result[0])
    for result in query3:
        depts.append(result[0])

    return instructors, courses, depts

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

def insert_review(username, data: dict):
    reviewID = random.randint(0, 10000)
    while(reviewID) in list(fetch_courses()):
        reviewID = random.randint(0, 10000)
        
    CRN, InstructorNetID = validate_review(data)
    recommended = int(data['recommended'])
    textbook = int(data['textbook'])

    conn = db.connect()
    conn.execute("use squad;")
    query = 'Insert Into Reviews (ReviewID, Rating, Comment, IsRecommended, RequiresTextbook, Username, CRN, InstructorNetID) VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}");'.format(reviewID, data['rating'], data['comment'], recommended, textbook, username, CRN, InstructorNetID)
    conn.execute(query)
    # db.session.commit()
    conn.close()

#updates review with ID of selectedReviewID
def update_review(review_id, data):
    
    CRN, InstructorNetID = validate_review(data)
    recommended = int(data['recommended'])
    textbook = int(data['textbook'])
    conn = db.connect()
    conn.execute("use squad;")
    query = 'UPDATE Reviews SET Rating = "{}", Comment = "{}", IsRecommended = "{}", RequiresTextbook = "{}", CRN = "{}", InstructorNetID = "{}" WHERE ReviewID = "{}";'.format(data['rating'], data['comment'], recommended, textbook, CRN, InstructorNetID, review_id)
    conn.execute(query)
    db.session.commit()
    conn.close()

def search_reviews(keyword):
    conn = db.connect()
    conn.execute("use squad;")
    results = conn.execute ("""
        Select ReviewID, Rating, Comment, IsRecommended, RequiresTextbook, Username, Course, CourseName, Name 
        From Reviews r JOIN Courses c on r.CRN=c.CRN JOIN Instructors i on r.InstructorNetID=i.NetID JOIN Departments d on c.DeptAbv=d.DeptAbv
        WHERE c.Course="{}" or r.Comment LIKE "{}" OR c.DeptAbv="{}" or i.Name="{}" or i.NetID="{}" or c.CRN="{}" or d.DeptName="{}"
        ORDER BY c.Course, Name, Rating DESC
        """.format(keyword,keyword,keyword,keyword,keyword,keyword,keyword)).fetchall()
    conn.close()
    searched_reviews = []
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
        searched_reviews.append(review)
    return keyword, searched_reviews

def remove_review_by_id(review_id: str) -> None:
    """ remove entries based on review ID """
    conn = db.connect()
    conn.execute("use squad;")
    query = 'Delete From Reviews Where ReviewID="{}";'.format(review_id)
    conn.execute(query)
    db.session.commit()
    conn.close()

def get_reviews_avg(course):
    conn = db.connect()
    conn.execute("use squad;")
    query = 'SELECT i.NetID, i.Name, AVG(r.Rating), COUNT(r.Rating), MIN(r.Rating), MAX(r.Rating) from Reviews r inner join Courses c on c.CRN = r.CRN inner join Instructors i on i.NetID = r.InstructorNetID where c.Course like "{}" group by i.NetID'.format(course) 
    results = conn.execute(query).fetchall()
    conn.close()

    stats = []
    for result in results:
        stat = {
            "Instructor": result[1],
            "Average": result[2],
            "Number": result[3],
            "Minimum": result[4],
            "Maximum": result[5]
        }
        stats.append(stat)

    return stats