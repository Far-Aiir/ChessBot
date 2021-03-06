import re
from bson.objectid import ObjectId

class Parameter():
	type_name = "object"
	name = "arg"
	required = True

	def __init__(self, name = None, required = True):
		self.required = required
		if name:
			self.name = name
	
	async def parse(self, ctx, arg):
		return None
	
	def usage_string(self):
		return ""

class ParamUser(Parameter):
	type_name = "user"
	name = "user"

	async def parse(self, ctx, arg):
		mention_re = re.search(r"^<@!?(\d+)>$", arg)
		id_re = re.search(r"^(\d+)$", arg)

		id = None

		if mention_re:
			id = mention_re.group(1)
		elif id_re:
			id = id_re.group(1)
		
		try:
			id = int(id)
			return await ctx.bot.fetch_user(id)
		except:
			return None

class ParamGameID(Parameter):
	type_name = "game_id"
	name = "game"

	async def parse(self, ctx, arg):
		try:
			ObjectId(arg)
			return arg
		except:
			return None

class ParamString(Parameter):
	type_name = "text"
	name = "text"

	async def parse(self, ctx, arg):
		return str(arg)

class ParamInt(Parameter):
	type_name = "number"
	name = "number"

	async def parse(self, ctx, arg):
		try:
			return int(arg)
		except:
			return None

# This is probably a terrible idea, still think I'm a genius for it though
# You know you're doing something wrong when you self roll type unions
class ParamUnion(Parameter):
	name = "query"
	def __init__(self, params, name=None, required=True):
		super(ParamUnion, self).__init__(name, required)

		self.params = params
		self.type_name = "/".join([param.type_name for param in self.params])

		if not name:
			self.name = "/".join([param.name for param in self.params])
	
	async def parse(self, ctx, arg):
		for param in self.params:
			parsed = await param.parse(ctx, arg)
			if parsed:
				return parsed
		
		return None


class ParamChoice(Parameter):
	type_name = "choice"
	name = "choice"

	def __init__(self, name=None, required=True, options=None):
		super(ParamChoice, self).__init__(name, required)

		self.options = options if options else None

	async def parse(self, ctx, arg):
		if str(arg) in self.options:
			return str(arg)
		
		return None
	
	def usage_string(self):
		return "Must be one of: `{}`!".format(", ".join(self.options))