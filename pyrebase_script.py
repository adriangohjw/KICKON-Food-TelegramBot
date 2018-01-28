import pyrebase

# set up config
config = {
    "apiKey": "",
    "authDomain": "",
    "databaseURL": "",
    "storageBucket": "",
    # change this path on a separate server
    "serviceAccount": "" 
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()


def get_num_entry():
    orders = db.child("orders").get()
    data = orders.val()
    max = 0
    for i in data:
        try:
            if i['id'] > max:
                max = i['id']
        except:
            pass
    return max


def push_order(order_id, chat_id, name, phone_no, prod, current_datetime, upsize=0):
    data = {
        "id": order_id,
        "name": '{}'.format(name),
        "datetime": '{}'.format(current_datetime),
        "chat_id": '{}'.format(chat_id),
        "phone_number": '{}'.format(phone_no),
        "product": '{}'.format(prod),
        "is_completed": 0,
        "stage": 0,
        "upsize": upsize
    }
    db.child("orders").child(order_id).set(data)
    print('uploaded')


def get_pending_orders(chat_id):
    new_list = []
    orders = db.child("orders").get()
    data = orders.val()
    for i in data:
        try:
            if i['chat_id'] == str(chat_id) and i['is_completed'] == 0:
                new_list.append(i)
        except:
            pass
    return new_list