from flask import Flask, request, jsonify 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Post {self.title}>' 

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Comment {self.id}>'
           
with app.app_context():
    db.create_all()

@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    
    if 'username' not in data:
        return jsonify({'message': 'Username is required'}), 400
    
    if 'email' in data and User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already exists'}), 400

    new_user = User(username=data['username'], email=data.get('email', None))
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully!"}), 201

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()  
    user_list = []
    for user in users:
        user_list.append({
            'id': user.id,
            'username': user.username,
            'email': user.email
        })
    return jsonify(user_list), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({"username": user.username, "email": user.email})

@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    db.session.commit()
    return jsonify({"message": "User updated successfully!"})

@app.route('/post', methods=['POST'])
def create_post():
    data = request.get_json()
    
    title = data.get('title')
    content = data.get('content')
    user_id = data.get('user_id')

    if not all([title, content, user_id]):
        return jsonify({"message": "Incomplete data sent"}), 400

    user = User.query.get(data['user_id'])
    
    if not user:
        return jsonify({"message": "user not found!"}), 404

    new_post = Post(title=data['title'], content=data['content'], user_id=data['user_id'])
    db.session.add(new_post)
    db.session.commit()

    return jsonify({"message": "Blog post created successfully!"}), 201

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"message": "User not found!"}), 404
    
    Post.query.filter_by(user_id=user_id).delete()
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({"message": "User deleted successfully!"}), 200

@app.route('/post/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify({"title": post.title, "content": post.content, "date_posted": post.date_posted})

@app.route('/post/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    data = request.get_json()
    
    if post.user_id != data['user_id']:
        return jsonify({"message": "You can only update your own posts!"}), 403
    
    post.title = data.get('title', post.title)
    post.content = data.get('content', post.content)
    db.session.commit()
    return jsonify({"message": "Post updated successfully!"})

@app.route('/post/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": "Post deleted successfully!"})

@app.route('/post/<int:post_id>/comments', methods=['POST'])
def create_comment(post_id):
    data = request.get_json()
    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(data['user_id'])

    new_comment = Comment(content=data['content'], post_id=post.id, user_id=user.id)
    db.session.add(new_comment)
    db.session.commit()
    
    return jsonify({"message": "Comment added successfully!"}), 201

@app.route('/post/<int:post_id>/comments', methods=['GET'])
def get_comments(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post.id).all()
    return jsonify([{"content": comment.content, "user_id": comment.user_id} for comment in comments])

@app.route('/')
def home():
    return "Welcome to Mini Blog API!"

if __name__ == '__main__':
    app.run(debug=True)
