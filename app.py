from re import U
from tkinter import YView
from flask import Flask

app=Flask(__name__)

@app.route("/")
def get_index():
    return "<p>This is the Nathan's website on PA.</p>"
