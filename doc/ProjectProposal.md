# **Rate My UIUC**


## SQL_Squad CS411 Final Project


# <span style="text-decoration:underline;">Project Summary</span>

The project is an application that serves as a compendium for students in UIUC so that they can contribute information on courses and professors. The purpose of this project is to increase visibility of course feedback and reviews and provide a platform where students can contribute, view and visualize aggregated feedback on courses that have been taught by UIUC in order to assist them in planning for degree completion and picking their core courses or general education courses that they might want to select.

The project will be a web application where students can perform queries on both course and professor reviews that have been already entered. They will also be able to add, delete and update their own reviews for professors and courses. Since this application contains data scoped to the course and the professor, users will also be able to enter data scoped to both the course and professor.


# <span style="text-decoration:underline;">Description</span>

The application is a web app built with React. We would like to solve the problem of there currently not being a central place where students can review courses taught at UIUC. We have observed that opinions and reviews of courses and/or professors at UIUC don’t have great visibility to students; information like this is found spread across discord servers, reddit threads like r/UIUC, and it is hard for students to get a more in-depth understanding of both course specifics and the student experience of taking the course. For example, the amount of workload in the course, how accessible the professor is, how difficult the course is, when you should take the course etc. As students, we have found that information like this is incredibly useful in helping understand when or why we should be picking the course, and also what course would be most appropriate for the kind of jobs or academic specializations we might want to go into in the future.

Therefore, we want to build a database with a web app-based front end where students can retrieve course and/or professor specific feedback that details fields with information useful to the students such as course difficulty, workload, professor teaching styles etc. Students will also be able to contribute feedback to the course.

In the end, we hope to have a central location where students can access all the above detailed information, to better help them in picking courses and planning for degree completion.


# <span style="text-decoration:underline;">Usefulness</span>


Our chosen application is useful since it provides insights on courses within our university so that students can choose the right course that matches his/her learning style or preferences, as well as help them plan their academic journey. Additionally, these insights are also helpful since they are from students who already experienced taking the course. The insights would also be from legitimate UIUC students since to write a review for a course one would have to login using their netid. There are applications similar to the one we plan to develop in terms of genre but are notably different in the type of useful information they are able to provide. Notably, [www.ratemyprofessors.com](http://www.ratemyprofessors.com) which allows users to find professors from any university/school and view reviews/comments about them. However, this website focuses primarily on professors, our web application differs in that it focuses on courses within our university and various key details of each course rather than just simple reviews. For example, for each course the application will display whether or not a textbook is required and how difficult it is on a scale from 1-10 gathered from student responses. This information will be valuable for students deciding on taking the course; our application is oriented for a more in depth understanding of the course experience for students.


# <span style="text-decoration:underline;">Realness</span>

Thanks to Professor Wade, we have access to a huge [database](https://github.com/wadefagen/datasets) of courses and other pertinent information that will be utilized in our application. These datasets will be utilized to give a general overview of the course such as the average GPA and letter grade distribution which we can display through a series of graphs. In addition to these logistics, we will have a separate dataset consisting of data entered by students who have taken the class. This data will consist of the students' review of the course, which will most likely consist of a rating from 1-5, their grade (optional input), the instructor’s name, and any comments (optional input). The data type of the student reviews will be an INT for the rating (1-5), a DOUBLE CHAR for the letter grade (A+ to F-), a STRING for the instructor name, and a STRING for the review. Furthermore, we can also gather additional information from the students such as average hours spent per week on the course, if there are required readings/textbooks, and if they attended office hours often. With all this data collected from students, we can provide a meaningful review of the course for future students to view.


# <span style="text-decoration:underline;">Functionality</span>

In the startup page, users will have the option to either create a new account with their netID and password, sign in with an existing account, or continue as a guest. An account is needed in order to update or submit any feedback to the SQL database. This is to ensure that reviews will be provided by actual students and not by spam accounts. After picking an option from the startup page, anyone will be able to input a query into a GUI search bar, which will perform a keyword search based on either the course number or the instructor’s name. Users will be able to scope their reviews to both course and instructor specific entries, or simply just scope them within the course or professor. Once the query has been fulfilled, the application will display student reviews and information pertaining to the course which will be queried from the SQL database of past student reviews. 

Students with a valid account will also be able to add, delete, or modify their own reviews, but they will not be able to delete or update entries that are not their own. Furthermore, in the profile tab, students with accounts will be able to view all the reviews they have made, along with the number of upvotes their reviews garnered (a system where students can give feedback on other students reviews to give a better indicator for how useful/accurate the review was).

Aggregated fields like course ratings from 1-5 and the average course GPA will be updated at every new entry/update via triggers. There will be different pages pertaining to the different functionalities that the users will use to interact with the database.


# <span style="text-decoration:underline;">UI Mockup</span>

[SQL_Squad Proposal Lofi Mockup](https://docs.google.com/presentation/d/14tPVDDgfDsw-Gjd7nUmXhJccBpakJ6PxRahRtBFt_lc/edit?usp=sharing)


# <span style="text-decoration:underline;">Work Distribution:</span>

**Sri (sra8)**: Search bar, displaying db information, UI beautification, GCP hosting, Search the database using a keyword search and stored procedure requirements

**Fang Yi (fyl2)**: Login Page, sign in page, creative component, Transaction requirements

**Alex (kwandou2)**: SQL Schemas, advanced SQL queries, Implement at least four main tables, providing DDL commands, Data insertion (1000 rows **each in **three of the tables), advanced database program, and trigger requirements

**Samuel (sydu2)**: Course and professor reviews/comments, editing existing reviews/comments, Insert new records (rows) to the database, update records on the database and Delete rows from the database

Each member is responsible for their own component of the web app and will do all the frontend and backend work for the feature to function. However, they are free to ask others for help if needed.


# <span style="text-decoration:underline;">Potential Creative Components</span>

We could potentially illustrate some simple visualizations of how the average GPA or rating of this course has changed over time, in order to help students, and even instructors, better understand how the course has progressed over time.

More complex creative components would include sentiment analysis on all of the reviews on a course or a professor to understand if reviews are largely positive or negative or a summarization algorithm to distill key insights from all the reviews that have been given to a course or professor. In order to achieve this, we will likely use available sentiment analysis or summarization libraries.
