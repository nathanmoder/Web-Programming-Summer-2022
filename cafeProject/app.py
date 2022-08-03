from urllib import response
from flask import Flask
from flask import render_template
from flask import request, redirect, url_for, make_response
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
import json

from mongita import MongitaClientDisk
db_server = MongitaClientDisk(host="./.mongita")

app = Flask(__name__)
app.secret_key="melon"

#routes to be handled:

##########################################################
#/
@app.route("/")
def get_index():
    if 'username' in session and session['username']!=None:
        return redirect(url_for('get_order'))
    else:
        username = request.cookies.get('username', None)
        if username == None:
            return redirect(url_for('get_menu'))
        else:
            session['username']=username
            return redirect(url_for('get_order'))
        
    

##########################################################
#/login and logout
@app.route("/login", methods=['GET'])
def get_login():
    username = request.cookies.get("username", None)
    if username != None or session['username'] != None:
        return redirect(url_for('get_index'))
    else:
        return render_template('login.html', name='no user')

@app.route("/login", methods=['POST'])
def post_login():
    username = request.form.get("username", None)
    if username == None:
        return redirect(url_for('get_login'))
    try:
        saved_user=db_server.user_db.user_list.find_one({"username":username})
    #except:
    #    print("No such user found")
    #    return redirect(url_for('get_login'))
    except Exception as e:
        print(f"Error in reading credentials. {e}")
        return redirect(url_for('get_login'))
    if saved_user != None:
        password = request.form.get("password", None)
        if password == None:
            return redirect(url_for('get_login'))
        if not check_password_hash(saved_user['password'], password):
            print("Password is incorrect")
            return redirect(url_for('get_login'))
        response = make_response(redirect(url_for('get_index')))
        response.set_cookie("username", username)
        return response
    return redirect(url_for('get_login'))



@app.route("/logout", methods=['GET'])
def get_logout():
    #shouldn't break, but may want to redirect
    response = make_response(redirect(url_for('get_index')))
    response.delete_cookie('username')
    session['username']=None
    return response

##########################################################
#/register

@app.route('/register', methods=['GET'])
def get_register():
    return render_template('register.html',name='no user')

@app.route('/register', methods=['POST'])
def post_register():
    username = request.form.get("username", None)
    if username == None:
        return redirect(url_for('get_register'))
    for c in username.lower():
        if not(c.isalpha() or c.isdigit() or (c in '.-_')):
            print("Illegal character in username. Only use abc,123, and .-_")
            return redirect(url_for('get_register'))
    password = request.form.get("password", None)
    if password == None:
        return redirect(url_for('get_register'))
    if len(password) < 8:
        print("Password must be at least 8 characters long.")
        return redirect(url_for('get_register'))
    repeated_password = request.form.get("repeated", None)
    if repeated_password == None:
        return redirect(url_for('get_register'))
    if repeated_password != password:
        print("repeated password does not match password")
        return redirect(url_for('get_register'))

    #TODO: add code to check for repeat users

    credentials={
        'username':username,
        'password':generate_password_hash(password)
    }
    db_server.user_db.user_list.insert_one(credentials)
    response = make_response(redirect(url_for('get_index')))
    response.set_cookie("username", username)
    session['username']=username
    return response



#/menu
@app.route("/menu")
def get_menu():
    if 'username' in session and session['username']!=None:
        username=session['username']
    else:
        username="no user"
    menu_list=list(db_server.menu_db.menu_items.find({}))
    #print(menu_list)
    return render_template('menu.html',name=username,menu_items=menu_list)

@app.route("/add_to_order/<id>")
def get_additem(id):
    #give ze cookie
    menu_items=db_server.menu_db.menu_items
    response=make_response(redirect(url_for('get_order')))
    item_to_add=menu_items.find_one({'_id':id})
    if item_to_add['type']=='drink':
        response.set_cookie('drink',id)
    if item_to_add['type']=='food':
        response.set_cookie('food',id)
    print('nothing exploded')
    return response

@app.route("/remove_food")
def get_remove_food():
    response=make_response(redirect(url_for('get_order')))
    response.delete_cookie('food')
    return response

@app.route("/remove_drink")
def get_remove_drink():
    response=make_response(redirect(url_for('get_order')))
    response.delete_cookie('drink')
    return response

#TODO: individual types of items in the menu, i.e. menu/drinks
#/about
#/receipt

#/order
#TODO: implement
@app.route('/order', methods=['GET'])
def get_order():
    menu_items=db_server.menu_db.menu_items
    previous_items=[]
    if 'username' in session and session['username']!=None:
        username=session['username']
        saved_items=db_server.user_db.saved_items
        previous_orders=list(saved_items.find({'username':username}))
        
        for item in previous_orders:
            print(item)
            the_thing=menu_items.find_one({'_id':item['item']})
            print(the_thing)
            previous_items.append(the_thing)

    else:
        username="no user"
    
    cookie_drink=request.cookies.get('drink',None)
    if cookie_drink != None:
        drink=menu_items.find_one({'_id':cookie_drink})
    else:
        drink="no drink"
    cookie_food=request.cookies.get('food',None)
    if cookie_food != None:
        food=menu_items.find_one({'_id':cookie_food})
    else:
        food="no food"
    
    return render_template('quick_order.html',name=username,drink=drink,food=food,previous_items=previous_items)

@app.route('/order', methods=['POST'])
def post_order():
    saved_items=db_server.user_db.saved_items
    response=make_response(redirect(url_for('get_order')))
    if 'username' in session and session['username']!=None:
        username=session['username']
        cookie_drink=request.cookies.get('drink',None)
        #TODO: search for repeats
        if cookie_drink != None:
            test_drink=saved_items.find_one({'username':username,'item':cookie_drink})
            if test_drink == None: 
                saved_items.insert_one({'username':username,'item':cookie_drink})
        cookie_food=request.cookies.get('food',None)
        if cookie_food != None:
            test_food=saved_items.find_one({'username':username,'item':cookie_food})
            if test_food == None: 
                saved_items.insert_one({'username':username,'item':cookie_food})
    response.delete_cookie('drink')
    response.delete_cookie('food')
    print('code actually ran')
    return response