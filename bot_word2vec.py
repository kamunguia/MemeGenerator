import gensim
import logging
import os.path
import csv

def load_memetags(fname):
	memetags = {}
	with open(fname, 'r') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		for row in reader:
			name = row[0]
			tags = [t for t in row[1:] if t in model.wv.vocab]
			memetags[name] = tags
	return memetags

def get_distance(sentence, tags, mode='max'):
	if mode == 'max':
		max_dist = -1
		for word in sentence:
		    for tag in tags:
		        dist = model.wv.similarity(word, tag)
		        if dist > max_dist:
		        	max_dist = dist
		return max_dist
	elif mode == 'avg':
	    avg_dist = 0
	    for word in sentence:
	        for tag in tags:
	            avg_dist += model.wv.similarity(word, tag)
	    return avg_dist/(len(sentence)*len(tags))

def get_closest_meme(sentence, memes):
	max_meme = ''
	max_dist = -1
	for meme in memes.keys():
		dist = get_distance(sentence, memes[meme])
		if dist > max_dist:
			max_dist = dist
			max_meme = meme
	return max_meme

model = gensim.models.Word2Vec.load('data/funny.model')
memetags_positive = load_memetags('images/positive/postive.csv')
memetags_neutral = load_memetags('images/neutral/neutral.csv')
memetags_negative = load_memetags('images/negative/sad.csv')

sentence = ['i', 'love', 'puppies', 'and', 'swimming']

print(get_closest_meme(sentence,memetags_positive))
print(get_closest_meme(sentence,memetags_neutral))
print(get_closest_meme(sentence,memetags_negative))
