from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

from config import db
from config import db, bcrypt

# Models go here!

#Employee login
class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = ('-users.user', '-_password_hash',)

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String)
    

    users = db.relationship('User', backref='user')

    @hybrid_property
    def password_hash(self):
        raise AttributeError('Password hashes may not be viewed.')

    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(
            password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, password.encode('utf-8'))

    def __repr__(self):
        return f'<User {self.username}>'
    
    
    class Order(db.Model, SerializerMixin):
    __tablename__ = 'users'

    



    def __repr__(self):
        return f'<User {self.username}>'
    