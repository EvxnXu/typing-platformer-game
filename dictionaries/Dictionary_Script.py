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

def main():
	input_path = os.path.join(os.path.dirname(__file__), 'cleaned.txt')
	with open(input_path, 'r', encoding='utf-8') as f:
		words = [line.strip() for line in f if line.strip()]

	raw_scores = [score_word(word) for word in words]
	normed_scores = normalize_scores(raw_scores)

	# Pair words with scores
	word_score_pairs = list(zip(words, normed_scores))
	# Sort by score ascending
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

	print('Done. Created 20 sub-dictionaries.')

if __name__ == '__main__':
	main()
