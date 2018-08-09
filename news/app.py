#! /usr/bin/env python3
# -*- coding:utf-8 -*-

from flask import Flask,render_template,redirect,url_for, abort
import os
import json

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

path = '/home/shiyanlou/files'
title = os.listdir(path)


@app.route('/')
def index():
        return render_template('index.html',title=title)

@app.route('/files/<filename>')
def file(filename):
    f = filename + '.json'
    if f in title:
        with open(path+'/'+f) as d:
            data = d.read()
            data = json.loads(data)
        return render_template('file.html',filename=data)
    else  :
        abort(404)
        #return redirect(url_for('not_found'))

@app.errorhandler(404)
def not_found():
    return render_template('404.html')
