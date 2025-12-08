# Dictionary_Script.py
# Parses cleaned.txt, assigns difficulty scores to words, and splits into 20 sub-dictionaries.

import os
import math

# QWERTY hand/finger mapping (simplified)
LEFT_HAND = set('qwertasdfgzxcvb')
RIGHT_HAND = set('yuiophjklnm')
HOME_ROW = set('asdfghjkl')
PINKY_RING = set('qazplm')

# Common English digraphs (for bonus)
COMMON_DIGRAPHS = set([
	'th','he','in','er','an','re','on','at','en','nd','ti','es','or','te','of','ed','is','it','al','ar','st','to','nt','ng','se','ha','as','ou','io','le','ve','co','me','de','hi','ri','ro','ic','ne','ea','ra','ce','li','ch','ll','be','ma','si','om','ur'
])

def pair_difficulty(a, b):
	a, b = a.lower(), b.lower()
	if a == b:
		return 5  # Same finger twice
	pair = a + b
	if pair in COMMON_DIGRAPHS:
		return -2
	if (a in LEFT_HAND and b in RIGHT_HAND) or (a in RIGHT_HAND and b in LEFT_HAND):
		return 2  # Alternating hands
	if a not in HOME_ROW and b not in HOME_ROW:
		return 3  # Both off home row
	if a in PINKY_RING or b in PINKY_RING:
		return 4  # Pinky or ring involved
	if pair in {'zx','qp','qz','xq','pq','bq','jq','zj','qj','vj','xv','qv'}:
		return 6  # Awkward pairs
	return 0  # Default

def score_word(word):
	base = 10 * len(word)
	pair_score = 0
	for i in range(len(word)-1):
		pair_score += pair_difficulty(word[i], word[i+1])
	return base + pair_score

def normalize_scores(raw_scores, min_score=100, max_score=5000):
	raw_min = min(raw_scores)
	raw_max = max(raw_scores)
	normed = []
	for s in raw_scores:
		if raw_max == raw_min:
			val = min_score
		else:
			val = min_score + ((s - raw_min) / (raw_max - raw_min)) * (max_score - min_score)
		val = int(round(val / 10.0) * 10)
		normed.append(val)
	return normed

# --- New: dictionary cleaning utilities ---
def load_bad_words(path=None):
	"""
	Load bad words from a 'bad_words.txt' file located next to this script.
	Each line in the file should be a single word (no score). Lines starting with '#' are ignored.
	If no file is found, returns an empty set (no automatic removals).
	"""
	if path is None:
		path = os.path.join(os.path.dirname(__file__), 'bad_words.txt')
	if not os.path.isfile(path):
		print(f"[Dictionary_Script] No bad_words file found at: {path} (skipping automatic removals)")
		return set()
	with open(path, 'r', encoding='utf-8') as fh:
		words = {line.strip().lower() for line in fh if line.strip() and not line.strip().startswith('#')}
	return words


def clean_subdict_files(bad_words, make_backup=True):
	"""
	Remove lines from subdict_*.txt files whose word (left of '|') matches or contains any entry
	in bad_words. Matching is case-insensitive and strips whitespace. Optionally makes a .bak backup.
	"""
	if not bad_words:
		return
	dirpath = os.path.dirname(__file__)
	for filename in os.listdir(dirpath):
		if not (filename.startswith('subdict_') and filename.endswith('.txt')):
			continue
		path = os.path.join(dirpath, filename)
		with open(path, 'r', encoding='utf-8') as fh:
			lines = fh.readlines()
		cleaned = []
		removed = 0
		for ln in lines:
			ln_strip = ln.strip()
			if not ln_strip:
				continue
			parts = ln_strip.split('|', 1)
			word = parts[0].strip().lower()
			# remove if exact match or contains a bad token as a substring
			if any(b in word or word in b for b in bad_words):
				removed += 1
			else:
				cleaned.append(ln_strip + '\n')
		if removed:
			if make_backup:
				bak = path + '.bak'
				if not os.path.exists(bak):
					with open(bak, 'w', encoding='utf-8') as bf:
						bf.writelines(lines)
			with open(path, 'w', encoding='utf-8') as fh:
				fh.writelines(cleaned)
			print(f"[Dictionary_Script] Cleaned {removed} entries from {filename}")

# --- End new utilities ---

def main():
	# Try to load a bad_words.txt (create this file next to Dictionary_Script.py with one word per line)
	bad_words = load_bad_words()
	# If any bad words were provided, clean subdict files and exit without regenerating files
	if bad_words:
		clean_subdict_files(bad_words)
		print('[Dictionary_Script] Completed cleaning subdict files. Exiting without regenerating subdict files.')
		return

	input_path = os.path.join(os.path.dirname(__file__), 'cleaned.txt')
	with open(input_path, 'r', encoding='utf-8') as f:
		words = [line.strip() for line in f if line.strip()]

	raw_scores = [score_word(word) for word in words]
	normed_scores = normalize_scores(raw_scores)

	word_score_pairs = list(zip(words, normed_scores))
	word_score_pairs.sort(key=lambda x: x[1])

	# Split into 20 sub-dictionaries
	n = len(word_score_pairs)
	chunk_size = math.ceil(n / 20)
	for i in range(20):
		chunk = word_score_pairs[i*chunk_size:(i+1)*chunk_size]
		out_path = os.path.join(os.path.dirname(__file__), f'subdict_{i+1:02d}.txt')
		with open(out_path, 'w', encoding='utf-8') as out:
			for word, score in chunk:
				out.write(f'{word}|{score}\n')


if __name__ == '__main__':
	main()
