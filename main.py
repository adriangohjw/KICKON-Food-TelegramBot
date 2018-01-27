from access import Token
import keyboard as kb

import json
import time
from pprint import pprint
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import LabeledPrice, ShippingOption
from telepot.delegate import (
    per_invoice_payload, pave_event_space, create_open,
    per_message, call)
from datetime import datetime

menu_file = open('menu.json')
menu_json = json.load(menu_file)
menu_dict = json.loads(json.dumps(menu_json))['menu']

orders_file = open('order_list.json')
orders_json = json.load(orders_file)
orders_dict = json.loads(json.dumps(orders_json))['orders']

# calling data
# for i in menu_dict:
#     print(i['backend_name'])
#     print(i['price'])


class OrderProcessor(telepot.helper.InvoiceHandler):
    def __init__(self, *args, **kwargs):
        super(OrderProcessor, self).__init__(*args, **kwargs)

    def on_shipping_query(self, msg):
        query_id, from_id, invoice_payload = telepot.glance(msg, flavor='shipping_query')

        print('Shipping query:')
        pprint(msg)

        bot.answerShippingQuery(
            query_id, True,
            shipping_options=[
                ShippingOption(id='self_collection', title='Self Collection', prices=[
                    LabeledPrice(label='self_collection', amount=0)]),
                ShippingOption(id='delivery', title='Delivery', prices=[
                    LabeledPrice(label='delivery', amount=390)])])

    def on_pre_checkout_query(self, msg):
        query_id, from_id, invoice_payload = telepot.glance(msg, flavor='pre_checkout_query')

        print('Pre-Checkout query:')
        pprint(msg)

        bot.answerPreCheckoutQuery(query_id, True)

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)

        if content_type == 'successful_payment':
            print('Successful payment RECEIVED!!!')
            pprint(msg)
        else:
            print('Chat message:')
            pprint(msg)


def send_invoice(seed_tuple):
    msg = seed_tuple[1]

    pprint(msg)
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    # try:
    if content_type == 'text':
        if msg['text'] == '/menu':
            pass
        elif msg['text'] == '/order':
            for order in orders_dict:
                if chat_id == order['chat_id']:

                    description = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n'
                    for order in orders_dict:
                        for item in order['orders']:
                            description += str(item[0]) + '\n'

                    sent = bot.sendInvoice(
                        chat_id=chat_id,
                        title='Checkout',
                        description=description,
                        payload='a-string-identifying-related-payment-messages-tuvwxyz',
                        provider_token=Token.PAYMENT_PROVIDER_TOKEN,
                        start_parameter=order['chat_id'],
                        currency='SGD',
                        photo_url='https://d1nqx6es26drid.cloudfront.net/app/uploads/2015/06/18104056/ramanda-bundles.png',
                        prices=[LabeledPrice(label=item[0], amount=item[1]) for order in orders_dict for item in order['orders']],
                        need_shipping_address=True, need_phone_number=True
                    )
                    print(sent)
                    break
        else:
            try:
                for i in menu_dict:
                    if str(msg['text']).upper() == str(i['frontend_name']).upper():
                        if 'UPSIZE' in str(msg['text']).upper():
                            title = i['frontend_name'] + ' Upsized'
                            label = 'Upsize'
                            price = str(int(i['price'])+150)
                        else:
                            title = i['frontend_name']
                            label = 'No Upsize'
                            price = i['price']
                else:
                    bot.sendMessage(chat_id, text='error sending invoice')
            except Exception as e:
                print(e)
                bot.sendMessage(chat_id, text='Try selecting with the buttons', reply_markup=kb.custom_keyboard)
    # except Exception as e:
    #     print(e)
    #     bot.sendMessage(chat_id, text='fuck')

bot = telepot.DelegatorBot(Token.TOKEN, [
    (per_message(flavors=['chat']), call(send_invoice)),
    pave_event_space()(
        per_invoice_payload(), create_open, OrderProcessor, timeout=30,
    )
])

print('Listening...')
MessageLoop(bot).run_as_thread()

while 1:
    time.sleep(10)
