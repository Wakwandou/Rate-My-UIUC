Guest(TempID:VARCHAR(200) [PK], TempUsername:VARCHAR(200))

Registrations(NetID:VARCHAR(10) [PK], SemYear:VARCHAR(5) [PK], CRN:VARCHAR(6) [FK to Course.CRN])

User(NetID:VARCHAR(10) [PK], Username:VARCHAR(200))

Instructor(NetID:VARCHAR(200) [PK], Name:VARCHAR(200), AverageScore:VARCHAR(200))

Course(CRN:VARCHAR(6) [PK], SemYear:VARCHAR(5) [PK], InstructorNetID:VARCHAR(200) [PK][FK to Instructor.NetID], Department:VARCHAR(200), AverageGPA:REAL, AverageScore:REAL, CourseName:VARCHAR(200))

Review(ReviewID:VARCHAR(200) [PK], CRN:VARCHAR(6), InstructorNetID:VARCHAR(10) [FK to Instructor.NetID], Score:REAL, Comment:VARCHAR(500), GPA:REAL, TakeAgain:BOOLEAN, TextBook:VARCHAR(200), Upvotes:INT, Downvotes:INT, NetID:VARCHAR(10) [FK to User.NetID])
