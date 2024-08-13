from pyrogram import Client
from config import API_ID, API_HASH
from app.data.data import DataStorage

import sqlite3

class pg:

	def __init__(self, bot):

		self.client = Client(
			"client",
			api_id=API_ID,
			api_hash=API_HASH
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

							link = f't.me/{chat.username}/{message.id}' if message.from_user.username else message.from_user.first_name
							text = [
								f"🔔 {chat.username} | {link}\n",
								txt
							]
						except:
							await self.client.join_chat(channel_id)

						conn = sqlite3.connect('data.db')
						cur = conn.cursor()
						cur.execute("SELECT userid FROM users WHERE channel = ?", (channel_id,))
						res = cur.fetchall()
						users = [item[0] for item in res]

						for id in users:

							cur.execute("SELECT keywords FROM filters WHERE userid = ?", (id,))
							res = cur.fetchall()
							keywords = [item[0] for item in res]

							conn.close()

							if keywords:
								for word in keywords:

									if word.lower() in txt.lower():

										await self.bot.send_message(id, '\n'.join(text), disable_web_page_preview=True)

							else:
								await self.bot.send_message(id, '\n'.join(text), disable_web_page_preview=True)

						await data.add_pars_data(channel_id, message.id)