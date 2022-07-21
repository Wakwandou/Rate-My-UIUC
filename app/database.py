import random
from app import db

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