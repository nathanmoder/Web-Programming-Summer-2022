from re import U
from tkinter import YView
from flask import Flask
from flask import render_template
from flask import request, redirect, url_for, make_response

app = Flask(__name__)

username = None

@app.route("/")
@app.route("/home")
def get_index():
    username = request.cookies.get("username", None)
    if username == None:
        return redirect(url_for('get_login'))
    return render_template('home.html', name=username)

@app.route("/login", methods=['GET'])
def get_login():
    username = request.cookies.get("username", None)
    if username != None:
        return redirect(url_for('get_index'))
    return render_template('login.html')

@app.route("/login", methods=['POST'])
def post_login():
    username = request.form.get("username", None)
    response = make_response(redirect(url_for('get_index')))
    response.set_cookie("username", username)
    return response

@app.route("/register", methods=['GET'])
def get_register():
    username = request.cookies.get("username", None)
    if username != None:
        return redirect(url_for('get_index'))
    return render_template('register.html')

@app.route("/register", methods=['POST'])
def post_register():
    username = request.form.get("username", None)
    response = make_response(redirect(url_for('get_index')))
    response.set_cookie("username", username)
    return response

@app.route("/logout", methods=['GET'])
def get_logout():
    response = make_response(redirect(url_for('get_login')))
    response.delete_cookie('username')
    return response