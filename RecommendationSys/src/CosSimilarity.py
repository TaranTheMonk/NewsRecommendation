##Integrated System
##Compute Similarity Module
##7th, Dec, 2016
##Developed by Xulang

import CosSimilarityAL as cal
import gensim
from gensim import similarities
import TextTransFormer as ttf
import csv
import pandas as pd

##Build tf to tf-idf
##Compute similarity and get output

##Wash text before refresh config

Raw_Path = '../src/TestDocs/news.tsv'
ttf.WashRawText(Raw_Path)

def getData(docs_address):
    #Import User Dataset
    #Specify dataset location
    corpus = cal.load_corpus(docs_address)
    docs = cal.corpus_docs(corpus)
    docs = cal.docs_stemmer(docs)

    ##stemmering and cleanning for reducing dimensions of vector space
    ##Use docs dictionary as the dictionary
    dictionary = gensim.corpora.Dictionary(docs)
    vecs = cal.docs_vecs(docs, dictionary)
    fileids = corpus.fileids()
    docs = {'vecs': vecs, 'dictionary': dictionary, 'file_ids': fileids, 'tf_idf': 0}
    return docs

def Computing():
    #tf to tf-idf
    docs['tf_idf'], docs['vecs'] = cal.tf_idf(docs['vecs'])
    #Build Index
    index = similarities.SparseMatrixSimilarity(docs['vecs'], len(docs['dictionary']))
    print('Computing Finished')
    return index

def enSavingConfig(index):
    ##Save index, tf-idf model and dictionary
    index.save("ConfigData/enTFIDF.idx")
    docs['tf_idf'].save("ConfigData/enTFIDF.mdl")
    docs['dictionary'].save("ConfigData/en.dic")
    pd.DataFrame(docs['file_ids']).to_csv('ConfigData/enTextIDs.csv' ,header = False, index = False)
    print('Saving Finished')
    return

address_docs = '../src/TestDocs/en/'
docs = getData(address_docs)
index = Computing()
enSavingConfig(index)