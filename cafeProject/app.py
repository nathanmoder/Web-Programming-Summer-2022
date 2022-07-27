from flask import Flask
from flask import render_template
from flask import request, redirect, url_for, make_response
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
import json

from mongita import MongitaClientDisk
db_server = MongitaClientDisk(host="./.mongita")

app = Flask(__name__)

#routes to be handled:
#/
#/login
#/register
#/menu
#/about
#/receipt