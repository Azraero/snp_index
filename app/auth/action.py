from app.db import DB
from datetime import datetime
get_user_cmd = "select username from users where username='{0}'"
get_passwd_cmd = "select password from users where username='{0}' or email='{0}'"


def check_login(form_data):
    db = DB()
    user = form_data['user']
    result = db.execute(get_user_cmd.format(user), get_all=False)
    if result:
        passwd = form_data['password']
        result = db.execute(get_passwd_cmd.format(user), get_all=False)
        if result[0] == passwd:
            return True, 'ok'
        else:
            return False, 'password error'
    return False, 'user not found!'

def save_register(form_data):
    db = DB()
    user = form_data['user']
    passwd = form_data['password']
    email = form_data['email']
    db.insert('users',{'username':user,
                       'password':passwd,
                       'email':email,
                       'create_at':datetime.now().strftime("%y-%m-%d %H:%M")})
    return True, 'ok'