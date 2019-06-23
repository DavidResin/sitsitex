import random

# Get all valid combinations between a given song and a list of other songs
def combinations(elem, others, limit):
	length, segs = elem
	ret = []

	for o_length, o_segs in others:
		# Can't have songs in common
		if set(segs.keys()) & set(o_segs.keys()):
			continue

		# Combination has to fit the page
		if length + o_length > limit:
			continue

		# Save combination
		ret += [(length + o_length, {**segs, **o_segs})]

	return ret

def process(songs, limit):
	curr_batches = [([], 0, list(songs.keys()))]
	next_batches = []
	finals = []

	while curr_batches:
		for choice, length, rem in curr_batches:
			# End of the list
			if len(rem) == 0:
				finals += [(choice, length)]
				continue
			
			# Case where song not chosen
			next_batches += [(choice, length, rem[1:])]

			# Case where song chosen and it fits the page
			if length + songs[rem[0]] <= limit:
				next_batches += [(choice + [rem[0]], length + songs[rem[0]], rem[1:])]

		curr_batches = next_batches
		next_batches = []

	return finals

def combinations(pages, n_songs):
	curr_batches = [([], [], range(len(pages)))]
	next_batches = []
	finals = []

	while curr_batches:
		for choice, scores, rem in curr_batches:
			# End of the list, keep only if all songs are in
			if len(rem) == 0:
				if len(set([item for sub in choice for item in pages[sub][0]])) == n_songs:
					finals += [(choice, scores)]

				continue

			# Case where page not chosen
			next_batches += [(choice, scores, rem[1:])]

			# Case where page is chosen and it doesn't double insert a song
			if not set(pages[rem[0]][0]) & set([item for sub in choice for item in pages[sub][0]]):
				next_batches += [(choice + [rem[0]], scores + [pages[rem[0]][1]], rem[1:])]

			curr_batches = next_batches
			next_batches = []

	return finals

low, high = 20, 100
n_songs = 50
length = 120

songs = [random.randint(low, high) for i in range(n_songs)]
ref = dict(zip(range(n_songs), songs))

# Build tree with dynamic programming to remember what has been done already