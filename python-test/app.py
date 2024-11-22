from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# ユーザーモデル
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# フォローモデル
class Follower(db.Model):
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

# ログインマネージャー
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# データベース初期化
with app.app_context():
    db.create_all()

# ホームページ
@app.route('/')
def index():
    if current_user.is_authenticated:
        followed_users = [
            f.followed_id for f in Follower.query.filter_by(follower_id=current_user.id).all()
        ]
        users = User.query.all()
        return render_template('index.html', users=users, followed_users=followed_users)
    return redirect(url_for('login'))

# ユーザー登録
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(email=email).first():
            flash('Email already registered!')
            return redirect(url_for('register'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))

    return render_template('register.html')

# ログイン
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password.')

    return render_template('login.html')

# ログアウト
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('login'))

# フォローAPI
@app.route('/api/follow', methods=['POST'])
@login_required
def follow():
    data = request.get_json()
    followed_id = data.get('followed_id')

    if Follower.query.filter_by(follower_id=current_user.id, followed_id=followed_id).first():
        return jsonify({'message': 'Already following'}), 400

    new_follow = Follower(follower_id=current_user.id, followed_id=followed_id)
    db.session.add(new_follow)
    db.session.commit()

    return jsonify({'message': 'Followed successfully'}), 200

# アンフォローAPI
@app.route('/api/unfollow', methods=['POST'])
@login_required
def unfollow():
    data = request.get_json()
    followed_id = data.get('followed_id')

    follow = Follower.query.filter_by(follower_id=current_user.id, followed_id=followed_id).first()
    if not follow:
        return jsonify({'message': 'Not following'}), 400

    db.session.delete(follow)
    db.session.commit()

    return jsonify({'message': 'Unfollowed successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
