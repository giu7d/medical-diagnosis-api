import valid_values 

class Test_valid:

	@staticmethod
	def test_is_integer_from_valid():
		valid = valid_values.Valid_values()

		x,y = valid.is_integer("string")
		if x:print("string is a integer , ret=",y)

		x,y = valid.is_integer(0.1)
		if x:print("0.1 is a integer , ret=",y)

		x,y = valid.is_integer("1010-20-30")
		if x:print("1010-20-30 is a integer , ret=",y)

		x,y = valid.is_integer(30)
		if x:print("30 is a integer , ret=",y)

		x,y = valid.is_integer('{"a":2}')
		if x:print("'{a:2}' is a integer , ret=",y)


	@staticmethod
	def test_is_json_from_valid():
		valid = valid_values.Valid_values()

		x,y = valid.is_json("string")
		if x:print("string is a json , ret=",y)

		x,y = valid.is_json(0.1)
		if x:print("0.1 is a json , ret=",y)

		x,y = valid.is_json("1010-20-30")
		if x:print("1010-20-30 is a json , ret=",y)

		x,y = valid.is_json(30)
		if x:print("30 is a json , ret=",y)

		x,y = valid.is_json('{"a":2}')
		if x:print("'{a:2}' is a json , ret=",y)


	@staticmethod
	def test_is_date_from_valid():
		valid = valid_values.Valid_values()

		x,y = valid.is_date("string")
		if x:print("string is a date , ret=",y)

		x,y = valid.is_date(0.1)
		if x:print("0.1 is a date , ret=",y)

		x,y = valid.is_date("1010-20-30")
		if x:print("1010-20-30 is a date , ret=",y)

		x,y = valid.is_date(30)
		if x:print("30 is a date , ret=",y)

		x,y = valid.is_date('{"a":2}')
		if x:print("'{a:2}' is a date , ret=",y)


	@staticmethod
	def test_is_string_from_valid():
		valid = valid_values.Valid_values()

		x,y = valid.is_string("string")
		if x:print("string is a string , ret=",y)

		x,y = valid.is_string(0.1)
		if x:print("0.1 is a string , ret=",y)

		x,y = valid.is_string("1010-20-30")
		if x:print("1010-20-30 is a string , ret=",y)

		x,y = valid.is_string(30)
		if x:print("30 is a string , ret=",y)

		x,y = valid.is_string('{"a":2}')
		if x:print("'{a:2}' is a string , ret=",y)


	@staticmethod
	def test_is_norm_from_valid():
		valid = valid_values.Valid_values()

		x,y = valid.is_norm("string")
		if x:print("string is a norm , ret=",y)

		x,y = valid.is_norm(0.1)
		if x:print("0.1 is a norm , ret=",y)

		x,y = valid.is_norm("1010-20-30")
		if x:print("1010-20-30 is a norm , ret=",y)

		x,y = valid.is_norm(30)
		if x:print("30 is a norm , ret=",y)

		x,y = valid.is_norm('{"a":2}')
		if x:print("'{a:2}' is a norm , ret=",y)


if __name__ == "__main__":
	t = Test_valid()
	t.test_is_integer_from_valid()
	t.test_is_json_from_valid()
	t.test_is_date_from_valid()
	t.test_is_string_from_valid()
	t.test_is_norm_from_valid()

