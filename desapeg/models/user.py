from extensions import db

class User(db.Model):
    __tablename__ = 'users'

    User_ID = db.Column('user_id', db.Integer, primary_key=True)
    Name = db.Column('name', db.String(30))
    Tel = db.Column('tel', db.String(12))
    Email = db.Column('email', db.String(30))
    Password = db.Column('password', db.String(60))