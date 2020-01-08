import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbosity', 
	help="increase output verbosity",
	)
	# action="store_true"
try:
	args = parser.parse_args('-v z '.split())
	print(args)
except:
	print(123)

