from mongita import MongitaClientDisk
client = MongitaClientDisk(host="./.mongita")

menu_db=client.menu_db
menu_items=menu_db.menu_items

menu_items.insert_one({'id':'coffee','size':'8 oz','cal':'100','price':'2.00','type':'drink'})
#menu_items.insert_one({'id':'','size':'','cal':'','price':'','type':''})