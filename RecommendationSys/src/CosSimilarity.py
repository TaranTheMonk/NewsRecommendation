##Integrated System
##Compute Similarity Module
##7th, Dec, 2016
##Developed by Xulang

import CosSimilarityAL as cal
import gensim
from gensim import similarities
from . import JsonTextTransFormer as ttf
import csv
import pandas as pd

##Build tf to tf-idf
##Compute similarity and get output

##Wash text before refresh config

def getData_en(docs_address):
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

def Computing_en(docs):
    #tf to tf-idf
    docs['tf_idf'], docs['vecs'] = cal.tf_idf(docs['vecs'])
    #Build Index
    index = similarities.SparseMatrixSimilarity(docs['vecs'], len(docs['dictionary']))
    print('Computing Finished')
    return index

def enSavingConfig_en(index, docs):
    ##Save index, tf-idf model and dictionary
    index.save("../Data/ConfigData/enTFIDF.idx")
    docs['tf_idf'].save("../Data/ConfigData/enTFIDF.mdl")
    docs['dictionary'].save("../Data/ConfigData/en.dic")
    pd.DataFrame(docs['file_ids']).to_csv('../Data/ConfigData/enTextIDs.csv' ,header = False, index = False)
    print('Saving Finished')
    return

def getData_cn(docs_address):
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

def Computing_cn(docs):
    #tf to tf-idf
    docs['tf_idf'], docs['vecs'] = cal.tf_idf(docs['vecs'])
    #Build Index
    index = similarities.SparseMatrixSimilarity(docs['vecs'], len(docs['dictionary']))
    print('Computing Finished')
    return index

def enSavingConfig_cn(index, docs):
    ##Save index, tf-idf model and dictionary
    index.save("../Data/ConfigData/cnTFIDF.idx")
    docs['tf_idf'].save("../Data/ConfigData/cnTFIDF.mdl")
    docs['dictionary'].save("../Data/ConfigData/cn.dic")
    pd.DataFrame(docs['file_ids']).to_csv('../Data/ConfigData/cnTextIDs.csv' ,header = False, index = False)
    print('Saving Finished')
    return

def main():
    Raw_Path = '../Data/TestDocs/news_all.json'
    ttf.WashRawText(Raw_Path)

    address_docs_en = '../Data/TestDocs/en/'
    docs_en = getData_en(address_docs_en)
    index_en = Computing_en(docs_en)
    enSavingConfig_en(index_en, docs_en)

    address_docs_cn = '../Data/TestDocs/cn/'
    docs_cn = getData_cn(address_docs_cn)
    index_cn = Computing_cn(docs_cn)
    enSavingConfig_cn(index_cn, docs_cn)

main()
