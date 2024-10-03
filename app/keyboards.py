from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Каналы'), 
     KeyboardButton(text='Ключевые слова'), 
     KeyboardButton(text='Слова исключения')],

    [KeyboardButton(text='Настроить пересылку в чат')]],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие")


settings_channel = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Добавить', callback_data='add_channel'), 
                                                          InlineKeyboardButton(text='Удалить', callback_data='delete_channel'), 
                                                          InlineKeyboardButton(text='Список', callback_data='list_channel')]
                                                          ])

settings_kw = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Добавить', callback_data='add_kw'), 
                                                          InlineKeyboardButton(text='Удалить', callback_data='delete_kw'), 
                                                          InlineKeyboardButton(text='Список', callback_data='list_kw')]
                                                          ])

settings_bw = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Добавить', callback_data='add_bw'), 
                                                          InlineKeyboardButton(text='Удалить', callback_data='delete_bw'), 
                                                          InlineKeyboardButton(text='Список', callback_data='list_bw')]
                                                          ])

settings_destination = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Добавить', callback_data='add_ds'), 
                                                          InlineKeyboardButton(text='Удалить', callback_data='delete_ds'), 
                                                          InlineKeyboardButton(text='Список', callback_data='list_ds')]
                                                          ])