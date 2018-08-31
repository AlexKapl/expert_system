import os
import sys
from ast import Fact
from parse import ExpertParser
from tatsu.exceptions import FailedToken, FailedParse

class ExpertSystem():
	"""ExpertSystem: class that contains all logic for evaluate whole task"""
	def __init__(self):
		self._rules = None
		self._init  = None
		self._query = None
		self.parser = ExpertParser()
		self.commands = {
			'read'    : self.parse_file_dialog,
			'delete'  : self.delete_rule_dialog,
			'help'    : self.print_help,
			'print'   : self.print_system,
			'queries' : self.print_queries,
			'solve'   : self.print_solutions,
			'clean'   : self.clean_screen,
			'quit'    : sys.exit,
		}

	def is_valid(self):
		return self._rules != None and self._init != None and self._query != None

	# ------------------- REPL cycle and dialogs ---------------------------------

	def repl_cycle(self):
		try:
			while True:
				query = input('>>> ').strip()
				if query in self.commands:
					self.commands[query]()
				elif query.startswith('->'):
					self.parse_repl_query(query[2:])
				elif query != '' and query[0] in ['=', '?']:
					self.parse_repl_query(query)
				else:
					print('Unsupported command. Try again or type "help" to show commands list')
				print()
		except EOFError:
			print('\nBye!')

	def print_help(self):
		help = [
			['read',					'read new tree from file'],
			['delete',					'delete one of excisiting rules'],
			['->[Expr]+ => [Expr]+',	'add new rule'],
			['=[Fact]*',				'set new initial section'],
			['?[Fact]+',				'set new query'],
			['help',					'print help'],
			['print',					'print current tree'],
			['queries',					'print rules for current query list'],
			['clean',					'clean screen'],
			['solve',					'evaluate current query list'],
			['quit',					'quit Expert System'],
		]
		for item in help:
			print('{0:20} : {1}'.format(item[0], item[1]))

	def dialog_template(self, request, fn):
		query = input('Enter ' + request + ' or "q" to go back\n')
		if query != 'q':
			fn(query)

	def parse_file_dialog(self):
		self.dialog_template('file name', self.parse_file)

	def delete_rule_dialog(self):
		for i in range(len(self._rules)):
			print (i, ': ', str(self._rules[i]))
		self.dialog_template('number of rule you want delete', self.delete_rule)

	def clean_screen(self):
		os.system('clear')

	# ------------------- Update repl tree state ---------------------------------

	def refresh(self):
		if self._rules is not None:
			for rule in self._rules:
				if rule.valid is not True:
					print(rule.valid)
					self._rules.remove(rule)
		Fact.refresh(self._init)

	def delete_rule(self, id):
		if not id.isdigit():
			print('Invalid id, only integer!')
		else:
			id = int(id)
			if id not in range(len(self._rules)):
				print('Invalid rule number!')
			else:
				self._rules.pop(id)
				self.refresh()

	def parse_file(self, query):
		def parse(file):
			ast = self.parser.parse_file(file)
			if ast is not None:
				if ast != [[], [], []]:
					self._rules = ast[0]
					self._init =  ast[1][0]
					self._query = ast[2][0]
					self.refresh()
				else:
					print('Empty file!')
		self.secure_parse(parse)(query)

	def parse_repl_query(self, query):
		def parse(rule):
			ret = self.parser.parse_str(rule)
			if ret != [[], [], []]:
				if ret[0] != []:
					self._rules.append(ret[0][0])
				elif ret[1] != []:
					self._init = ret[1][0]
				elif ret[2] != []:
					self._query = ret[2][0]
				self.refresh()
		self.secure_parse(parse)(query)

	def secure_parse(self, parse_fn):
		def wrap(query):
			try:
				parse_fn(query)
			except (FailedToken, FailedParse) as e:
				exc = str(e).split('\n')[0:3]
				print('\n'.join(exc))
			except Exception as e:
				print(e)
		return wrap

	# -------------------- ------ Print methods ---------------------------------

	def _print_query_list(self, fn):
		for fact in self._query.list:
			print(str(fact) + ': ', fn(fact))

	def print_queries(self):
		self._print_query_list(lambda fact: '\n^---'.join(fact.merge()))

	def print_solutions(self):
		self._print_query_list(lambda fact: fact.eval())

	def print_system(self):
		def check_print(check, fn, either):
			if check != [] and check is not None:
				print(fn(check), '\n')
			else:
				print("You didn't set {}!\n".format(either))

		check_print(self._rules, lambda p: '\n'.join(map(str, p)), 'rules')
		check_print(self._init,  str, 'init')
		check_print(self._query, str, 'query')

	def get_solutions(self):
		if self.is_valid():
			return [str(fact.eval()) for fact in self._query.list]
		else:
			return []
