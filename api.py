from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

application = Flask(__name__)
app = application
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flights.db'
db = SQLAlchemy(app)

class Flight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    airline = db.Column(db.String(50))
    arrival_airport = db.Column(db.String(50))
    arrival_time = db.Column(db.DateTime)

@app.route('/flights', methods=['GET'])
def get_flights():
    arrival_airport = request.args.get('arrival_airport', default=None, type=str)
    arrival_date = request.args.get('arrival_date', default=None, type=str)
    
    query = db.session.query(Flight)
    
    if arrival_airport:
        query = query.filter(Flight.arrival_airport == arrival_airport)

    if arrival_date:
        arrival_date = datetime.strptime(arrival_date, "%Y-%m-%d")
        query = query.filter(db.func.date(Flight.arrival_time) == arrival_date.date())

    flights = query.all()

    return jsonify([{ 'id': f.id, 'airline': f.airline, 
                      'arrival_airport': f.arrival_airport, 
                      'arrival_time': str(f.arrival_time) } for f in flights])

if __name__ == '__main__':
    app.run(debug=True)
