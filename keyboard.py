from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton

# default custom keyboard
# called by index.py due to unaccounted user's input, prompting them to make a selection from the keyboard instead
custom_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='McSpicy'), KeyboardButton(text='Double McSpicy')]
    ],
    resize_keyboard=True
)

# custom_keyboard = ReplyKeyboardMarkup(
#     keyboard=[
#         [KeyboardButton(text='McSpicy'), KeyboardButton(text='Double McSpicy')],
#         [KeyboardButton(text='Cheeseburger'), KeyboardButton(text='Double Cheeseburger')],
#         [KeyboardButton(text='Chicken McNuggets'), KeyboardButton(text='Fillet-O-Fish')],
#         [KeyboardButton(text='McChicken'), KeyboardButton(text='Big Mac'), KeyboardButton(text='McWings')],
#     ],
#     resize_keyboard=True
# )
