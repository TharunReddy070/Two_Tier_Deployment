'''
Created on Jan 10, 2017
Author: hanif (updated for modern DevOps deployment)
'''

import os
from flask import Flask, flash, render_template, redirect, url_for, request, session
from module.database import Database

app = Flask(__name__)

# Secure Secret Key for session handling
app.secret_key = os.environ.get("SECRET_KEY", "mys3cr3tk3y")

db = Database()

@app.route('/')
def index():
    data = db.read(None)
    return render_template('index.html', data=data)

@app.route('/add/')
def add():
    return render_template('add.html')

@app.route('/addphone', methods=['POST', 'GET'])
def addphone():
    if request.method == 'POST' and request.form.get('save'):
        if db.insert(request.form):
            flash("A new phone number has been added")
        else:
            flash("A new phone number cannot be added")
        return redirect(url_for('index'))
    return redirect(url_for('index'))

@app.route('/update/<int:id>/')
def update(id):
    data = db.read(id)
    if len(data) == 0:
        return redirect(url_for('index'))
    session['update'] = id
    return render_template('update.html', data=data)

@app.route('/updatephone', methods=['POST'])
def updatephone():
    if request.method == 'POST' and request.form.get('update'):
        if db.update(session['update'], request.form):
            flash('A phone number has been updated')
        else:
            flash('A phone number cannot be updated')
        session.pop('update', None)
        return redirect(url_for('index'))
    return redirect(url_for('index'))

@app.route('/delete/<int:id>/')
def delete(id):
    data = db.read(id)
    if len(data) == 0:
        return redirect(url_for('index'))
    session['delete'] = id
    return render_template('delete.html', data=data)

@app.route('/deletephone', methods=['POST'])
def deletephone():
    if request.method == 'POST' and request.form.get('delete'):
        if db.delete(session['delete']):
            flash('A phone number has been deleted')
        else:
            flash('A phone number cannot be deleted')
        session.pop('delete', None)
        return redirect(url_for('index'))
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html')

# Only used in LOCAL development, not in Docker
if __name__ == '__main__':
    app.run(debug=True)
