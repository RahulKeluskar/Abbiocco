from app import app
from flask import request
from flask import render_template, flash, redirect, url_for, request, g, session



@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')