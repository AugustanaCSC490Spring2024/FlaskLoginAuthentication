from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SECRET_KEY"] = "abc"
db = SQLAlchemy()

# TODO: some configurations here


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)


db.init_app(app)


with app.app_context():
    db.create_all()

# TODO: add user_loader here


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = Users(username=request.form.get("username"),
                     password=request.form.get("password"))  # TODO: should not save password w/out encryption
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("signup.html")


@app.route('/profile')
def profile():
    pass


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = Users.query.filter_by(
            username=request.form.get("username")).first()
        # TODO: Make sure this secure
        if user.password == request.form.get("password"):
            return redirect(url_for("home"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    # TODO: Code here
    return redirect(url_for("home"))


@app.route("/")
def home():
    return render_template("home.html")


if __name__ == "__main__":
    app.run()
