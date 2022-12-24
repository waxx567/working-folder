from flask import Flask, redirect, render_template, request, session, url_for, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "makeitcomplicated"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=5)

db = SQLAlchemy(app)

CLIENT = "gaslitcatfish web designs"
CLIENT_1 = "gaslit"
CLIENT_2 = "catfish"
CLIENT_3 = "designs"

BUILDER = "fivefiftyfive ltd"
BUILDER_1 = "webworld"
YEAR = "2022"


class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email


@app.route("/")
def home():
    return render_template("index.html", client=CLIENT, client_1=CLIENT_1, client_2=CLIENT_2, year=YEAR, builder=BUILDER, builder_1=BUILDER_1)


@app.route("/view")
def view():
    return render_template("view.html", client=CLIENT, client_1=CLIENT_1, client_2=CLIENT_2, year=YEAR, builder=BUILDER, builder_1=BUILDER_1, values=users.query.all())


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user

        found_user = users.query.filter_by(name=user).first()
        if found_user:
            session["email"] = found_user.email
        else:
            usr = users(user, None)
            db.session.add(usr)
            db.session.commit()

        flash(f"{user} has successfully logged in")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("You are already logged in")
            return redirect(url_for("user"))

        return render_template("login.html", client=CLIENT, client_1=CLIENT_1, client_2=CLIENT_2, client_3=CLIENT_3, year=YEAR, builder=BUILDER, builder_1=BUILDER_1)


@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]

        if request.method == "POST":
            email = request.form["email"]
            found_user = users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit()
            session["email"] = email
            flash("Email saved!")
        else:
            if "email" in session:
                email = session["email"]

        return render_template("user.html", client=CLIENT, client_1=CLIENT_1, client_2=CLIENT_2, client_3=CLIENT_3, year=YEAR, builder=BUILDER, builder_1=BUILDER_1, email=email)
    else:
        flash("You are not logged in", "info")
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
    flash("You have logged out", "info")
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))


@app.route("/services")
def services():
    return render_template("services.html", client=CLIENT, client_1=CLIENT_1, client_2=CLIENT_2, client_3=CLIENT_3, year=YEAR, builder=BUILDER, builder_1=BUILDER_1)


@app.route("/test")
def test():
    return render_template("test.html", client=CLIENT, client_1=CLIENT_1, client_2=CLIENT_2, client_3=CLIENT_3, year=YEAR, builder=BUILDER, builder_1=BUILDER_1)


@app.route("/build")
def build():
    return render_template("build.html", client=CLIENT, client_1=CLIENT_1, client_2=CLIENT_2, client_3=CLIENT_3, year=YEAR, builder=BUILDER, builder_1=BUILDER_1)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
