from urllib import request
import requests

from forms.user import RegisterForm, LoginForm
from flask_login import LoginManager, login_user, login_required, logout_user

from data import db_session
from data.users import User

from flask import Flask, render_template, redirect, make_response, session

from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/")
def index():
    db_session.global_init(f"db/WT_users.db")
    months = ["Января", "Февраля", "Марта",
              "Апреля", "Мая", "Июня",
              "Июля", "Августа", "Сентября",
              "Октября", "Ноября", "Декабря"]

    WEATHER_API_KEY = "137f14bfa0d3400a8f9183700251404"
    city = "Москва"
    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}&lang=ru"
    response = requests.get(url)
    current_weather_data = response.json()["current"]
    date = list(map(int, current_weather_data["last_updated"].split()[0].split("-")))
    current_weather_data["localtime"] = " ".join([str(date[2]), str(months[date[1] % 12 - 1])])

    url = f"http://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={city}&days=1&lang=ru"
    response = requests.get(url)
    hourly_forecast_weather_data = response.json()["forecast"]["forecastday"][0]["hour"]
    now = datetime.now().hour
    for hour in hourly_forecast_weather_data:
        hour["time"] = hour["time"].split()[1]

    hourly_forecast_weather_data = hourly_forecast_weather_data[now:]

    url = f"http://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={city}&days=3&lang=ru"
    response = requests.get(url)
    daily_forecast_weather_data = response.json()["forecast"]["forecastday"]

    for day in daily_forecast_weather_data:
        date = list(map(int, day["date"].split("-")))
        day["date"] = " ".join([str(date[2]), str(months[date[1] % 12 - 1])])

    return render_template("index.html",
                           current_weather_data=current_weather_data,
                           daily_forecast_weather_data=daily_forecast_weather_data,
                           hourly_forecast_weather_data=hourly_forecast_weather_data)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            home_city=form.home_city.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    db_session.global_init("db/WT_users.db")
    app.run()


if __name__ == '__main__':
    main()
