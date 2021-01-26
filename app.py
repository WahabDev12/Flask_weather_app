from flask import Flask,render_template,redirect,request,url_for
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
db = SQLAlchemy(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///weather.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

class City(db.Model):
    id  = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(200),nullable = False)

@app.route("/",methods=["POST","GET"])
def index():
    if request.method == "POST":
        new_city = request.form.get("city")
        if new_city:
            new_city_obj = City(name =new_city)
            db.session.add(new_city_obj) 
            db.session.commit()
    cities = City.query.all()
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=0b5c273b022c1f3199c520878cc91d66"
    
    weather_data = []
    for city in cities:
        r = requests.get(url.format(city.name)).json()

        weather = {
            "city": city.name,
            "temperature":r["main"]["temp"],
            "description":r["weather"][0]["description"],
            "icon":r["weather"][0]["icon"]
        }
        weather_data.append(weather)
    return render_template("index.html",weather_data = weather_data)

@app.route("/delete/<int:weather_id>")
def delete(weather_id):
    city = City.query.filter_by(id = weather_id).first()
    db.session.delete(city)
    db.session.commit()
    return render_template("index.html")



if __name__ == "__main__":
    db.create_all()
    app.run(debug = True)   