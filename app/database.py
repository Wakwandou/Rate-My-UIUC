import random
from app import db

def fetch_reviews() -> dict:
    """Reads and returns a dictionary of reviews"""

    conn = db.connect()
    conn.execute("use squad;")
    query_results = conn.execute("Select * from Reviews;").fetchall()
    conn.close()
    reviews = []
    for result in query_results:
        item = {
            "ReviewID": result[0].strip(),
            "Rating": result[1],
            "Comment": result[2].strip(),
            "IsRecommended": "Yes" if result[3] else "No",
            "RequiresTextbook": "Yes" if result[4] else "No",
            "Username": result[5].strip(),
            "CRN": result[6].strip(),
            "InstructorNetID": result[7].strip()
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
    for result in query_results:
        course = {
            "CourseName": result[1].strip(),
            "CourseNumber": result[2],
            "Description": result[3].strip(),
            "DeptAbv": result[4].strip(),
            "Course": result[4].strip() + result[2]
        }
        courses[result[0].strip()] = course
    
    return courses

def fetch_instructors() -> dict:
    """Reads and returns a dictionary of instructors"""
    conn = db.connect()
    conn.execute("use squad;")
    query_results = conn.execute("Select * from Instructors;").fetchall()
    conn.close()
    instructors = {}
    for result in query_results:
        instructor = {
            "Name": result[1].strip(),
            "DeptAbv": result[2].strip()
        }
        instructors[result[0].strip()] = instructor
    
    return instructors


def get_name():
    return random.choice(["Ann", "Bob", "Chris", "Daniel"])

# average ratings for each CRN 
def get_avg_ratings():
    conn = db.connect()
    results = conn.execute 
    (
        """ 
        SELECT AVG(r.Rating), c.Description, c.CourseName, c.CourseNumber, c.DeptAbv 
        FROM Reviews r LEFT JOIN Courses c ON r.CRN = c.CRN LEFT JOIN Enrollments e 
        ON c.CRN = e.CRN 
        GROUP BY c.CRN LIMIT 15; 
        """ 
    ).fetchall()

    print([row for row in results])

# returns the most highly rated professors name and their rating for all courses (identified by the coursenumber and deptabv)
def get_highest_ratings():
    conn = db.connect()
    results = conn.execute 
    (
        """ 
        SELECT DISTINCT i.Name, s2.DeptAbv, s2.CourseNumber, s2.maxRating
        FROM (
                SELECT MAX(s1.avgRating) as maxRating, s1.DeptAbv, s1.CourseNumber
                FROM (
                        SELECT AVG(r.Rating) as avgRating, c.DeptAbv, c.CourseNumber, r.InstructorNetID 
                        FROM Reviews r 
                        LEFT JOIN Courses c ON r.CRN = c.CRN 
                        GROUP BY c.DeptAbv, c.CourseNumber, r.InstructorNetID
                    ) AS s1 
                GROUP BY s1.DeptAbv, s1.CourseNumber) AS s2 
                LEFT JOIN (
                            SELECT AVG(r2.Rating) as avgRating, c2.DeptAbv, c2.CourseNumber, r2.InstructorNetID 
                            FROM Reviews r2 LEFT JOIN Courses c2 ON r2.CRN = c2.CRN 
                            GROUP BY c2.DeptAbv, c2.CourseNumber, r2.InstructorNetID
                        ) AS s3 ON s2.maxRating = s3.avgRating AND s2.DeptAbv = s3.DeptAbv AND s2.CourseNumber = s3.CourseNumber 
                LEFT JOIN Instructors i ON s3.InstructorNetID = i.NetID
        LIMIT 15;
 
        """ 
    ).fetchall()

    print([row for row in results])
    # return results

def insert_new_task(text: str) ->  int:
    """
    Insert new task to todo table.

    Args:
    text (str): Task description

    Returns: The task ID for the inserted entry
    """

    conn = db.connect()
    query = 'Insert Into tasks (task, status) VALUES ("{}", "{}");'.format(
        text, "Todo")
    conn.execute(query)
    query_results = conn.execute("Select LAST_INSERT_ID();")
    query_results = [x for x in query_results]
    task_id = query_results[0][0]
    conn.close()

    return task_id


def remove_review_by_id(review_id: int) -> None:
    """ remove entries based on review ID """
    conn = db.connect()
    conn.execute("use squad;")
    query = 'Delete From Reviews where ReviewID={};'.format(review_id)
    conn.execute(query)
    conn.close()

#updates review with ID of selectedReviewID
def update_review(selectedReviewID, rating, comment, is_recommended, requires_textbook, CRN, instructor_netid):
    conn = db.connect()
    #not sure if this format for the ? and () works check later if not use .format()
    conn.execute 
    (
        """ 
        UPDATE Reviews 
        SET Rating = ?, Comment = ?, IsRecommended = ?, RequiresTextbook = ?, CRN = ?, InstructorNetID = ? 
        WHERE ReviewID = ?; 
        """, 
        (rating, comment, is_recommended, requires_textbook, CRN, instructor_netid, selectedReviewID)
    )
    conn.commit()
    conn.close()
def search_reviews(keyword):
    conn = db.connect()
    # conn.execute("use squad;")
    query = f"""
        SELECT * 
        FROM Reviews r 
        WHERE r.Comment like '%%{keyword}%%';
    """
    results = conn.execute(query).fetchall()
    print([row for row in results])
    return results
        
