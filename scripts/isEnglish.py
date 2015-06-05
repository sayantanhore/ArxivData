import enchant

def is_english(text):
	checker = enchant.Dict("en_US")
	word_count = 0
	english_count = 0
	for word in text:
		word_count += 1
		if checker.check(word):
			english_count += 1
	if english_count / word_count > 0.5:
		return True
	else:
		return False

#NOTE: checker.suggest("Helo") >>> ['He lo', 'Hello'...] spellchecker
