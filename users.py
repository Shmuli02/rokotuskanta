from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def login(username,password):
    sql = "SELECT password, id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
        return False
    else:
        if check_password_hash(user[0],password):
            session["user_id"] = user[1]
            return True
        else:
            return False

def logout():
    del session["user_id"]

def register(username,password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username,password, rights) VALUES (:username,:password,1)"
        db.session.execute(sql, {"username":username,"password":hash_value})
        db.session.commit()
        sql2 = "INSERT INTO vaccination (user_id) VALUES ((SELECT id FROM users WHERE username=:username))"
        db.session.execute(sql2, {"username":username})
        db.session.commit()
    except:
        return False
    return login(username,password)

def user_id():
    return session.get("user_id",0)
