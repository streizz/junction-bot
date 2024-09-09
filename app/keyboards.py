from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Отслеживать канал'), KeyboardButton(text='Добавить ключевые слова'), KeyboardButton(text='Добавить слова-исключения')],
    [KeyboardButton(text='Перестать отслеживать канал'), KeyboardButton(text='Удалить ключевые слова'), KeyboardButton(text='Удалить слова-исключения')],
    [KeyboardButton(text='Список отслеживаемых каналов'), KeyboardButton(text='Список ключевых слов'), KeyboardButton(text='Список слов-исключений')]
])



