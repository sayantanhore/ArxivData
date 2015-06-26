import enchant
import re
import cprints as cp

def correct_spelling(text):
	checker = enchant.Dict("en_US")
	cp.cprint("Incorrect words", "", True)
	for word_at in re.finditer(r'\w+', text):
		word = word_at.group(0)

		if not word[0].isupper() and not checker.check(word):
			cp.cprint("Word", word)
			cp.cprint("Suggestions", checker.suggest(word))
def is_word(word):
	checker = enchant.Dict("en_US")
	if len(word) > 1:
		if word.isdigit():
			return False
		else:
			return checker.check(word)
	elif len(word) == 1:
		if word in ['a', 'A', 'I']:
			return True
		else:
			return False
	
def is_english(text, UK = False):
	if UK:
		checker = enchant.Dict("en_UK")
	else:
		checker = enchant.Dict("en_US")

	word_count = 0
	english_count = 0

	for word_at in re.finditer(r'\w+', text):
		word = word_at.group(0)
		word_count += 1
		if checker.check(word):
			english_count += 1
	if word_count > 0:
		if (float(english_count) / word_count) > 0.5:
			return True
		else:
			if UK:
				return False
			else:
				return is_english(text, UK = True)
	else:
		return False

#NOTE: checker.suggest("Helo") >>> ['He lo', 'Hello'...] spellchecker
