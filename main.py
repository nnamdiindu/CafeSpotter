import os
from dotenv import load_dotenv
from flask import Flask, redirect, url_for, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Boolean, select
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from forms import EditForm, RegisterForm, LoginForm

load_dotenv()
app = Flask(__name__)
bootstrap = Bootstrap5(app)

class Base(DeclarativeBase):
    pass

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"
app.secret_key = os.environ.get("SECRET_KEY")
db = SQLAlchemy(model_class=Base)
db.init_app(app)
login_manager = LoginManager(app)

class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(100), nullable=False)

class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def home():
    all_cafes = db.session.execute(db.select(Cafe)).scalars().all()
    return render_template("index.html", cafes=all_cafes)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    all_cafes = db.session.execute(db.select(Cafe)).scalars().all()

    form = RegisterForm()
    if form.validate_on_submit():
        hash_and_salted_password = generate_password_hash(
            password=form.password.data,
            method="pbkdf2:sha256",
            salt_length=8
        )
        new_user = User(
            name=form.name.data,
            email=form.email.data,
            password=hash_and_salted_password
        )
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return render_template("index.html", current_user=current_user, cafes=all_cafes)
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = db.session.execute(select(User).where(User.email == email)).scalar_one_or_none()
        if user:
            if email != user.email:
                flash("Email doesn't exist, please register.")
                return redirect(url_for("register"))
        else:
            flash("Email doesn't exist, please register.")
            return redirect(url_for("register"))

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("home"))
        else:
            flash("Incorrect password, please try again.")
            # return redirect(url_for("login"))
    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/edit/<int:cafe_id>", methods=["POST", "GET"])
@login_required
def edit(cafe_id):
    form = EditForm()
    selected_cafe = db.get_or_404(Cafe, cafe_id)
    if form.validate_on_submit():
        selected_cafe.map_url = form.map_url.data
        selected_cafe.img_url = form.img_url.data
        selected_cafe.has_wifi = form.wifi.data
        selected_cafe.seats = form.seats.data
        selected_cafe.has_toilet = form.toilets.data
        selected_cafe.has_sockets = form.sockets.data
        selected_cafe.coffee_price = form.coffee_price.data
        selected_cafe.location = form.location.data
        selected_cafe.name = form.name.data
        selected_cafe.can_take_calls = form.allow_calls.data
        db.session.commit()
        return redirect(url_for("home"))

    # Populating data of the selected cafe from the database
    form.allow_calls.data = selected_cafe.can_take_calls
    form.name.data = selected_cafe.name
    form.location.data = selected_cafe.location
    form.wifi.data = selected_cafe.has_wifi
    form.img_url.data = selected_cafe.img_url
    form.coffee_price.data = selected_cafe.coffee_price
    form.seats.data = selected_cafe.seats
    form.toilets.data = selected_cafe.has_toilet
    form.sockets.data = selected_cafe.has_sockets
    form.map_url.data = selected_cafe.map_url

    return render_template("edit.html", form=form)


@app.route("/delete/<int:cafe_id>")
@login_required
def delete(cafe_id):
    selected_cafe = db.get_or_404(Cafe, cafe_id)
    db.session.delete(selected_cafe)
    db.session.commit()
    return redirect(url_for("home"))



if __name__ == "__main__":
    app.run(debug=True)