from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from api.models.database import BaseModel


class User(BaseModel.db.Model):
    __tablename__ = 'users'
    AppDb = BaseModel.db

    id = AppDb.Column(AppDb.Integer, primary_key=True)
    first_name = AppDb.Column(AppDb.String(65), nullable=False)
    last_name = AppDb.Column(AppDb.String(65), nullable=False)
    email = AppDb.Column(AppDb.String(65), index=True, unique=True, nullable=False)
    password = AppDb.Column(AppDb.String(128), nullable=False)
    role_id = AppDb.Column(AppDb.Integer, AppDb.ForeignKey('role.id', ondelete='SET NULL'), nullable=True)
    housedata_id = AppDb.Column(AppDb.Integer, AppDb.ForeignKey('housedata.id', ondelete='SET NULL'), nullable=True)
    # Fields to help in audits
    created_at = AppDb.Column(AppDb.DateTime, nullable=False, default=datetime.now)
    created_by = AppDb.Column(AppDb.String(65), nullable=True)
    updated_at = AppDb.Column(AppDb.DateTime, nullable=True)
    updated_by = AppDb.Column(AppDb.String(65), nullable=True)
    deleted_at = AppDb.Column(AppDb.DateTime, nullable=True)
    deleted_by = AppDb.Column(AppDb.String(65), nullable=True)
    is_deleted = AppDb.Column(AppDb.Boolean, nullable=False, default=False)

    # relationship(s)
    sample_owner = AppDb.relationship('Sample', backref='owner', lazy='dynamic')
    publication = AppDb.relationship('Publication', back_populates='user')

    def __repr__(self):
        return '<< User: (name={0} || email={1}) >>'.format(self.first_name, self.email)

    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)

    def verify_password(self, password):
        """
        Checks if a provided password is the correct user's password
        :param password: Provided password by user
        :return: True is the password is correct, False otherwise
        """
        return check_password_hash(pwhash=self.password, password=password)

    @staticmethod
    def user_exists(email):
        """
            Checks if the user already has an account
        :param email:
        :return: True if they have an account, False otherwise
        """
        if User.query.filter(
                User.email == email
        ).first():
            return True
        return False
