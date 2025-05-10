Mini Blog API Project Summary
=============================

This project is a simple Mini Blog API built using Python, Flask, and SQLAlchemy. It was developed as a learning project to understand how RESTful APIs work with Flask and how to perform database operations using SQLAlchemy ORM.

What I Did:
------------

1. **Project Setup**
   - Created a virtual environment.
   - Installed required packages: Flask and SQLAlchemy.
   - Created the project structure and `app.py` file.

2. **User Management**
   - Created a User model with fields: id, username, and email.
   - Added endpoints to:
     - Create new users (`POST /users`)
     - Delete users by ID (`DELETE /users/<id>`)
     - List all users (`GET /users`)

3. **Blog Post Management**
   - Created a Post model with fields: id, title, content, and user_id (foreign key).
   - Added endpoints to:
     - Create new blog posts (`POST /posts`)
     - Delete blog posts by ID (`DELETE /posts/<id>`)
     - List all posts (`GET /posts`)

4. **Relationships**
   - Set up a one-to-many relationship between User and Post.
   - Ensured that when a user is deleted, their posts are also removed.

5. **Testing**
   - Used Insomnia to test all endpoints.
   - Verified that user and post creation, listing, and deletion work correctly.

Learning Outcomes:
------------------
- Learned how to build RESTful APIs with Flask.
- Understood how to define models and relationships in SQLAlchemy.
- Practiced using HTTP methods like GET, POST, and DELETE.
- Used Insomnia to send and inspect API requests.
- Handled errors like missing data and foreign key constraints.

This was a great beginner project to practice backend development and database interaction using Flask.

