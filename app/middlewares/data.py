from aiogram import BaseMiddleware


class DataMiddleware(BaseMiddleware):
	skip_patterns = ['error', 'update']

	def __init__(self, data_obj):
		super().__init__()
		self.data = data_obj


	async def pre_process(self, obj, data, *args):
		data['data'] = self.data


	async def post_process(self, obj, data, *args):
		del data['data']
		self.data.save()