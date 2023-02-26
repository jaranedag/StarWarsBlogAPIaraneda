from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
   
    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)        
    name = db.Column(db.String(120), unique=True, nullable=False)
    fav_people = db.relationship("Fav_People", backref="people")

    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }
class Fav_People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    people_name = db.Column(db.String(120), db.ForeignKey("people.name"))
    user_fav = db.Column(db.String(120), db.ForeignKey("user.email"))
    fav_people = db.relationship("People")
    rel_user = db.relationship("User")   

    def serialize(self):
        return {
            "id": self.id,
            "people_name": self.people_name,
        }

class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)        
    name = db.Column(db.String(120), unique=True, nullable=False)
    rel_planets = db.relationship("Fav_Planets", backref="planets")
    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        } 
        
class Fav_Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    planets_name = db.Column(db.String(120), db.ForeignKey("planets.name"))
    user_fav = db.Column(db.String(120), db.ForeignKey("user.email"))
    rel_planets = db.relationship("Planets")
    rel_user = db.relationship("User")   

    def serialize(self):
        return {
            "id": self.id,
            "name": self.planets_name,
        } 
