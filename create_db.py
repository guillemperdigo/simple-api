import pandas as pd
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__)
app = application
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flights.db'
db = SQLAlchemy(app)

class Flight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    airline = db.Column(db.String(50))
    arrival_airport = db.Column(db.String(50))
    arrival_time = db.Column(db.DateTime)

with app.app_context():
    db.create_all()

    df = pd.read_csv('flights.csv', parse_dates=['arrival_time'])
    try:
        for index, row in df.iterrows():
            flight = Flight(id=row['id'], airline=row['airline'], 
                            arrival_airport=row['arrival_airport'], 
                            arrival_time=row['arrival_time'])
            db.session.add(flight)
        db.session.commit()
    except Exception as e:
        print("Failed to add data to database.")
        print(e)

