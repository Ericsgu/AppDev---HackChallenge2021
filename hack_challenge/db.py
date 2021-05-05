from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



# user 2 user
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
    uid = db.Column(db.String, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    public_lists = db.relationship("User_PublicList_Association", back_populates="user")
    
    # 已有好友
    friends = db.relationship(
        'User',
        secondary=friends_association,
        primaryjoin=(applying_friends_association.user_id1 == id),
        secondaryjoin=(applying_friends_association.user_id2 == id),
        lazy='dynamic',
        backref=db.backref('applying_friends_association', lazy='dynamic')
    )
    # 好友申请
    applying_friends = db.relationship(
        'User',
        secondary=friends_association,
        primaryjoin=(friends_association.user_id1 == id),  # 多对多中）用于从子对象查询其父对象的 condition（child.parents）
        secondaryjoin=(friends_association.user_id2 == id),  # 多对多中）用于从父对象查询其所有子对象的 condition（parent.children）
        lazy='dynamic',  # 延迟求值，这样才能用 filter_by 等过滤函数
        backref=db.backref('friends_association', lazy='dynamic')
    )

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.uid = kwargs.get('uid')
        self.password = kwargs.get('password')




class PublicList(db.Model):
    __tablename__ = "public_list"
    id = db.Column(db.Integer, primary_key=True)
    publisher_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    listName = db.Column(db.String, nullable=False)
    events = db.relationship("Event", cascade="delete")
    users = db.relationship("User_PublicList_Association", back_populates="publiclist")
    
    def __init__(self, **kwargs):
        self.listname = kwargs.get('listname')
        self.publisher_id = kwargs.get('publisher_id')

    def serialize(self):
        return {
            "id": self.id,
            "listName": self.listName,
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
        self.is_public = kwargs.get('is_public')
    def serialize(self):
        return {
            "userid": self.user_id,
            "public_list_id": self.public_list_id,
            "public_list": [l.serialize() for l in self.public_list]    
        }

class Event(db.Model):
    __tablename__ = "event"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    event_time = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String, nullable=False)
    public_list_id = db.Column(db.Integer, db.ForeignKey('public_list.id'))
    
    def __init__(self, **kwargs):
        self.title = kwargs.get('title')
        self.description = kwargs.get('description')
        self.event_time = kwargs.get('event_time')
        self.public_list_id=kwargs.get('public_list_id')
    
    def serialize(self):
        return {
            'id':self.id,
            'title': self.title,
            'description': self.description,
            'event_time': self.event_time
        }

class Image(db.Model):
    __tablename__ = "images"
    id = db.Column(db.Integer, primary_key=True)




