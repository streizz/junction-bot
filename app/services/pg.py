from pyrogram import Client
from pyrogram.errors.exceptions.bad_request_400 import InviteRequestSent, InviteHashExpired
from config import API_ID, API_HASH, PHONE
from app.data.data import DataStorage
from aiogram.exceptions import TelegramMigrateToChat
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import asyncio

import sqlite3

class pg:

	def __init__(self, bot):

		self.client = Client(
			"client",
			api_id=API_ID,
			api_hash=API_HASH,
			phone_number=PHONE
		)

		self.bot = bot

	async def pars(self):

		pars = True
		pars_limit = 20
		data = DataStorage()

		conn = sqlite3.connect('data.db')
		cur = conn.cursor()
		cur.execute("SELECT channel FROM users")
		res = cur.fetchall()
		pars_id = set([item[0] for item in res])
		conn.close()

		if not pars: return pars
		
		async with self.client as client:

			for channel_id in pars_id:

				try: await client.get_chat(channel_id)

				except:

					conn = sqlite3.connect('data.db')
					cur = conn.cursor()
					cur.execute("DELETE FROM users WHERE channel = ?", (channel_id,))
					conn.commit()
					conn.close()

					continue

				async for message in client.get_chat_history(channel_id, limit=pars_limit):

					txt = message.caption if message.caption else message.text

					if not txt:
						continue
					
					if message.id in await data.get_pars_data(channel=channel_id):
						continue

					else:

						chat = await client.get_chat(channel_id)

						try:

							link = f't.me/{chat.username}/{message.id}'
							text = [
								f"🔔 {chat.username} | {link}\n",
								txt
							]
						except:
							try:

								await self.client.join_chat(channel_id)

							except InviteRequestSent or InviteHashExpired:

								conn = sqlite3.connect('data.db')
								cur = conn.cursor()
								cur.execute("DELETE * FROM users WHERE channel = ?", (channel_id,))
								continue
							

						conn = sqlite3.connect('data.db')
						cur = conn.cursor()
						cur.execute("SELECT userid FROM users WHERE channel = ?", (channel_id,))
						res = cur.fetchall()
						users = [item[0] for item in res]

						for id in users:

							cur.execute("SELECT tochat FROM destination WHERE userid = ?", (id,))
							res = cur.fetchall()
							destination = [item[0] for item in res] if res else id

							cur.execute("SELECT keywords FROM filters WHERE userid = ? AND keywords IS NOT NULL", (id,))
							res = cur.fetchall()
							keywords = [item[0] for item in res]

							cur.execute("SELECT banwords FROM filters WHERE userid = ? AND banwords IS NOT NULL", (id,))
							res1 = cur.fetchall()
							banwords = [item1[0] for item1 in res1]

							conn.close()

							keyflag = False
							banflag = False

							stemmer = SnowballStemmer("russian")
							text = txt.lower()
							tokens = word_tokenize(text)
							stemmed_words = [stemmer.stem(word) for word in tokens]

							if keywords:
								for word in keywords:
									if word:
										if word.lower() in stemmed_words:
												
												keyflag = True

							if not keywords:
								keyflag = True

							if banwords:
								for banword in banwords:
									if banword:
										if banword.lower() in stemmed_words:

											banflag = True
											
							if keyflag and not banflag:
								if destination != id:
									for chat in destination:
										try:

											await self.bot.send_message(chat, '\n'.join(text), disable_web_page_preview=True)

										except TelegramMigrateToChat:

											conn = sqlite3.connect('data.db')
											cur = conn.cursor()
											cur.execute(f"DELETE * FROM destination WHERE userid = {chat}")
											conn.commit()
											conn.close()

								else:
									
									await self.bot.send_message(id, '\n'.join(text), disable_web_page_preview=True)

						await data.add_pars_data(channel_id, message.id)