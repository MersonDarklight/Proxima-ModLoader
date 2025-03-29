import argparse
parser = argparse.ArgumentParser(description='A tutorial of argparse!')
parser.add_argument("--f", default="none", help="file for block")
args = parser.parse_args()
file = args.f
from time import sleep
if(file == 'none'):
	exit()
else:
	f = open(file)
	sleep(999999)