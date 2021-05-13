import json
import os
from db import db, User, PublicList, Event, Image, User_PublicList_Association, Item
from flask import Flask
from flask import request

app = Flask(__name__)
db_filename = "letsdoit.db"

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

def get_user_by_name(name):
    return User.query.filter_by(name=name).first()

def get_user_by_session_token(session_token):
    return User.query.filter_by(session_token=session_token).first()

def get_user_by_update_token(update_token):
    return User.query.filter_by(update_token=update_token).first()

def extract_token(request):
    auth_header = request.headers.get("Authorization")
    if auth_header is None:
        return False, failure_response("missing auth header")
    bearer_token = auth_header.replace("Bearer ", "").strip()
    if bearer_token is None or not bearer_token:
        return False, failure_response("invalid auth header")
    return True, bearer_token

def check_session():
    success, session_token = extract_token(request)
    if not success: 
        return False, session_token
    user = get_user_by_session_token(session_token)
    if user is None:
        return False, failure_response("user not found!")
    if not user.verify_session(session_token):
        return False, failure_response("invalid session token!")
    return True, user

@app.route("/api/session/", methods=["POST"])
def update_token():
    success, update_token = extract_token(request)
    if not success:
        return update_token
    user = get_user_by_update_token(update_token)
    if user is None:
        return failure_response("invalid update token: " + update_token)
    user.renew_session()
    db.session.commit()
    return success_response({ 
        "session_token": user.session_token,
        "session_expiration": str(user.session_expiration),
        "update_token": user.update_token
    })

@app.route("/api/register/", methods=["POST"])
def register():
    body = json.loads(request.data.decode())
    name = body.get('name')
    if name is None:
        return failure_response("no name entered")
    password = body.get('password')
    if password is None:
        return failure_response("no password entered")
    if get_user_by_name(name) is not None:
        return failure_response("user already exists!")
    new_user = User(name=name, password=password)
    db.session.add(new_user)
    db.session.commit()
    return success_response({ 
        "session_token": new_user.session_token,
        "session_expiration": str(new_user.session_expiration),
        "update_token": new_user.update_token
    })

@app.route("/api/login/", methods=["POST"])
def login():
    body = json.loads(request.data.decode())
    name = body.get('name')
    if name is None:
        return failure_response("no name entered")
    password = body.get('password')
    if password is None:
        return failure_response("no password entered")
    user = get_user_by_name(name)
    if user is None:
        return failure_response("user not found!")
    if not user.verify_password(password):
        return failure_response("password incorrect!")
    return success_response({ 
        "session_token": user.session_token,
        "session_expiration": str(user.session_expiration),
        "update_token": user.update_token
    })

# List routes 
@app.route("/api/lists/")
def get_all_lists():
    success, user = check_session()
    if not success:
        return user
    return success_response({"lists": [c.public_list.serialize() for c in user.public_lists if c.is_public]})

@app.route("/api/lists/<int:list_id>/")
def get_list_by_id(list_id):
    success, user = check_session()
    if not success:
        return user
    public_list = user.public_lists.filter_by(public_list_id=list_id).first()
    if public_list is None:
        return failure_response("list not found!")
    return success_response(public_list.public_list.serialize())

@app.route("/api/lists/", methods=['POST'])
def create_list():
    body = json.loads(request.data.decode())
    list_name = body.get('list_name')
    is_public = body.get('is_public')
    if is_public is None or list_name is None:
        return failure_response("Please provide access information/name of list")
    success, user = check_session()
    if not success:
        return user
    new_list = PublicList(list_name=list_name, publisher_id=user.id)
    db.session.add(new_list)
    association = User_PublicList_Association(user_id=user.id, is_public=is_public)
    association.public_list = new_list
    user.public_lists.append(association)
    db.session.add(association)
    db.session.commit()
    return success_response(new_list.serialize())

@app.route("/api/lists/<int:list_id>/", methods=["POST"])
def edit_list_by_id(list_id):
    success, user = check_session()
    if not success:
        return user
    public_list = user.public_lists.filter_by(public_list_id=list_id).first()
    if public_list is None:
        return failure_response("list not found!")
    body = json.loads(request.data.decode())
    public_list.is_public = body.get('is_public', public_list.is_public)
    public_list = public_list.public_list
    public_list.list_name = body.get('list_name', public_list.list_name)
    db.session.commit()
    return success_response(public_list.serialize())

@app.route("/api/lists/<int:list_id>/delete/", methods=['DELETE'])
def delete_list_by_id(list_id):
    success, user = check_session()
    if not success:
        return user
    delete_list = User_PublicList_Association.query.filter_by(user_id=user.id, public_list_id = list_id).first()
    if delete_list is None:
        return failure_response("list not found!")
    public_list = delete_list.public_list
    db.session.delete(public_list)
    user.public_lists.remove(delete_list)
    db.session.delete(delete_list)
    db.session.commit()
    return success_response(public_list.serialize())

# Event routes
@app.route("/api/lists/<int:list_id>/events/")
def get_all_events(list_id):
    success, user = check_session()
    if not success:
        return user
    public_list = PublicList.query.filter_by(id=list_id).first()
    if public_list is None:
        return failure_response('list not found!')
    return success_response({"events": [c.serialize() for c in public_list.events]})

@app.route("/api/lists/<int:list_id>/events/<int:event_id>/")
def get_event_by_id(list_id, event_id):
    success, user = check_session()
    if not success:
        return user
    event_list = user.public_lists.filter_by(public_list_id = list_id).first()
    if event_list is None:
        return failure_response("list not found!")
    event_list = event_list.public_list
    event = event_list.events.filter_by(id = event_id).first()
    if event is None:
            return failure_response("event not found!")
    return success_response(event.serialize())

@app.route("/api/lists/<int:list_id>/events/", methods=["POST"])
def create_event(list_id):
    success, user = check_session()
    if not success:
        return user
    public_list = PublicList.query.filter_by(id=list_id).first()
    if public_list is None:
        return failure_response('list not found!')
    body = json.loads(request.data.decode())
    main_title = body.get('main_title')
    sub_title = body.get('sub_title')
    in_progress = body.get('in_progress')
    if main_title is None or sub_title is None or in_progress is None:
        return failure_response("missing field(s)!")
    new_event = Event(main_title=main_title, sub_title=sub_title, in_progress=in_progress, public_list_id = list_id)
    public_list.events.append(new_event)
    db.session.add(new_event)
    db.session.commit()
    return success_response(new_event.serialize(), 201)

@app.route("/api/lists/<int:list_id>/events/<int:event_id>/", methods=["POST"])
def edit_event_by_id(list_id, event_id):
    success, user = check_session()
    if not success:
        return user
    event_list = user.public_lists.filter_by(public_list_id = list_id).first()
    if event_list is None:
        return failure_response("list not found!")
    event_list = event_list.public_list
    event = event_list.events.filter_by(id = event_id).first()
    if event is None:
            return failure_response("event not found!")
    body = json.loads(request.data.decode())
    event.main_title = body.get('main_title', event.main_title)
    event.sub_title = body.get('sub_title', event.sub_title)
    event.in_progress = body.get('in_progress', event.in_progress)
    db.session.commit()
    return success_response(event.serialize())

@app.route("/api/lists/<int:list_id>/events/<int:event_id>/delete/", methods=['DELETE'])
def delete_event_by_id(list_id, event_id):
    success, user = check_session()
    if not success:
        return user
    event_list = user.public_lists.filter_by(public_list_id = list_id).first()
    if event_list is None:
        return failure_response("list not found!")
    event_list = event_list.public_list
    delete_event = event_list.events.filter_by(id = event_id).first()
    if delete_event is None:
            return failure_response("event not found!")
    event_list.events.remove(delete_event)
    db.session.delete(delete_event)
    db.session.commit()
    return success_response(delete_event.serialize())

# Friend routes
@app.route("/api/friends/add/", methods=['POST'])
def add_friend():
    success, user = check_session()
    if not success:
        return user
    body = json.loads(request.data.decode())
    search_id = body.get('id')
    if search_id is None:
        return failure_response("no id entered")
    if id == search_id:
        return failure_response("cannot send a request to yourself!")
    search_user = User.query.filter_by(id=search_id).first()
    if search_user is None:
        return failure_response("user not found!")
    already_friend = user.friends.filter_by(id=search_id).first()
    if already_friend is not None:
        return failure_response("you already added this user!")
    already_request = user.applying_friends.filter_by(id=search_id).first()
    if already_request is not None:
        return failure_response("you already have a pending response!")
    search_user.applying_friends.append(user)
    db.session.commit()
    return success_response(search_user.serialize())

@app.route("/api/friends/accept/<int:friend_id>/", methods=["POST"])
def accept_friend_request(friend_id):
    success, user = check_session()
    if not success:
        return user
    friend = User.query.filter_by(id=friend_id).first()
    if friend is None:
        return failure_response("friend user not found!")
    friend = user.applying_friends.filter_by(id=friend_id).first()
    if friend is None:
        return failure_response("this user does not have a pending request!")
    user.friends.append(friend)
    user.applying_friends.remove(friend)
    db.session.commit()
    return success_response(friend.serialize())

@app.route("/api/friends/reject/<int:friend_id>/", methods=["POST"])
def reject_friend_request(friend_id):
    success, user = check_session()
    if not success:
        return user
    friend = User.query.filter_by(id=friend_id).first()
    if friend is None:
        return failure_response("friend user not found!")
    friend = user.applying_friends.filter_by(id=friend_id).first()
    if friend is None:
        return failure_response("this user does not have a pending request!")
    user.applying_friends.remove(friend)
    db.session.commit()
    return success_response(friend.serialize())

@app.route("/api/friends/requests/")
def get_friend_requests():
    success, user = check_session()
    if not success:
        return user
    return success_response({"requests": [f.serialize() for f in user.applying_friends]})

@app.route("/api/friends_lists/")
def get_friends_lists():
    success, user = check_session()
    if not success:
        return user
    return success_response({"friends": [f.serialize() for f in user.friends]})

# Item routes
@app.route("/api/lists/<int:list_id>/events/<int:event_id>/items/")
def get_all_items(list_id, event_id):
    success, user = check_session()
    if not success:
        return user
    event_list = user.public_lists.filter_by(public_list_id = list_id).first()
    if event_list is None:
        return failure_response("list not found!")
    event_list = event_list.public_list
    event = event_list.events.filter_by(id = event_id).first()
    if event is None:
        return failure_response("event not found!")
    return success_response({"items": [i.serialize() for i in event.items]})

@app.route("/api/lists/<int:list_id>/events/<int:event_id>/items/<int:item_id>/")
def get_item_by_id(list_id, event_id, item_id):
    success, user = check_session()
    if not success:
        return user
    event_list = user.public_lists.filter_by(public_list_id = list_id).first()
    if event_list is None:
        return failure_response("list not found!")
    event_list = event_list.public_list
    event = event_list.events.filter_by(id = event_id).first()
    if event is None:
        return failure_response("event not found!")
    item = event.items.filter_by(id = item_id).first()
    if item is None:
        return failure_response("item not found!")
    return success_response(item.serialize())

@app.route("/api/lists/<int:list_id>/events/<int:event_id>/items/", methods=["POST"])
def create_item(list_id, event_id):
    success, user = check_session()
    if not success:
        return user
    event_list = user.public_lists.filter_by(public_list_id = list_id).first()
    if event_list is None:
        return failure_response("list not found!")
    event_list = event_list.public_list
    event = event_list.events.filter_by(id = event_id).first()
    if event is None:
        return failure_response("event not found!")
    body = json.loads(request.data.decode())
    completed = body.get('completed')
    date = body.get('date')
    title = body.get('title')
    if completed is None or date is None or title is None:
        return failure_response("missing field(s)!")
    new_item = Item(completed=completed, date=date, title=title, event_id = event_id)
    event.items.append(new_item)
    db.session.add(new_item)
    db.session.commit()
    return success_response(new_item.serialize(), 201)

@app.route("/api/lists/<int:list_id>/events/<int:event_id>/items/<int:item_id>/", methods=["POST"])
def edit_item_by_id(list_id, event_id, item_id):
    success, user = check_session()
    if not success:
        return user
    event_list = user.public_lists.filter_by(public_list_id = list_id).first()
    if event_list is None:
        return failure_response("list not found!")
    event_list = event_list.public_list
    event = event_list.events.filter_by(id = event_id).first()
    if event is None:
            return failure_response("event not found!")
    item = event.items.filter_by(id = item_id).first()
    if item is None:
        return failure_response("item not found!")
    body = json.loads(request.data.decode())
    item.completed = body.get('completed', item.completed)
    item.date = body.get('date', item.date)
    item.title = body.get('title', item.title)
    db.session.commit()
    return success_response(item.serialize())

@app.route("/api/lists/<int:list_id>/events/<int:event_id>/items/<int:item_id>/delete/", methods=['DELETE'])
def delete_item_by_id(list_id, event_id, item_id):
    success, user = check_session()
    if not success:
        return user
    event_list = user.public_lists.filter_by(public_list_id = list_id).first()
    if event_list is None:
        return failure_response("list not found!")
    event_list = event_list.public_list
    event = event_list.events.filter_by(id = event_id).first()
    if event is None:
            return failure_response("event not found!")
    delete_item = event.items.filter_by(id = item_id).first()
    if delete_item is None:
        return failure_response("item not found!")
    event.items.remove(delete_item)
    db.session.delete(delete_item)
    db.session.commit()
    return success_response(delete_item.serialize())

if __name__ == "__main__":
    port = os.environ.get('PORT', 5000)
    app.run(host="0.0.0.0", port=port)
