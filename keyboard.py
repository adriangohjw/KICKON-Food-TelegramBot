from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# default custom keyboard
# called by index.py due to unaccounted user's input, prompting them to make a selection from the keyboard instead
custom_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='McSpicy'), KeyboardButton(text='Double McSpicy')]
    ],
    resize_keyboard=True
)


def custom_inline(price):
    my_text = "Buy NOW: Pay ${:.2f}".format(int(price)/100)
    custom_inline = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=my_text, pay=True)]
        ]
    )
    return custom_inline

# custom_keyboard = ReplyKeyboardMarkup(
#     keyboard=[
#         [KeyboardButton(text='McSpicy'), KeyboardButton(text='Double McSpicy')],
#         [KeyboardButton(text='Cheeseburger'), KeyboardButton(text='Double Cheeseburger')],
#         [KeyboardButton(text='Chicken McNuggets'), KeyboardButton(text='Fillet-O-Fish')],
#         [KeyboardButton(text='McChicken'), KeyboardButton(text='Big Mac'), KeyboardButton(text='McWings')],
#     ],
#     resize_keyboard=True
# )
