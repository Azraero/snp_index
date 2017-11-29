from app.db import DB
from datetime import datetime
get_user_cmd = "select username from users where username='{0}' or email='{0}'"
get_passwd_cmd = "select password,is_active from users where username='{0}' or email='{0}'"


def check_login(form_data):
    db = DB()
    user = form_data['user']
    result = db.execute(get_user_cmd.format(user), get_all=False)
    if result:
        passwd = form_data['password']
        password, is_active = db.execute(get_passwd_cmd.format(user), get_all=False)
        if password == passwd and is_active == 'Y':
            return True, 'ok'
        elif password != passwd:
            return False, 'password error'
        return False, 'user not active'
    return False, 'user not found'

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