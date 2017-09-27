# coding=utf-8
import os
from flask import Flask, render_template, session, request, jsonify, redirect, url_for
from flask_script import Manager, Shell
from datetime import datetime
import MySQLdb


app = Flask(__name__)
manager = Manager(app)
files = ['test1', 'test2', 'test3']
file_dict = {'test1': ['a', 'b', 'c'],
             'test2': ['d', 'e', 'f'],
             'test3': ['whd', 'mhd']}
basedir = os.path.abspath(os.path.dirname(__file__))
app.secret_key = 'djaildhjsdfhjsofjilsfjsfjpjfojgogj'


@app.route('/')
def index():
    return render_template('index.html', user='chencheng', files=files)


@app.route('/select_file', methods=['GET'])
def select_file():
    filename = request.args.get('file', '')
    if file_dict.get(filename):
        msg = file_dict[filename]
        return jsonify({'msg': msg})
    else:
        msg = 'error'
        return jsonify({'msg': msg})


@app.route('/search_sampe', methods=['GET'])
def search_sampe():
    sample = request.args.get('sample', '')
    # here check smaple whether in table
    msg = sample
    return jsonify({'msg': msg})


if __name__ == '__main__':
    manager.run()
