from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Отслеживать канал'), KeyboardButton(text='Добавить ключевые слова')],
    [KeyboardButton(text='Перестать отслеживать канал'), KeyboardButton(text='Удалить ключевые слова')],
    [KeyboardButton(text='Список отслеживаемых каналов'), KeyboardButton(text='Список ключевых слов')]
])



