# import modules & set up logging
import gensim
import logging
import os.path
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# get corpus 
from urllib.request import urlretrieve

# Downolad the text file if necessary.
if not os.path.isfile('corpus.txt'):
    urlretrieve('http://shilad.com/reddit-123/funny_large.txt', 'corpus.txt')

# Set up word2vec model
model_sentences = []
with open('corpus.txt', 'r') as f:
    for line in f:
        words = gensim.utils.tokenize(line, lowercase=True)
        model_sentences.append(list(words))

model = gensim.models.Word2Vec(model_sentences, workers=4, size=50, sg=1, min_count=5)

model.save('funny.model')