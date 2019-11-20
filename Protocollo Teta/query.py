import time
from whoosh import  scoring , qparser
from whoosh.query import Every
from whoosh.index import open_dir
from whoosh.qparser import QueryParser



class Query():

    time_ricerca = None
    def __init__(self):
        pass

    def ricerca (filename,content,rank_text):
        start_ricerca= time.time()
        passo = []

        ix = open_dir(filename)
        #searcher = ix.searcher()
        #print(list(searcher.lexicon("title"))) Fa una lista di tutti gli index term trovati

        if content == "" :
             results = ix.searcher().search(Every('key'),limit=None)

        elif rank_text.get() == 'BM25F' :

            results = ix.searcher(weighting=scoring.BM25F()).search(QueryParser('content', schema=ix.schema,group=qparser.OrGroup).parse(content),limit=None)

        elif rank_text.get() == 'PL2':

            results = ix.searcher(weighting=scoring.PL2()).search(QueryParser('content', schema=ix.schema,group=qparser.OrGroup).parse(content),limit=None)

        start= time.time()
        for i in results:
            passo.append(i)
        end= time.time()


        print('tempo passo : ', end-start)
        end_ricerca=time.time()
        Query.time_ricerca=(end_ricerca-start_ricerca)
        print("tempo ricerca",Query.time_ricerca)

        return results
        #self.c_start += 10
         #if self.c_end  += 10
         #self.c_end  += 10
        # if self.c_start < 0:
        #     self.c_start = 0
