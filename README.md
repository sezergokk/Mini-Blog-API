# Mini Blog API – Insomnia Testing Info

This API runs locally on the following URL:

http://localhost:5000


### How to Test with Insomnia

To test this API using Insomnia:

1. Open Insomnia.
2. Create a new request collection.
3. Use the base URL `http://localhost:5000`.

### Available Endpoints

#### Users
- `GET /users` – List all users
- `POST /users` – Create a new user
- `DELETE /users/<id>` – Delete user by ID

#### Posts
- `GET /posts` – List all posts
- `POST /posts` – Create a new post
- `DELETE /posts/<id>` – Delete post by ID

Make sure the Flask app is running before testing.
