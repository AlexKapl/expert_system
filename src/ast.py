import string
from fp_utils import fold

__all__ = [
	'Fact',
	'Init',
	'Query',
	'Expression',
	'NotExpr',
	'AndExpr',
	'OrExpr',
	'XorExpr',
	'Implies',
]


class ExpertResult():
	"""ExpertResult handles undeterminated results(OR|XOR)"""
	def __init__(self, expr, fact=None, result=None):
		self.chance = float(expr)
		self.fact = fact
		if (result is not None):
			self.eval(result)

	def __str__(self):
		if self.chance == 1.0:
			return 'True'
		elif self.chance == 0.0:
			return 'False'
		else:
			return 'Maybe({:.3f})'.format(self.chance)

	def __float__(self):
		return self.chance

	def __lt__(self, that):
		return self.chance < that.chance

	def __gt__(self, that):
		return self.chance > that.chance

	def __and__(self, that):
		return self if self < that else that

	def __or__(self, that):
		return self if self > that else that

	def __xor__(self, that):
		xor = lambda l, r: ExpertResult(max(l, r) - l * r)
		return xor(self.chance, that.chance)

	def eval(self, expr):
		if type(expr) is Fact:
			return self.chance
		elif type(expr) is NotExpr:
			self.chance = 1.0 - self.chance
			return self.eval(expr.expr)
		else:
			for item in expr.list.list:
				if self.fact in item.getFacts():
					if type(expr) is not AndExpr:
						self.chance /= len(expr.list.list)
					return self.eval(item)


class Fact():
	'''Fact - basic class, contains an var name, that can be found in current namespace'''
	@classmethod
	def init_fact_tree(cls):
		cls.tree = {var: Fact(var) for var in string.ascii_uppercase}

	@classmethod
	def get_fact(cls, name):
		return cls.tree[name]

	@classmethod
	def refresh(cls, init):
		for fact in cls.tree:
			cls.tree[fact].val = None
		if init is not None:
			for fact in init.list:
				fact._set(True)

	def __init__(self, name):
		self._name = name
		self.val = None
		self.rules = []
		self.visited = False

	def __repr__(self):
		return 'Fact(' + self._name + ')'

	def __str__(self):
		return self._name

	def merge(self):
		if self.rules == []:
			return [str(self)]
		else:
			return map(lambda rule: rule.merge(), self.rules)

	def _set(self, val):
		self.val = ExpertResult(val, self)

	def eval(self):
		if self.visited:
			return ExpertResult(False, self)
		else:
			if self.val is None:
				self.visited = True
				self._set(self._eval_rules())
				self.visited = False
		return self.val

	def _eval_rules(self):
		join = []
		for rule in self.rules:
			res = rule.eval(self)
			if str(res) == 'True':
				return True
			else:
				join.append(res)
		return fold(join, ExpertResult(False, self), lambda acc, res: acc | res)

	def getFacts(self):
		return {self}

	def subscribe(self, rule):
		if rule not in self.rules:
			self.rules.append(rule)

# -----------Fact List: init(=), query(?)------------------------

class FactList():
	def __init__(self, fact_list, delim='', prefix=''):
		self.unique_list(fact_list)
		self._prefix = prefix
		self._delim = delim
		self._facts = self.fold(set(), lambda acc, fact: acc | fact.getFacts())

	def unique_list(self, fact_list):
		self.list = []
		sets = {}
		for item in fact_list:
			i_set = tuple(item.getFacts())
			set_list = sets.get(i_set, None)
			if set_list is None:
				sets[i_set] = [item]
				self.list.append(item)
			else:
				for set_item in set_list:
					if type(item) == type(set_item):
						break
				else:
					sets[i_set].append(item)
					self.list.append(item)

	def __repr__(self):
		return ', '.join(map(repr, self.list))

	def __str__(self):
		return self._prefix + self._delim.join(map(ultimate_str, self.list))

	def fold(self, init, fn):
		return fold(self.list, init, fn)

	def getFacts(self):
		return self._facts


class Init(FactList):
	def __init__(self, fact_list):
		super().__init__(fact_list, prefix='=')


class Query(FactList):
	def __init__(self, fact_list):
		super().__init__(fact_list, prefix='?')

	def __repr__(self):
		return "Q: " + super().__repr__()

# ------------------------------------------------------------------

def ultimate_str(part):
	if type(part) in [Fact, NotExpr]:
		return str(part)
	else:
		return '(' + str(part) + ')'

# -----------Expressions (not, and, or, xor)------------------------

class NotExpr():
	'''don't inherit from super class because all others can have list of args, this has only one'''
	def __init__(self, expr):
		self.expr = expr

	def __repr__(self):
		return 'Not( ' + repr(self.expr) + ' )'

	def __str__(self):
		return '!' + ultimate_str(self.expr)

	def eval(self):
		return ExpertResult(1.0 - float(self.expr.eval()))

	def getFacts(self):
		return self.expr.getFacts()


class Expression():
	def __init__(self, expr, join, init, fn):
		self.list = FactList(expr, delim=join)
		self._join = join
		self._init = init
		self._eval_fn = fn

	def __repr__(self):
		return type(self).__name__ + '(' + repr(self.list) + ')'

	def __str__(self):
		return str(self.list)

	def eval(self):
		return self.list.fold(ExpertResult(self._init), self._eval_fn)

	def getFacts(self):
		return self.list.getFacts()


class AndExpr(Expression):
	def __init__(self, expr):
		super().__init__(expr, ' + ', True, lambda acc, fact: acc & fact.eval())


class OrExpr(Expression):
	def __init__(self, expr):
		super().__init__(expr, ' | ', False, lambda acc, fact: acc | fact.eval())


class XorExpr(Expression):
	def __init__(self, expr):
		super().__init__(expr, ' ^ ', False, lambda acc, fact: acc ^ fact.eval())

# ---------------------Rules (=>)------------------------

class Implies():
	def __init__(self, If, Then):
		self.If = If
		self.Then = Then
		self.valid = True
		self.validate()

	def __repr__(self):
		return 'If( {!r} => {!r} )'.format(self.If, self.Then)

	def __str__(self):
		return '{!s} => {!s}'.format(self.If, self.Then)

	def validate(self):
		if_list = self.If.getFacts()
		for fact in self.Then.getFacts():
			if fact in if_list:
				self.valid = 'Invalid rule({0!s}): {1!r} is in both sides!'.format(self, fact)
				break
		else:
			for fact in self.Then.getFacts():
				fact.subscribe(self)

	def merge(self):
		ret = str(self.If)
		if type(self.Then) is NotExpr:
			return str(NotExpr(ret))
		else:
			return ret

	def eval(self, fact):
		ret = self.If.eval()
		return ExpertResult(ret, fact, self.Then)

	def getFacts(self):
		return self.If.getFacts() | self.Then.getFacts()

