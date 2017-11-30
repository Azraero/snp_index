# coding:utf-8
import json
from . import auth
from .actions import check_login, save_register
from flask import session, render_template, \
    request, redirect, url_for, jsonify


@auth.route('/auth/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form_data = json.loads(request.form['data'])
        code, msg = check_login(form_data)
        if code:
            session['login_id'] = form_data['user']
        return jsonify({'msg': msg})
    return render_template('auth/login.html')


@auth.route('/auth/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        form_data = json.loads(request.form['data'])
        code, msg = save_register(form_data)
        return jsonify({'msg': msg})
    return render_template('auth/register.html')


@auth.route('/auth/logout', methods=['GET'])
def logout():
    session['login_id'] = None
    return redirect(url_for('auth.login'))

