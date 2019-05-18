from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5


class Bruger(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brugernavn = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return f'Bruger: {self.brugernavn}' 

    def set_password(self, password):
    	self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return Bruger.query.get(int(id))


class By(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bruger_id = db.Column(db.Integer, db.ForeignKey('bruger.id'))
    navn = db.Column(db.String(150), index=True)

    def __repr__(self):
        return f'{self.bruger_id} | {self.navn}' 
