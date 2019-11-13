from api.models.database import BaseModel
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
from api.models.role import Role

class User (UserMixin, BaseModel.db.Model):
    __tablename__='users'
    AppDb = BaseModel.db
    id = AppDb.Column(AppDb.Integer, primary_key = True)
    role_id = AppDb.Column(AppDb.Integer, AppDb.ForeignKey('role.id'))
    email = AppDb.Column(AppDb.String(65), index = True, unique = True )
    password_hash = AppDb.Column(AppDb.String(128))
    firstname = AppDb.Column(AppDb.String(65), nullable = False)
    lastname = AppDb.Column(AppDb.String(65), nullable = False)
    #samples = AppDb.relationship('Sample', backref='', lazy='dynamic')


    def __repr__():
        return '<User {}>'.format(self.firstname, self.lastname)

    def set_password (self, password) :
        self.password_hash = generate_password_hash(password) 

    def check_password (self, password):
        return check_password_hash (self.password_hash, password)

