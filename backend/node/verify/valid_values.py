class Valid_values:

	@staticmethod
	def is_integer(value):
			 return type(value) == int , value

	@staticmethod
	def is_json(value):
			try: return type(eval(value)) == dict , value
			except: return False , None

	@staticmethod
	def is_date(value):
			if type(value) != str : return False,None
			value = value.split('-')
			try: int(value[0]),int(value[1]),int(value[2])
			except: return False,None
			return True,'-'.join([value[0],value[1],value[2]])

	@staticmethod
	def is_string(value):
			 return type(value) == str , value

	@staticmethod
	def is_norm(value):
			if type(value) not in [float,int]: return False,None
			return (True, value) if value >= 0 and value <= 1 else (False,None)

