#By WAN Xulang
import preparation as pre
import gensim
import re
import nltk
import sklearn
import numpy as np
import time, random
from nltk.classify import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB
from nltk import FreqDist
from gensim import similarities
import computing as cp

##Build tf to tf-idf
##User corpus
##User center
##Compute similarity and get output

###Flag: user - 0, docs' house - 1
def getData(user_address, docs_address):
    #Import User Dataset
    #Specify dataset location
    corpus_0 = pre.load_corpus(user_address)
    corpus_1 = pre.load_corpus(docs_address)
    docs_0 = pre.corpus_docs(corpus_0)
    docs_0 = pre.docs_stemmer(docs_0)
    docs_1 = pre.corpus_docs(corpus_1)
    docs_1 = pre.docs_stemmer(docs_1)

    ##stemmering and cleanning for reducing dimensions of vector space
    ##Use docs dictionary as the dictionary
    dictionary_0 = gensim.corpora.Dictionary(docs_0)
    dictionary_1 = gensim.corpora.Dictionary(docs_1)
    vecs_0 = pre.docs_vecs(docs_0, dictionary_1)
    vecs_1 = pre.docs_vecs(docs_1, dictionary_1)
    fileids_0 = corpus_0.fileids()
    fileids_1 = corpus_1.fileids()
    user = {'vecs': vecs_0, 'dictionary': dictionary_0, 'file_ids': fileids_0, 'tf_idf': 0}
    docs = {'vecs': vecs_1, 'dictionary': dictionary_1, 'file_ids': fileids_1, 'tf_idf': 0}
    return user, docs

address_user = '../CosSimilarity/User/en'
address_docs = '../CosSimilarity/TestDocs/en'
user, docs = getData(address_user, address_docs)

#user['tf_idf'], user['vecs'] = pre.tf_idf(user['vecs'])
docs['tf_idf'], docs['vecs'] = pre.tf_idf(docs['vecs'])

# for i in range(len(docs['vecs'])):
#     docs['vecs'][i] = user['tf_idf'][docs['vecs'][i]]
for i in range(len(user['vecs'])):
    user['vecs'][i] = docs['tf_idf'][user['vecs'][i]]

#Locate target docs
index = similarities.SparseMatrixSimilarity(docs['vecs'], len(docs['dictionary']))
##Load the index to compute
index.save("allTFIDF.idx")
sims = []
##Sum the scores together!
print('Index Finished')

for i in range(len(docs['vecs'])):
    sims.append([index[docs['vecs'][i]].max(), index[docs['vecs'][i]].argmax(), docs['file_ids'][i]])


##idf based on all docs
##Check top ones, whether in same category
sims = cp.merge_sort(sims)
output = []

C = 10
i = 0
while len(output) < C:
    if not(sims[i][2] in user['file_ids']):
        output.append(sims[i])
    i += 1
print(output)

