import json

class DataStorage:

	def __init__(self):
		self.path = "app/data/data.json"
		self.storage = {}

	def load(self):
		with open(self.path) as file:
			self.storage = json.load(file)
			return self

	def save(self):
		with open(self.path, 'w') as file:
			json.dump(self.storage, file, indent=4)
			return True

	async def get_pars_config(self):
		self.load()
		return (self.storage['pars'], self.storage['pars_limit'])

	# записываем ID сообщения, чтобы оно не высвечивалось несколько раз
	async def add_pars_data(self, channel, message_id):
		self.load()
		if not channel in self.storage['pars_data']:
			self.storage['pars_data'][channel] = []
		self.storage['pars_data'][channel].append(message_id)
		self.save()

	# читаем все записанные сообщения в определенном чате
	async def get_pars_data(self, channel):
		self.load()
		if not channel in self.storage['pars_data']:
			self.storage['pars_data'][channel] = []
		return self.storage['pars_data'][channel]