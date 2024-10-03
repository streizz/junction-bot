import sqlite3


from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramMigrateToChat


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


class AddDestination(StatesGroup):
    chat = State()


class DeleteDestination(StatesGroup):
    chat = State()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Привет, {message.from_user.first_name}',
                         reply_markup=kb.main)
    
@router.message(F.text == 'Каналы')
async def manage_channel(message: Message):
    await message.answer("Выберите действие с каналами",
                         reply_markup=kb.settings_channel)
    
@router.message(F.text == 'Ключевые слова')
async def manage_kw(message: Message):
    await message.answer("Выберите действие с ключевыми словами",
                         reply_markup=kb.settings_kw)

@router.message(F.text == 'Слова исключения')
async def manage_bw(message: Message):
    await message.answer("Выберите действие со словами исключениями",
                         reply_markup=kb.settings_bw)
    
@router.message(F.text == 'Настроить пересылку в чат')
async def manage_destination(message: Message):
    await message.answer("Выберите действие с чатами для отправки",
                         reply_markup=kb.settings_destination)   


#   Манипуляции каналами


@router.callback_query(F.data == "add_channel")
async def follow_channel(callback: CallbackQuery, state: FSMContext):

    await state.set_state(Follow.channel)
    await callback.message.answer('Введите @ канала \nПример: @telegram\nВы так же можете написать несколько через запятую.\nПример: @telegram,@stickers')

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


@router.callback_query(F.data == "delete_channel")
async def delete_channel(callback: CallbackQuery, state: FSMContext):

    await state.set_state(UnFollow.channel)
    await callback.message.answer('Введите @ канала \nПример: @telegram\nВы так же можете написать несколько через запятую.\nПример: @telegram,@stickers')

@router.message(UnFollow.channel)
async def delete_channel_second(message: Message, state: FSMContext):

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


@router.callback_query(F.data == "list_channel")
async def channel_list(callback: CallbackQuery):
    userid = callback.from_user.id

    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    cur.execute(f"SELECT channel FROM users WHERE userid = {userid}")
    result = cur.fetchall()
    res = ' '.join([item[0] for item in result if item]) if result else []

    if res:

        await callback.message.answer(res)

    else: 

        await callback.message.answer('Вы не отслеживаете ни одного канала')

    conn.close()


#    Манипуляции ключевыми словами


@router.callback_query(F.data == "add_kw")
async def keyword_addition_first(callback: CallbackQuery, state: FSMContext):

    await state.set_state(AddKeyword.keyword)
    await callback.message.answer('Введите ключевое слово/фразу \nПример: ищу команду \nВы так же можете написать несколько слов/фраз через запятую. \nПример: ищу,команду')

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


@router.callback_query(F.data == "delete_kw")
async def keyword_deletion_first(callback: CallbackQuery, state: FSMContext):

    await state.set_state(DeleteKeyword.keyword)
    await callback.message.answer('Введите ключевое слово/фразу \nПример: ищу команду')

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


@router.callback_query(F.data == "list_kw")
async def keyword_list(callback: CallbackQuery):
    userid = callback.from_user.id

    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    cur.execute(f"SELECT keywords FROM filters WHERE userid = {userid} AND keywords IS NOT NULL;")
    result = cur.fetchall()
    res = ', '.join([item[0] for item in result if item])

    if res:

        await callback.message.answer(res)

    else:

        await callback.message.answer('У вас нет ни одного ключевого слова')

    conn.close()


# Слова исключения

@router.callback_query(F.data == "add_bw")
async def banword_addition_first(callback: CallbackQuery, state: FSMContext):

    await state.set_state(AddBanword.banword)
    await callback.message.answer('Введите слово/фразу которую хотите исключить\nПример: ищу команду\nВы так же можете написать несколько через запятую. \nПример: ищу,команду')

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


@router.callback_query(F.data == "delete_kw")
async def banword_deletion_first(callback: CallbackQuery, state: FSMContext):

    await state.set_state(DeleteBanword.banword)
    await callback.message.answer('Введите слово/фразу \nПример: ищу команду \nВы так же можете написать несколько слов/фраз через запятую. \nПример: ищу,команду')

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


@router.callback_query(F.data == "list_bw")
async def banword_list(callback: CallbackQuery):
    userid = callback.from_user.id

    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    cur.execute(f"SELECT banwords FROM filters WHERE userid = {userid} AND banwords IS NOT NULL;")
    result = cur.fetchall()
    res = ', '.join([item[0] for item in result])

    if res:

        await callback.message.answer(res)

    else:

        await callback.message.answer('У вас нет ни одного исключения')

    conn.close()


# Каналы назначения


@router.callback_query(F.data == "add_ds")
async def add_ds(callback: CallbackQuery, state: FSMContext):

    await state.set_state(AddDestination.chat)
    await callback.message.answer('Для настройки пересылки сообщений в чат выполните следующие шаги:\n1. Добавьте этого бота в чат для пересылки и выдайте ему права на отправку сообщений (сделайте его администратором).\n2. Получите ID чата, в который будут отправляться сообщения в боте @getidallbot и отправьте ID следующим сообщением.')

@router.message(AddDestination.chat)
async def add_ds2(message: Message, state: FSMContext):

    await state.update_data(chatid=message.text)
    data = await state.get_data()
    chatid = ''.join(data['chatid'].split(','))

    try:

        chat = await message.bot.get_chat(chatid)
        chatname = chat.title
        userid = message.from_user.id

        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        cur.execute(f"SELECT tochat FROM destination WHERE userid={userid};")
        res = cur.fetchall()

        if (chatid,) in res:

            await message.answer(f'Бот уже пересылает сообщения в {chatname}')

        else:

            await message.answer(f'Бот теперь будет пересылать сообщения в {chatname}')
            cur.execute("INSERT INTO destination (userid, tochat) VALUES (?, ?);", (userid, chatid))
            conn.commit()

        conn.close()

    except:

        await message.answer(f'Чат {chatid} не найден.')

    await state.clear()


@router.callback_query(F.data == "delete_ds")
async def delete_ds(callback: CallbackQuery, state: FSMContext):

    await state.set_state(DeleteDestination.chat)
    await callback.message.answer('Введите ID чата (можно получить в боте @getidallbot)')

@router.message(DeleteDestination.chat)
async def delete_ds2(message: Message, state: FSMContext):

    await state.update_data(chatid=message.text)
    data = await state.get_data()
    chatid = ''.join(data['chatid'].split(','))

    try:

        chat = await message.bot.get_chat(chatid)
        chatname = chat.title
        userid = message.from_user.id

        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        cur.execute(f"SELECT tochat FROM destination WHERE userid = {userid};")
        res = cur.fetchall()

        if (chatid,) not in res:

            await message.answer(f'Бот не отправляет сообщения в {chatname}')

        else:

            await message.answer(f'Теперь бот не будет отправлять сообщения в {chatname}')
            cur.execute(f"DELETE FROM destination WHERE userid=? AND tochat=?;", (userid, chatid))
            conn.commit()

        conn.close()

    except:

        await message.answer(f'Чат {chatid} не найден.')

    await state.clear()


@router.callback_query(F.data == "list_ds")
async def ds_list(callback: CallbackQuery):
    userid = callback.from_user.id

    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    cur.execute(f"SELECT tochat FROM destination WHERE userid = {userid}")
    result = cur.fetchall()
    res = [item[0] for item in result if item] if result else []
    res1 = []

    if res:
        try:

            for i in range(len(res)):

                chat = await callback.bot.get_chat(res[i])
                chatname = chat.title
                res1.append(f'{res[i]} : {chatname}')

            await callback.message.answer('\n'.join(res1))
        
        except TelegramMigrateToChat:

            cur.execute(f"DELETE * FROM destination WHERE userid = {userid}")
            conn.commit()

    else: 

        await callback.message.answer('Сообщения бота не переадресовываются')

    conn.close()