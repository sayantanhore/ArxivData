import sys
from localsettings import columns
# Custom console output functions
# ----------------------------------------------------------

# Flushing out standard output
def flush_stdout():
	sys.stdout.flush()

# Prints heading text
def head(text, major = False):
	for i in range(int(columns)):
		if (major):
			sys.stdout.write("*")
		else:
			sys.stdout.write("-")
	flush_stdout()
	spaces = (int(columns) - len(text))/2
	for i in range(spaces):
		sys.stdout.write(" ")
	flush_stdout()
	print(text)
	for j in range(int(columns)):
		if (major):
			sys.stdout.write("*")
		else:
			sys.stdout.write("-")
	flush_stdout()
	print("\n")


# Custom prints
def cprint(text, s = "", linebreak = False):
	sys.stdout.write(text + " :: ")
	flush_stdout()
	if (linebreak):
		print("")
		for i in range(int(columns)):
			sys.stdout.write("-")
		flush_stdout()
		print("")
	if (s != ""):
		print(s)
		print("")

