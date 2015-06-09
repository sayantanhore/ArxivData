import sys
from localsettings import columns
# Custom console output functions
# ----------------------------------------------------------


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Prints coloured text
def ccprint(text, scheme):
	sys.stdout.write(scheme + text + bcolors.ENDC)

# Flushing out standard output
def flush_stdout():
	sys.stdout.flush()

# Prints heading text
def head(text, major = False):
	for i in range(int(columns)):
		if (major):
			#sys.stdout.write(bcolors.HEADER + "*" + bcolors.ENDC)
			ccprint("*", bcolors.HEADER)
		else:
			#sys.stdout.write(bcolors.HEADER + "-" + bcolors.ENDC)
			ccprint("-", bcolors.HEADER)
	flush_stdout()
	spaces = (int(columns) - len(text))/2
	for i in range(spaces):
		sys.stdout.write(" ")
	flush_stdout()
	#print(bcolors.HEADER + text + bcolors.ENDC)
	ccprint(text, bcolors.HEADER)
	flush_stdout()
	print("")
	for j in range(int(columns)):
		if (major):
			#sys.stdout.write(bcolors.HEADER + "*" + bcolors.ENDC)
			ccprint("*", bcolors.HEADER)
		else:
			#sys.stdout.write(bcolors.HEADER + "-" + bcolors.ENDC)
			ccprint("-", bcolors.HEADER)
	flush_stdout()
	print("\n")


# Custom prints
def cprint(text, s = "", linebreak = False):
	#sys.stdout.write(bcolors.OKBLUE + text + " :: " + bcolors.ENDC)
	ccprint(text + " :: ", bcolors.OKBLUE)
	flush_stdout()
	if (linebreak):
		print("")
		for i in range(int(columns)):
			#sys.stdout.write(bcolors.OKBLUE + "-" + bcolors.ENDC)
			ccprint("-", bcolors.OKBLUE)
		flush_stdout()
		print("")
	if (s != ""):
		print(s)
		print("")

