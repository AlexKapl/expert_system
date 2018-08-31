import sys
from repl import ExpertSystem


def print_help(usageMsg):
	print(usageMsg)
	print('\t-v: verbose - print more')
	print('\t-h: print help and quit')
	print('\t-r: start "REPL" mode')
	print('\t' + '-----' * 10)
	print('\tYou can use keys separatly or combine them')


def parse_args():
	keys = {
		'verbose' : False,
		'repl'    : False,
		'help'    : False,
		'file'    : None,
	}
	for arg in sys.argv[1:]:
		if arg[0:5] == '/dev/':
			print('Not a valid file')
			sys.exit(0)
		if (arg == '-v'):
			keys['verbose'] = True
		elif (arg == '-r'):
			keys['repl'] = True
		elif (arg == '-h'):
			keys['help'] = True
		else:
			if keys['file'] is None:
				keys['file'] = arg
			else:
				return None
	return keys


if __name__ == "__main__":
	try:
		usageMsg = "Usage: python3 " + sys.argv[0] + "[-v, -h, -r] [<file_name>]"
		if (sys.argv == []):
			print(usageMsg)
		else:
			keys = parse_args()
			if keys == None:
				print(usageMsg)
			elif keys['help']:
				print_help(usageMsg)
			else:
				solver = ExpertSystem()
				if keys['file'] is not None:
					solver.parse_file(keys['file'])

				if keys['repl']:
					solver.repl_cycle()
				else:
					if keys['file'] is None:
						print(usageMsg)
					elif solver.is_valid():
						if keys['verbose']:
							solver.print_system()
						solver.print_queries()
						solver.print_solutions()
	except KeyboardInterrupt:
		print('\nWhy so rude?')
