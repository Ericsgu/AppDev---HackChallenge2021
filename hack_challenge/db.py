from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

friends_association = db.Table(
    'friends',
    db.Column('user_id1', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('user_id2', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

applying_friends_association = db.Table(
    'friends_apply',
    db.Column('user_id1', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('user_id2', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

list_events_association_table = db.Table(
    'list_events_association',
    db.Column('list_id', db.Integer, db.ForeignKey('public_list.id')),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'))
)

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    public_lists = db.relationship("User_PublicList_Association", back_populates="user", lazy='dynamic')
    
    applying_friends = db.relationship(
        'User',
        secondary=applying_friends_association,
        primaryjoin=(applying_friends_association.c.user_id1 == id),
        secondaryjoin=(applying_friends_association.c.user_id2 == id),
        lazy='dynamic',
        backref=db.backref('applying_friends_association', lazy='dynamic')
    )
    friends = db.relationship(
        'User',
        secondary=friends_association,
        primaryjoin=(friends_association.c.user_id1 == id), 
        secondaryjoin=(friends_association.c.user_id2 == id), 
        lazy='dynamic',
        backref=db.backref('friends_association', lazy='dynamic')
    )

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.password = kwargs.get('password')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "friends": [f.serialize() for f in self.friends],
            "public_list": [pl.serialize() for pl in self.public_lists]
        }

class PublicList(db.Model):
    __tablename__ = "public_list"
    id = db.Column(db.Integer, primary_key=True)
    publisher_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    list_name = db.Column(db.String, nullable=False)
    events = db.relationship("Event", cascade="delete", lazy='dynamic')
    users = db.relationship("User_PublicList_Association", back_populates="public_list", lazy='dynamic')
    
    def __init__(self, **kwargs):
        self.list_name = kwargs.get('list_name')
        self.publisher_id = kwargs.get('publisher_id')

    def serialize(self):
        return {
            "id": self.id,
            "list_name": self.list_name,
            "events": [e.serialize() for e in self.events]
        }

#https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#association-object
class User_PublicList_Association(db.Model):
    __tablename__ = 'user_publiclist_association'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key = True)
    public_list_id = db.Column(db.Integer, db.ForeignKey('public_list.id'), primary_key = True)
    is_public = db.Column(db.Boolean, nullable=False)
    user = db.relationship("User", back_populates="public_lists")
    public_list = db.relationship("PublicList", back_populates="users")
    
    def __init__(self, **kwargs):
        self.user_id = kwargs.get('user_id')
        self.is_public = kwargs.get('is_public')

    def serialize(self):
        return {
            "user_id": self.user_id,
            "public_list_id": self.public_list_id,
            "public_list": self.public_list.serialize()
        }

class Event(db.Model):
    __tablename__ = "event"
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String, nullable=False)
    position = db.Column(db.String, nullable=False)
    reminder = db.Column(db.String, nullable=False)
    public_list_id = db.Column(db.Integer, db.ForeignKey('public_list.id'))

    def __init__(self, **kwargs):
        self.company = kwargs.get('company')
        self.position = kwargs.get('position')
        self.reminder = kwargs.get('reminder')
        self.public_list_id=kwargs.get('public_list_id')
    
    def serialize(self):
        return {
            "id": self.id,
            "company": self.company,
            "position": self.position,
            "reminder": self.reminder
        }

class Image(db.Model):
    __tablename__ = "images"
    id = db.Column(db.Integer, primary_key=True)