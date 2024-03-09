# FlaskLoginAuthentication

## Tues 3/12

Flask - Login/Authentication - Viet & Hung Tran

## Usage

1. For macOS/Linux

```
git clone https://github.com/AugustanaCSC490Spring2024/FlaskLoginAuthentication.git
cd FlaskLoginAuthentication
python3 -m venv venv
```

2. Activate the environment

```
source venv/bin/activate
```

3. Install the requirements

```
pip install -r requirements.txt
```

## Tutorial to add user authentication in flask app

To add Flask-Login for authentication in a Flask app starting from a blank Flask application, follow these steps:

### 1. Set Up Your Flask App

First, ensure you have Flask installed. If not, you can install it using pip:

```bash
pip install Flask
```

Create a new Python file for your application, for example, `app.py`, and initialize your Flask app:

```python:app.py
from flask import Flask

app = Flask(__name__)
```

### 2. Install Flask-Login and Flask-SQLAlchemy

Flask-Login will manage user sessions for us, and Flask-SQLAlchemy will be used for the database:

```bash
pip install flask-login flask-sqlalchemy
```

### 3. Configure Your App

Add configuration for your database and secret key:

```python:app.py
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///yourdatabase.db"
app.config["SECRET_KEY"] = "your_secret_key"
```

### 4. Initialize Flask-Login and Flask-SQLAlchemy

```python:app.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
```

### 5. Create User Model

Create a user model that inherits from `UserMixin` and `db.Model`:

```python:app.py
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
```

### 6. Initialize Database

Before running your app, make sure to create the database:

```python:app.py
with app.app_context():
    db.create_all()
```

### 7. User Loader Function

Define a user loader function for Flask-Login:

```python:app.py
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
```

### 8. Create Authentication Routes

Create routes for login, logout, and registration. Here's an example for a login route:

```python:app.py
from flask import request, redirect, url_for, render_template, flash
from flask_login import login_user, logout_user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.password == request.form['password']:
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')
```

### 9. Protect Routes

Use `@login_required` decorator to protect routes that require authentication:

```python:app.py
from flask_login import login_required

@app.route('/secret')
@login_required
def secret():
    return 'Only authenticated users can see this!'
```

### 10. Protect your user password
Use `from werkzeug.security import generate_password_hash, check_password_hash` to add a layer of protection into user password

where `generate_password_hash(request.form.get("password"), method='scrypt')` will request the password in the registration and convert that into a hashed form with the 'scrypt' method from werkzeug library.

to verify the password when the user login use the condition to check `check_password_hash(user.password, request.form.get("password"))`


### 11. Run Your App

Finally, run your Flask app:

```python:app.py
if __name__ == "__main__":
    app.run(debug=True)
```

Remember, this is a basic setup. In a real application, you should never store plain text passwords in your database. Use a library like Werkzeug to hash passwords before storing them.
