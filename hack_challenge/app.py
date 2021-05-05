import json
import os
import string, random
import bcrypt
from db import db, User, PublicList, Event, Image, User_PublicList_Association
from flask import Flask
from flask import request

app = Flask(__name__)
db_filename = "cms.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()


def success_response(data, code=200):
    return json.dumps({"success": True, "data": data}), code


def failure_response(message, code=404):
    return json.dumps({"success": False, "error": message}), code


@app.route("/api/courses/")
def get_lists():
    return success_response([c.serialize() for c in PublicList.query.all()])


# 注册 需要跳转到登录界面
@app.route("/api/register/")
def register():
    body = json.loads(request.data.decode())
    name = body.get('name')
    if name is None:
        return failure_response("no name entered")
    password = body.get('password')
    if password is None:
        return failure_response("no password entered")
    salt = bcrypt.gensalt()
    password = bcrypt.hashpw(password.encode('utf-8'), salt)
    uid = ''.join(random.sample(string.digits, 8))
    possible_user = User.query.filter_by(uid=uid).first()
    while possible_user is not None:
        uid = ''.join(random.sample(string.digits, 8))
        possible_user = User.query.filter_by(uid=uid).first()
    new_user = User(name=name, password=password, uid=uid, public_lists=[], private_lists=[], sharing_lists=[],
                    friends=[])
    db.session.add(new_user)
    db.session.commit()
    return success_response("successfully registered!")



# 登录
@app.route("/api/login/", methods=['POST'])
def login():
    body = json.loads(request.data.decode())
    uid = body.get('uid')
    if uid is None:
        return failure_response("no uid entered")
    password = body.get('password')
    if password is None:
        return failure_response("no password entered")
    user = User.query.filter_by(uid=uid).first()
    if user is None:
        return failure_response("user not found!")
    if user.password != password:
        return failure_response("password incorrect!")


# 查看好友的lists
@app.route("/api/<string:uid>/friends_lists/")
def get_friends_lists(uid):
    user = User.query.filter_by(id=uid).first()
    
    if user is None:
        return failure_response("user not found!")
    friends = user.friends
    return success_response([lst.serialize() for f in friends for lst in f.public_lists if lst.is_public])


# 查看自己的lists
@app.route("/api/<int:id>/lists/")
def get_lists(id):
    user = User.query.filter_by(id=id).first()
    if user is None:
        return failure_response("user not found!")
    return success_response([c.serialize() for c in User.public_lists.query.all()])


@app.route("/api/<string:uid>/lists/<int:list_id>")
def get_list_by_id(uid, list_id):
    user = User.query.filter_by(id=uid).first()
    if user is None:
        return failure_response("user not found!")
    public_list = User.public_lists.query.filter_by(public_list_id=list_id).first()
    return success_response(public_list.serialize())

@app.route("/api/<int:userid>/lists/", methods=['POST'])
def create_list(userid):
    body = json.loads(request.data.decode())
    list_name = body.get('listname')
    is_public = body.get('is_public')
    if is_public is None or list_name is None:
        return failure_response("Please provide access information/name of list")
    user = User.query.filter_by(id=userid).first()
    if user is None:
        return failure_response("user not found!")
    new_list = PublicList(listname=list_name, publisher_id=userid)
    db.session.add(new_list)
    db.session.commit()
    association = User_PublicList_Association(is_public=is_public)
    association.public_list = new_list
    user.public_lists.append(association)
    db.session.add(association)
    db.session.commit()


@app.route("/api/<string:uid/lists/<int:list_id>/events/", methods=['POST'])
def create_event(list_id):
    public_list = PublicList.query.filter_by(id=list_id).first()
    if public_list is None:
        return failure_response('list not found!')
    
    body = json.loads(request.data)
    title = body.get('title')
    description = body.get('description')
    event_time = body.get('event_time')
    
    if title is None or description is None or event_time is None:
        return failure_response('Please provide titile, description, and time')
    
    new_event = Event(
        title = title,
        description = description,
        public_list_id = list_id,
        event_time = event_time
    )
    #new_assignment.course = course
    public_list.events.append(new_event)
    db.session.add(new_event)
    db.session.commit()
    return success_response(new_event.serialize(), 201)



@app.route("/api/<string:uid>/lists/<int:list_id>/<int:event_id>")
def get_event_by_id(uid, list_id, event_id):
    user = User.query.filter_by(id=uid).first()
    if user is None: 
        return failure_response("user not found!")
    event_list = user.public_lists.query.filter_by(public_list_id = list_id).first()
    if event_list is None:
        return failure_response("list not found!")
    event = event_list.events.filter_by(id = event_id).first()
    if event is None:
            return failure_response("list not found!")
    return success_response(event.serialize())

@app.route("/api/<string:uid>/lists/<int:list_id>/<int:event_id>", methods=["POST"])
def edit_event_by_id(uid, list_id, event_id):
    user = User.query.filter_by(id=uid).first()
    if user is None: 
        return failure_response("user not found!")
    event_list = user.public_lists.query.filter_by(public_list_id = list_id).first()
    if event_list is None:
        return failure_response("list not found!")
    event = event_list.events.filter_by(id = event_id).first()
    if event is None:
            return failure_response("list not found!")
    body = json.loads(request.data.decode())
    event.title = body.get('title', event.title)
    event.description = body.get('description', event.description)
    event.event_time = body.get('event_time', event.event_time)
    db.sesssion.commit()


# 添加好友
@app.route("/api/<string:uid>/friends/add/", methods=['POST'])
def add_friends(uid):
    body = json.loads(request.data.decode())
    user = User.query.filter_by(uid=uid).first()
    if user is None:
        return failure_response("user not found!")
    search_uid = body.get('uid')
    if search_uid is None:
        return failure_response("no uid entered")
    search_user = User.query.filter_by(uid=search_uid).first()
    if search_user is None:
        return failure_response("user not found!")
    search_user.applying_friends.append(user)
    db.session.add(user)
    db.session.commit()
    return success_response("successfully applied!")


# 同意好友申请
@app.route("/api/<string:uid>/friends/new_friends/<int:friend_uid>/consent/")
def agree_friend_request(uid, friend_uid):
    user = User.query.filter_by(uid=uid).first()
    if user is None:
        return failure_response("user not found!")
    friend = User.query.filter_by(uid=friend_uid).first()
    user.friends.append(friend)
    user.applying_friends.remove(friend)
    db.session.add(friend)
    db.session.commit()
    return success_response("successfully applied!")


# 拒绝好友申请
@app.route("/api/<string:uid>/friends/new_friends/<int:friend_uid>/decline/")
def decline_friend_request(uid, friend_uid):
    user = User.query.filter_by(uid=uid).first()
    if user is None:
        return failure_response("user not found!")
    friend = User.query.filter_by(uid=friend_uid).first()
    user.applying_friends.remove(friend)
    db.session.add(friend)
    db.session.commit()
    return success_response("successfully declined!")


if __name__ == "__main__":
    port = os.environ.get('PORT', 5000)
    app.run(host="0.0.0.0", port=port)