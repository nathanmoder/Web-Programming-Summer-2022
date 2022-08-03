from mongita import MongitaClientDisk
client = MongitaClientDisk(host="./.mongita")

#setting up the database for users
user_db=client.user_db
user_list=user_db.user_list
order_list=user_db.order_list
saved_items=user_db.saved_items

user_list.delete_many({})
order_list.delete_many({})
saved_items.delete_many({})

#user_list data: username, hashedword
#order_list data: username, drink, food, price, pickup time
#save_items data: username item _id pairs

#setting up static menu
menu_db=client.menu_db
menu_items=menu_db.menu_items
menu_items.delete_many({})

#menu_items: id,size,cal,price, type
menu_items.insert_one({'id':'coffee','size':'8 oz','cal':'100','price':'2.00','type':'drink'})
#menu_items.insert_one({'id':'','size':'','cal':'','price':'','type':''})