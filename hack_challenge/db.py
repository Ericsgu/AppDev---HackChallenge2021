from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


user_publicList_association = db.Table(
    'association',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('publicList_id', db.Integer, db.ForeignKey('public_list.id'))
)
user_publicList_association2 = db.Table(
    'association2',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('publicList_id', db.Integer, db.ForeignKey('public_list.id'))
)

user_privateList_association = db.Table(
    'association3',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('privateList_id', db.Integer, db.ForeignKey('private_list.id'))
)

# user 2 user
friends_association = db.Table(
    'friends',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

applying_friends_association = db.Table(
    'friends',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    uid = db.Column(db.String, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    public_lists = db.relationship("PublicList", secondary=user_publicList_association, back_populates='publisher_id')
    private_lists = db.relationship("PrivateList", secondary=user_publicList_association, back_populates='publisher_id')
    sharing_lists = db.relationship('PublicList', secondary=user_publicList_association2, back_populates='sharers')

    # 已有好友
    friends = db.relationship(
        'User',
        secondary=friends_association,
        primaryjoin=(applying_friends_association.friend_id == id),
        secondaryjoin=(applying_friends_association.friend_id == id),
        lazy='dynamic',
        backref=db.backref('applying_friends_association', lazy='dynamic')
    )
    # 好友申请
    applying_friends = db.relationship(
        'User',
        secondary=friends_association,
        primaryjoin=(friends_association.friend_id == id),  # 多对多中）用于从子对象查询其父对象的 condition（child.parents）
        secondaryjoin=(friends_association.friend_id == id),  # 多对多中）用于从父对象查询其所有子对象的 condition（parent.children）
        lazy='dynamic',  # 延迟求值，这样才能用 filter_by 等过滤函数
        backref=db.backref('friends_association', lazy='dynamic')
    )

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.uid = kwargs.get('uid')
        self.public_lists = kwargs.get('public_lists')
        self.private_lists = kwargs.get('private_lists')
        self.friends = kwargs.get('friends')




class PublicList(db.Model):
    __tablename__ = "public_list"
    id = db.Column(db.Integer, primary_key=True)
    publisher_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    sharers = db.relationship('User', secondary=user_publicList_association2, back_populates='sharing_lists')
    listName = db.Column(db.String, nullable=False)
    events = db.relationship("Event", cascade="delete")

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.publisher_id = kwargs.get('publisher_id')
        self.sharers = kwargs.get('sharers')
        self.listName = kwargs.get('listName')
        self.events = kwargs.get('events')

    def serialize(self):
        return {
            "name": self.name,
            "listName": self.listName,
            "events": self.events
        }


class PrivateList(db.Model):
    __tablename__ = "private_list"
    id = db.Column(db.Integer, primary_key=True)
    publisher_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    listName = db.Column(db.String, nullable=False)
    events = db.relationship("Event", cascade="delete")


class Event(db.Model):
    __tablename__ = "event"
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String, nullable=False)
    position = db.Column(db.String, nullable=False)
    reminder = db.Column(db.String, nullable=False)


class Image(db.Model):
    __tablename__ = "images"
    id = db.Column(db.Integer, primary_key=True)




