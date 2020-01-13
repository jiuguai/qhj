import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbosity', 
	help="increase output verbosity",
	)
parser.add_argument('-s', '--status', action='store_true', 
	help="increase output status",
	)
	# action="store_true"
try:
	args = parser.parse_args('-v z '.split())
	print(args)
except:
	print(123)

