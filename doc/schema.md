Entities: 
Users(Username:VARCHAR(100) [PK], NetID:VARCHAR(50), Password: VARCHAR(100), IsGuest:BOOLEAN)

Reviews(ReviewID:VARCHAR(50) [PK], Rating:REAL, Comment:VARCHAR(500), IsRecommended:BOOLEAN, RequiresTextbook:BOOLEAN, Upvotes:INT, Downvotes:INT, UserNetID:VARCHAR(100) [FK to Users.NetID], CRN:VARCHAR(6) [FK to Courses.CRN], InstructorNetID:VARCHAR(50) [FK to Instructors.NetID])

Courses(CRN:VARCHAR(6) [PK], CourseName:VARCHAR(50), CourseNumber:VARCHAR(3), Description:VARCHAR(500), DeptAbv:VARCHAR(4) [FK to Departments.DeptAbv])

Instructors(NetID:VARCHAR(50) [PK], Name:VARCHAR(100), DeptAbv:VARCHAR(4) [FK to Departments.DeptAbv])

Departments(DeptAbv:VARCHAR(4) [PK], DeptName:VARCHAR(50), Location:VARCHAR(100), URL:VARCHAR(50), PhoneNumber:VARCHAR(20))

Relationships:
Enrolled(YearTerm:VARCHAR(10) [PK], GPA:REAL, UserNetID:VARCHAR(50) [PK, FK to Users.NetID], InstrNetID:VARCHAR(50) [PK, FK to Instructors.NetID], CRN:VARCHAR(4) [PK, FK to Courses.CRN])
