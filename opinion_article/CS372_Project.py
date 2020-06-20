# Running this code takes about 8 mins in my computer.
# Please let this code run until the end, it just takes long. There is no infinite loop T.T

import nltk
from nltk.corpus import PlaintextCorpusReader

forward = PlaintextCorpusReader('./forward', '.*')
print(forward.fileids())
print(forward.words('forward0.txt')[:100])

