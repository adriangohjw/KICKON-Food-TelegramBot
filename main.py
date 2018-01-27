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
from emoji import emojize

menu_file = open('menu.json')
menu_json = json.load(menu_file)
menu_dict = json.loads(json.dumps(menu_json))['menu']

orders_file = open('order_list.json')
orders_json = json.load(orders_file)
orders_dict = json.loads(json.dumps(orders_json))['orders']


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

    if content_type == 'text':
        if msg['text'] == '/help':
            bot.sendMessage(chat_id, parse_mode='HTML',
                            text=emojize(
                                ":hamburger: Hi! You can now order food from <b>NUS McDonald's</b>! \n"
                                ":backhand_index_pointing_down: Below is the list of commands and what they do\n\n"
                                ":white_heavy_check_mark: <b>User's command</b>\n"
                                "/menu - Display the list of food and their prices\n"
                                "/pending - Check the number of pending order\n\n"
                                ":credit_card: Use credit card number <b>4242 4242 4242 4242</b> if you do not have one "
                                "and would want to test out the bot\n\n"))
        elif msg['text'] == '/menu':
            bot.sendMessage(chat_id, parse_mode='HTML',
                            text=emojize(
                                "<b>Hi, these are the items on the menu.</b> :french_fries:\n\n"
                                ":chicken: /McSpicy - $5.80\n"
                                ":chicken: /DoubleMcSpicy - $7.65\n"
                                ":chicken: /McChicken - $3.95\n"
                                ":cow: /BigMac - $6.00\n"
                                ":cow: /Cheeseburger - $2.80\n"
                                ":cow: /DoubleCheeseburger - $4.60\n"
                                ":fish: /FiletOFish - $4.60\n"
                                ":chicken: /ChickenMcNuggets - $4.90\n"
                                ":chicken: /McWings - $4.90\n\n"
                                "<b>Upsized</b>\n"
                                ":chicken: /McSpicyUP - $7.30\n"
                                ":chicken: /DoubleMcSpicyUP - $9.15\n"
                                ":chicken: /McChickenUP - $5.45\n"
                                ":cow: /BigMacUP - $7.50\n"
                                ":cow: /CheeseburgerUP - $4.30\n"
                                ":cow: /DoubleCheeseburgerUP - $6.10\n"
                                ":fish: /FiletOFishUP - $6.10\n"
                                ":chicken: /ChickenMcNuggetsUP - $6.40\n"
                                ":chicken: /McWingsUP - $6.40\n"
                            ))
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
                name_to_compare = str(msg['text'])
                name_to_compare = name_to_compare.replace("/", "")
                name_to_compare = name_to_compare.upper()
                print(name_to_compare)
                print(name_to_compare[-2:])
                for i in menu_dict:
                    if name_to_compare.replace("UP", "") == str(i['backend_name']).upper():
                        if name_to_compare[-2:] == "UP":
                            title = i['frontend_name'] + ' Upsized'
                            label = 'Meal - Upsize'
                            price = i['price_upsize']
                        else:
                            title = i['frontend_name']
                            label = 'Meal - No Upsize'
                            price = i['price']
                        sent = bot.sendInvoice(
                            chat_id=chat_id,
                            title=title,
                            description=i['description'],
                            payload='a-string-identifying-related-payment-messages-tuvwxyz',
                            provider_token=Token.PAYMENT_PROVIDER_TOKEN,
                            start_parameter=str(chat_id),
                            currency='SGD',
                            photo_url=i['photo_url'],
                            prices=[LabeledPrice(label=label, amount=price)],
                            need_shipping_address=True, need_phone_number=True
                        )
                        print(sent)
                        break
                else:
                    bot.sendMessage(chat_id, text='error sending invoice')
            except Exception as e:
                print(e)
                bot.sendMessage(chat_id, text='Try selecting with the buttons', reply_markup=kb.custom_keyboard)

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
