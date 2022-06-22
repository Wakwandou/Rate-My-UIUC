# Rate My UIUC


## SQL_Squad CS411 Final Project


# Project Summary

The project is an application that serves as a compendium for students in UIUC so that they can contribute information on courses and professors. The purpose of this project is to increase visibility of course feedback and reviews and provide a platform where students can contribute, view and visualize aggregated feedback on courses that have been taught by UIUC in order to assist them in planning for degree completion and picking their core courses or general education courses that they might want to select.

The project will be a web application where students can perform queries on both course and professor reviews that have been already entered. They will also be able to add, delete and update their own reviews for professors and courses. Since this application contains data scoped to the course and the professor, users will also be able to enter data scoped to both the course and professor.



# Description

The application is a web app built with React. We would like to solve the problem of there currently not being a central place where students can review courses taught at UIUC. We have observed that opinions and reviews of courses and/or professors at UIUC don’t have great visibility to students; information like this is found spread across discord servers, reddit threads like r/UIUC, and it is hard for students to get a more in-depth understanding of both course specifics and the student experience of taking the course. For example, the amount of workload in the course, how accessible the professor is, how difficult the course is, when you should take the course etc. As students we have found that information like this is incredibly useful in helping understand when or why we should be picking the course, and also what course would be most appropriate for the kind of jobs or academic specializations we might want to go into in the future.

Therefore, we want to build a database with a webapp-based front end where students can retrieve course and/or professor specific feedback that details fields with information useful to the students such as course difficulty, workload, professor teaching styles etc. Students will also be able to contribute feedback to the course.

In the end, we hope to have a central location where students can access all the above detailed information, to better help them in picking courses and planning for degree completion.


# Usefulness


Our chosen application is useful since it provides insights on courses within our university so that students can choose the right course that matches his/her learning style or preferences, as well as help them plan their academic journey. Additionally, these insights are also helpful since they are from students who already experienced taking the course. The insights would also be from legitimate UIUC students since to write a review for a course one would have to login using their netid. There are applications similar to the one we plan to develop in terms of genre but are notably different in the type of useful information they are able to provide. Notably, [www.ratemyprofessors.com](http://www.ratemyprofessors.com) which allows users to find professors from any university/school and view reviews/comments about them. However, this website focuses primarily on professors, our web application differs in that it focuses on courses within our university and various key details of each course rather than just simple reviews. For example, for each course the application will display whether or not a textbook is required and how difficult it is on a scale from 1-10 gathered from student responses. This information will be valuable for students deciding on taking the course; our application is oriented for a more in depth understanding of the course experience for students.


# Realness

Our data will be entered by students in the school. We will be obtaining the data by opening it up to friends who have taken the courses and are willing to contribute their opinions and reviews. The data type we will be using will be Strings since students type out course reviews, with the exception of a 1 to 5 star rating that will be stored as an Integer. Furthermore, we also plan to store and display other information such as weekly hours spent on the course, average grade, average course rating, if there are required readings/textbooks and if they are necessary, and a list of professors that teach the course. 


# Functionality

Users will first be able to create a new account with their netID and password before they are able to retrieve, update or submit any entries to the system. Returning users will be able to sign into the application. Following the signing up, A user will be able to input in the search bar, performing a keyword search for either the course number or the professor’s name and search for reviews and information pertaining to the course which will be queried from a SQL database. Students will also be able to add their own reviews for courses and professors, thereby inserting new records into the database. They will be able to scope their reviews to both course and professor specific entries, or simply just scope them within the course or professor.

Students will be able to delete and/or update whatever they have submitted to the application, but they will not be able to delete or update entries that are not theirs.

Aggregated fields like course ratings from 1-5 and the average course GPA will be updated at every new entry/update via triggers. There will be different pages pertaining to the different functionalities that the users will use to interact with the database.


# UI Mockup

[https://docs.google.com/presentation/d/14tPVDDgfDsw-Gjd7nUmXhJccBpakJ6PxRahRtBFt_lc/edit?usp=sharing](https://docs.google.com/presentation/d/14tPVDDgfDsw-Gjd7nUmXhJccBpakJ6PxRahRtBFt_lc/edit?usp=sharing) 


# Work Distribution:

**Sri**: Search bar, displaying db information, UI beautification, GCP hosting, Search the database using a keyword search and stored procedure requirements

**Fang Yi**: Login Page, sign in page, creative component, Transaction requirements

**Alex**: SQL Schemas, advanced SQL queries, Implement at least four main tables, providing DDL commands, Data insertion (1000 rows **each in **three of the tables.), advanced database program, and trigger requirements

**Samuel**: Course and professor reviews/comments, editing existing reviews/comments, Insert new records (rows) to the database, Update records on the database and Delete rows from the database

Each member will own each component of the web app and will do all the frontend and backend work for the feature to function.


# Potential Creative Components

We could potentially illustrate some simple visualizations of how the average GPA or rating of this course has changed over time, in order to help students better understand how the course has progressed over time.

More complex creative components would include sentiment analysis on all of the reviews on a course or a professor to understand if reviews are largely positive or negative or a summarization algorithm to distill key insights from all the reviews that have been given to a course or professor. In order to achieve this, we will likely use available sentiment analysis or summarization libraries.