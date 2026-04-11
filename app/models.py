from datetime import datetime
from database import db

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))

    pregnancy = db.Column(db.String(30))
    smoking = db.Column(db.String(30))

    hba1c = db.Column(db.String(50))
    bp = db.Column(db.String(50))
    cholesterol = db.Column(db.String(50))
    duration = db.Column(db.String(50))

    image_path = db.Column(db.String(300))

    prediction = db.Column(db.String(100))
    confidence = db.Column(db.Float)

    heatmap = db.Column(db.Text)

    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Patient {self.name} - {self.prediction}>"