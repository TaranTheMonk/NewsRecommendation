import nltk
import re
from nltk.corpus import stopwords
from nltk.stem.porter import *
from gensim import corpora,models,similarities,utils
import jieba
import jieba.posseg as pseg

#useless_punct = re.compile('nbsp|a-zA-Z]{1,1}|\\\|\s|\?|\？|\。|\.|\(|\)|\（|\）|\/|\>|\<|\:|\：|\&|\;|\#|\_|\!|\,')

stop_list = nltk.corpus.stopwords.words('english')
stop_list = stop_list #+ ['IMG', 'nbsp', '我们', '你们', '他们'， '']

def load_corpus( dir ):
    # dir is a directory with plain text files to load.
    corpus = nltk.corpus.PlaintextCorpusReader(dir, '.*')
    return corpus

def corpus_docs ( corpus ):
    # corpus is an object returned by load_corpus that represents a corpus.
    fids = [w for w in corpus.fileids() if w != '.DS_Store']
    docs1 = []
    N = 1
    #N is the weight for title
    for fid in fids:
        doc_raw = corpus.raw(fid) + '' + (fid[:len(fid) - 4] * N)
        doc = nltk.word_tokenize(doc_raw)
        docs1.append(doc)
    docs2 = [[w.lower() for w in doc] for doc in docs1]
    docs3 = [[w for w in doc if re.match('^[a-z]+$', w)] for doc in docs2]
    docs4 = [[w for w in doc if w not in stop_list] for doc in docs3]
    return docs4

def corpus_docs_cn ( corpus ):
    ##CN Stop words list!
    ##Remove useless symbols
    # corpus is an object returned by load_corpus that represents a corpus.
    fids = [w for w in corpus.fileids() if w != '.DS_Store']
    docs1 = []
    N = 1
    # N is the weight for title
    for fid in fids:
        doc_raw = corpus.raw(fid)
        word_list = jieba.lcut((fid[:len(fid) - 4] * N) + doc_raw, cut_all=False)
        docs1.append(word_list)
    docs2 = [[w.lower() for w in doc] for doc in docs1]
    docs3 = [[w for w in doc if not (re.match('^[a-z]+$', w))] for doc in docs2]
    docs4 = [[w for w in doc if not(len(w) == 1)] for doc in docs3]
    docs5 = [[w for w in doc if w not in stop_list] for doc in docs4]
    return docs5

def docs_vecs ( docs , dictionary ):
    vecs = [dictionary.doc2bow(doc) for doc in docs]
    return vecs

def docs_stemmer ( docs ):
    stemmer = PorterStemmer()
    docs5 = [[stemmer.stem(w) for w in doc] for doc in docs]
    return docs5

def tf_idf(corpus):
    tf_idf = models.TfidfModel(corpus)
    tf_idf_vecs = [tf_idf[c] for c in corpus]
    return tf_idf, tf_idf_vecs
