import sqlite3


from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext


import app.keyboards as kb


router = Router()


class Follow(StatesGroup):
    channel = State()


class UnFollow(StatesGroup):
    channel = State()


class AddKeyword(StatesGroup):
    keyword = State()


class DeleteKeyword(StatesGroup):
    keyword = State()


class AddBanword(StatesGroup):
    banword = State()


class DeleteBanword(StatesGroup):
    banword = State()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Привет, {message.from_user.first_name}',
                         reply_markup=kb.main)


#   Манипуляции каналами


@router.message(F.text == "Отслеживать канал")
async def follow_channel(message: Message, state: FSMContext):

    await state.set_state(Follow.channel)
    await message.answer('Введите @ канала \nПример: @telegram\nВы так же можете написать несколько через запятую.\nПример: @telegram,@stickers')

@router.message(Follow.channel)
async def follow_channel_second(message: Message, state: FSMContext):

    await state.update_data(channelname=message.text)
    data = await state.get_data()
    channel_li = data['channelname'].split(',')

    for i in channel_li:
        try:

            chat = await message.bot.get_chat(i)
            chatname = chat.title
            userid = message.from_user.id

            conn = sqlite3.connect('data.db')
            cur = conn.cursor()
            cur.execute(f"SELECT channel FROM users WHERE userid={userid};")
            res = cur.fetchall()

            if (i,) in res:

                await message.answer(f'Вы уже отслеживаете {chatname}')

            else:

                await message.answer(f'Вы добавили канал {chatname}')
                cur.execute("INSERT INTO users (userid, channel) VALUES (?, ?);", (userid, i))
                conn.commit()

            conn.close()

        except:

            await message.answer(f'Чат {i} не найден.')

    await state.clear()


@router.message(F.text == "Перестать отслеживать канал")
async def follow_channel(message: Message, state: FSMContext):

    await state.set_state(UnFollow.channel)
    await message.answer('Введите @ канала \nПример: @telegram\nВы так же можете написать несколько через запятую.\nПример: @telegram,@stickers')

@router.message(UnFollow.channel)
async def follow_channel_second(message: Message, state: FSMContext):

    await state.update_data(channelname=message.text)
    data = await state.get_data()
    channel_li = data['channelname'].split(',')

    for i in channel_li:
        try:

            chat = await message.bot.get_chat(i)
            chatname = chat.title
            userid = message.from_user.id

            conn = sqlite3.connect('data.db')
            cur = conn.cursor()
            cur.execute(f"SELECT channel FROM users WHERE userid = {userid};")
            res = cur.fetchall()

            if (i,) not in res:

                await message.answer(f'Вы не отслеживаете {chatname}')

            else:

                await message.answer(f'Вы перестали отслеживать канал {chatname}')
                cur.execute(f"DELETE FROM users WHERE userid=? AND channel=?;", (userid, i))
                conn.commit()

            conn.close()

        except:

            await message.answer(f'Чат {i} не найден.')

    await state.clear()


@router.message(F.text == 'Список отслеживаемых каналов')
async def channel_list(message: Message):
    userid = message.from_user.id

    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    cur.execute(f"SELECT channel FROM users WHERE userid = {userid}")
    result = cur.fetchall()
    res = ' '.join([item[0] for item in result if item]) if result else []

    if res:

        await message.answer(res)

    else: 

        await message.answer('Вы не отслеживаете ни одного канала')

    conn.close()


#    Манипуляции ключевыми словами


@router.message(F.text == 'Добавить ключевые слова')
async def keyword_addition_first(message: Message, state: FSMContext):

    await state.set_state(AddKeyword.keyword)
    await message.answer('Введите ключевое слово/фразу \nПример: ищу команду \nВы так же можете написать несколько слов/фраз через запятую. \nПример: ищу,команду')

@router.message(AddKeyword.keyword)
async def keyword_addition_second(message: Message, state: FSMContext):

    await state.update_data(keyword_added=message.text)
    data = await state.get_data()
    userid = message.from_user.id

    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    cur.execute(f"SELECT keywords FROM filters WHERE userid = {userid};") 
    result = cur.fetchall()
    res = [item[0] for item in result]
    wordlist = data["keyword_added"].split(',')

    for i in wordlist:
        if i.lower() in res:

            await message.answer(f'"{i}" уже есть в списке ключевых слов')

        else:

            await message.answer(f'Вы добавили "{i}" в список ключевых слов')
            cur.execute("INSERT INTO filters (userid, keywords) VALUES (?, ?);", (userid, i.lower()))
            conn.commit()

    await state.clear()
    conn.close()


@router.message(F.text == 'Удалить ключевые слова')
async def keyword_deletion_first(message: Message, state: FSMContext):

    await state.set_state(DeleteKeyword.keyword)
    await message.answer('Введите ключевое слово/фразу \nПример: ищу команду')

@router.message(DeleteKeyword.keyword)
async def keyword_deletion_second(message: Message, state: FSMContext):

    await state.update_data(keyword_deleted=message.text)
    data = await state.get_data()
    userid = message.from_user.id

    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    cur.execute(f"SELECT keywords FROM filters WHERE userid = {userid};") 
    result = cur.fetchall()
    res = [item[0] for item in result]
    wordlist = data["keyword_deleted"].split(',')

    for i in wordlist:
        if i.lower() not in res:

            await message.answer(f'"{i}" отсутствует в списке ключевых слов')

        else:

            await message.answer(f'Вы удалили "{i}" из списка ключевых слов')
            cur.execute(f"DELETE FROM filters WHERE userid=? AND keywords=?;", (userid, i.lower()))
            conn.commit()

    await state.clear()
    conn.close()


@router.message(F.text == 'Список ключевых слов')
async def keyword_list(message: Message):
    userid = message.from_user.id

    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    cur.execute(f"SELECT keywords FROM filters WHERE userid = {userid} AND keywords IS NOT NULL;")
    result = cur.fetchall()
    res = ', '.join([item[0] for item in result if item])

    if res:

        await message.answer(res)

    else:

        await message.answer('У вас нет ни одного ключевого слова')

    conn.close()


@router.message(F.text == 'Добавить слова-исключения')
async def banword_addition_first(message: Message, state: FSMContext):

    await state.set_state(AddBanword.banword)
    await message.answer('Введите слово/фразу которую хотите исключить\nПример: ищу команду\nВы так же можете написать несколько через запятую. \nПример: ищу,команду')

@router.message(AddBanword.banword)
async def banword_addition_second(message: Message, state: FSMContext):

    await state.update_data(banword_added=message.text)
    data = await state.get_data()
    userid = message.from_user.id

    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    cur.execute(f"SELECT banwords FROM filters WHERE userid = {userid};") 
    result = cur.fetchall()
    res = [item[0] for item in result]
    wordlist = data['banword_added'].split(',')

    for i in wordlist:
        if i.lower() in res:

            await message.answer(f'"{i}" уже есть в списке ключевых слов')

        else:

            await message.answer(f'Вы добавили "{i}" в список исключений')
            cur.execute("INSERT INTO filters (userid, banwords) VALUES (?, ?);", (userid, i.lower()))
            conn.commit()

    await state.clear()
    conn.close()


@router.message(F.text == 'Удалить слова-исключения')
async def banword_deletion_first(message: Message, state: FSMContext):

    await state.set_state(DeleteBanword.banword)
    await message.answer('Введите слово/фразу \nПример: ищу команду \nВы так же можете написать несколько слов/фраз через запятую. \nПример: ищу,команду')

@router.message(DeleteBanword.banword)
async def banword_deletion_second(message: Message, state: FSMContext):

    await state.update_data(banword_deleted=message.text)
    data = await state.get_data()
    userid = message.from_user.id

    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    cur.execute(f"SELECT banwords FROM filters WHERE userid = {userid};") 
    result = cur.fetchall()
    res = [item[0] for item in result]
    wordlist = data['banword_deleted'].split(',')

    for i in wordlist:
        if i.lower() not in res:

            await message.answer(f'"{i}" отсутствует в списке исключений')

        else:

            await message.answer(f'Вы удалили слово/фразу "{i}" из списка исключений')

            cur.execute(f"DELETE FROM filters WHERE userid=? AND banwords=?;", (userid, i.lower()))
            conn.commit()

    await state.clear()
    conn.close()


@router.message(F.text == 'Список слов-исключений')
async def banword_list(message: Message):
    userid = message.from_user.id

    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    cur.execute(f"SELECT banwords FROM filters WHERE userid = {userid} AND banwords IS NOT NULL;")
    result = cur.fetchall()
    res = ', '.join([item[0] for item in result])

    if res:

        await message.answer(res)

    else:

        await message.answer('У вас нет ни одного исключения')

    conn.close()