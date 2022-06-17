from re import U
from tkinter import YView
from flask import Flask, render_template

app=Flask(__name__)

@app.route("/")
def get_index():
    return "<p>This is the Nathan's website on PA.</p>"

@app.route("/hello")
def get_hello():
    return render_template('hello.html',name="Nathan")