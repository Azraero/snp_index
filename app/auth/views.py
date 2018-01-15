# coding:utf-8
from . import auth
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from app.exetensions import login_manager
from .forms import RegisterForm, LoginForm
from flask import render_template, \
    request, redirect, url_for, flash
from settings import Config
from app.mail import send_mail


@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id=int(id)).first()


@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.active \
            and request.endpoint \
            and request.endpoint[:5] != 'auth.' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.active:
        return redirect(url_for('main.index'))
    mail_addr = Config.MAIL_MAP.get(current_user.email.split('@')[1], '')
    return render_template('auth/unconfirmed.html', mail=mail_addr)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You are logged out.', 'info')
    return redirect(url_for('main.index'))


@auth.route('/confirm/<token>')
def confirm(token):
    user = User.confirm(token)
    if user:
        if user.is_active:
            flash('you have update your email infomation.', 'success')
            login_user(user)
            return redirect(url_for('main.index'))
        if not user.is_active:
            flash('you have confirm your account. Thanks!', 'success')
            return redirect(url_for('main.index'))
    else:
        flash('the confirmation link is invalid.', 'danger')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=form.password.data)
        user.save()
        token = user.generate_confirmation_token()
        send_mail(user.email, 'Confirm Your Account',
                  'mail/confirm', user=user, token=token)
        flash('Thanks your register. A confirm email has been sent to your email', 'success')
        login_user(user)
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(form.user)
            flash('You are loggin in.', 'success')
            redicret_url = request.args.get('next') or url_for('users.members')
            return redirect(redicret_url)
    return render_template('auth/login.html', form=form)


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_mail(current_user.email, 'Confirm Your Account',
              'mail/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.', 'success')
    return redirect(url_for('main.index'))

