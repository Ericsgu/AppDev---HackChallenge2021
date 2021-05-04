import json
import os
import string, random
import bcrypt
from db import db
from db import User, PublicList, PrivateList, Event, Image
from flask import Flask
from flask import request

app = Flask(__name__)
db_filename = "cms.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False

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
    if not bcrypt.checkpw(password.encode('utf-8'), user.password):
    # if user.password != password:
        return failure_response("password incorrect!")


# 查看好友的lists
@app.route("/api/<string:uid>/friends_lists/")
def get_friends_lists(uid):
    user = User.query.filter_by(id=uid).first()
    if user is None:
        return failure_response("user not found!")
    return success_response([c.serialize() for c in User.sharing_lists.query.all()])


# 查看自己的lists
@app.route("/api/<string:uid>/lists/")
def get_lists(uid):
    user = User.query.filter_by(id=uid).first()
    if user is None:
        return failure_response("user not found!")
    return success_response([c.serialize() for c in User.public_lists.query.all()])


@app.route("/api/<string:uid>/lists/<int:list_id>")
def get_list_by_id(uid, list_id):
    user = User.query.filter_by(id=uid).first()
    if user is None:
        return failure_response("user not found!")
    public_list = user.public_lists.query.filter_by(id=list_id).first()
    return success_response(public_list.serialize())

@app.route("/api/<string:uid/lists/<int:list_id>/events/", methods=["POST"])
def create_event(uid, list_id):
    user = User.query(filter_by(id=uid).first()
    if user is None:
        return failure_response("user not found!")
    public_list = user.public_lists.query.filter_by(id=list_id).first()
    if public_list is None:
        return failure_response("list not found!")
    body = json.loads(request.data.decode())
    company = body.get('company')
    position = body.get('position')
    reminder = body.get('reminder')
    if not company or not position or not reminder:
        return failure_response("missing field(s)!")
    event = Event(company=company, position=position, reminder=reminder)
    public_list.append(event)
    return success_response(event.serialize())

@app.route("/api/<string:uid>/lists/<int:list_id>/<int:event_id>")
def get_event_by_id(uid, list_id, event_id):
    user = User.query.filter_by(id=uid).first()
    if user is None: 
        return failure_response("user not found!")
    event_list = user.public_lists.query.filter_by(id = list_id).first()
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
    event_list = user.public_lists.query.filter_by(id = list_id).first()
    if event_list is None:
        return failure_response("list not found!")
    event = event_list.events.filter_by(id = event_id).first()
    if event is None:
            return failure_response("list not found!")
    body = json.loads(request.data.decode())
    event.company = body.get('company', event.company)
    event.position = body.get('position', event.position)
    event.reminder = body.get('reminder', event.reminder)
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