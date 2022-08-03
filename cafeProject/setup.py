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
#menu_items.insert_one({'id':'','size':'','cal':'','price':'','type':''})
menu_items.insert_one({'id':'coffee(black)','size':'8 oz','cal':'100','price':'2.00','type':'drink'})
menu_items.insert_one({'id':'latte','size':'8 oz','cal':'150','price':'2.50','type':'drink'})
menu_items.insert_one({'id':'iced macha latte','size':'8 oz','cal':'150','price':'3.50','type':'drink'})
menu_items.insert_one({'id':'water','size':'8 oz','cal':'0','price':'1.00','type':'drink'})
menu_items.insert_one({'id':'hot chocolate','size':'8 oz','cal':'300','price':'2.50','type':'drink'})
menu_items.insert_one({'id':'chocolate chip waffle','size':'3 pieces','cal':'1000','price':'25.00','type':'food'})
menu_items.insert_one({'id':'dark chocolate croissant','size':'1','cal':'200','price':'4.76','type':'food'})
menu_items.insert_one({'id':'blueberry muffin','size':'1','cal':'170','price':'2.00','type':'food'})
menu_items.insert_one({'id':'jelly tart','size':'1','cal':'230','price':'3.00','type':'food'})
menu_items.insert_one({'id':'vodka','size':'16 oz','cal':'1050','price':'1.00','type':'drink'})