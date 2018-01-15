from flask import redirect, url_for
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose
import flask_login as login


class myAdminIndex(AdminIndexView):
    @login.login_required
    @expose('/')
    def index(self):
        return super(myAdminIndex, self).index()

    @login.login_required
    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('main.index'))


class authModelView(ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated and login.current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.index'))

