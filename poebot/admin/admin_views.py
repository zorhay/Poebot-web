from flask import request, redirect, url_for
from flask_admin import AdminIndexView, expose
from flask_login import current_user, login_user, logout_user
from .forms import LoginForm


class PoebotAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        return super(PoebotAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        params = {}
        form = LoginForm(request.form)
        if form.validate_on_submit():
            user = form.get_user()
            login_user(user)

        if current_user.is_authenticated:
            return redirect(url_for('.index'))

        self._template_args['form'] = form
        return self.render('admin/login.html', **params)

    @expose('/logout/')
    def logout_view(self):
        logout_user()
        return redirect(url_for('.index'))
