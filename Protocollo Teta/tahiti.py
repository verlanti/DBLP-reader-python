# -*- coding: utf-8 -*-

import xml.sax
import time
from xml.sax.handler import ContentHandler
import os
import os.path
import sys
from whoosh import index
from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED
from whoosh.query import Every
from whoosh.index import open_dir
from whoosh.writing import BufferedWriter
from whoosh.qparser import QueryParser

class  DumpHandler(ContentHandler):


    """

    Funzione di inizializzazione della classe DumpHandler che crea un dictionary,
    i contatori e le variabili per il caricamento.

    """

    def __init__(self):



        """ inizializzazione  delle variabili tag"""
       # self._tipologia = ''

        self._currentdata = ''
        self._key = ''
        self._title = ''
        self._author = ''
        self._date = ''
        self._publisher = ''
        self._journal = ''
        #self._booktitle = ''
        self._year = ''
        self._crossref = ''
        #self._editor,self._pages,self._address,self._volume,self._number,self._month,self._url,self._ee = ''
        #self._cdrom,self._cite,self._note,self._isbn,self._series,self._school,self._chapter,self._publnr = ''


        self.dict = {'key': None, 'title': None, 'author': None, 'date': None,  'journal': None,  'year': None, 'publisher': None,
                     'crossref': None,
                     }

        """contatori dei tag """
        self.countPhdthesis = 0
        self.countMastersthesis = 0
        self.countArticle = 0
        self.countBook = 0
        #self.countWww = 0
        self.countInproceedings = 0
        self.countIncollection = 0
        self.countProceedings = 0
        #self.countData = 0
        #self.countPerson = 0
       # self.countCross = 0
        #self.countInco_cross = 0
        #self.countInpro_cross = 0
        #self.countUniversale = 0



    """ modulo che parte con l'apertura dei tag"""
    def startElement(self, name, attrs):

        self._currentdata = name


        if name == 'phdthesis' or name == 'mastersthesis' or name == 'article' or \
           name == 'book'  or name == 'inproceedings' or name == 'incollection' or \
           name == 'proceedings' :

           self._key = attrs['key']
           self._date = attrs['mdate']

           self.dict['key'] = self._key
           self.dict['date'] = self._date


           if name == 'phdthesis'  :  self.countPhdthesis += 1
           if name == 'mastersthesis'  :  self.countMastersthesis += 1
           if name == 'article'  :  self.countArticle += 1
           if name == 'book'  :  self.countBook += 1
           #if name == 'www'  :  self.countWww += 1
           if name == 'inproceedings'  :  self.countInproceedings += 1
           if name == 'incollection'  :  self.countIncollection += 1
           if name == 'proceedings'  :  self.countProceedings += 1
           #if name == 'data'  :  self.countData += 1


        elif name == 'i' or name =='tt' or name == 'sup' or name == 'sub' or name == 'ref':
             if self.dict['title'] == None:
                     self.dict['title'] = self._title
                     self._title = ''
             else :
                self.dict['title']=self.dict['title']+self._title
                self._title = ''


    """controllo e gestione dei tag in chiusura"""
    def endElement(self, name) :


        """ per distanziare autori diversi"""
        space = " ; "

        if name == 'author':
            if self.dict['author'] == None:
                self.dict['author'] = self._author
                self._author = ''
            else:
                self.dict['author'] += space+self._author
                self._author = ''

        if name == 'title':
            if self.dict['title'] == None:
                self.dict['title'] = self._title
                self._title = ''
            else:
                self.dict['title'] += self._title
                self._title = ''

        if name == 'i' or name =='tt' or name == 'sup' or name == 'sub' or name == 'ref':
             if self.dict['title'] == None:
                     self.dict['title'] = self._title

             else :
                self.dict['title'] += self._title
             self._title = ''
             self._currentdata = 'title'

        if name == 'publisher': self.dict['publisher'] = self._publisher
        if name == 'journal': self.dict['journal'] = self._journal
        #if name == 'booktitle': self.dict['booktitle'] = self._booktitle
        if name == 'year': self.dict['year'] = self._year
        if name == 'crossref': self.dict['crossref'] = self._crossref

        if name == 'phdthesis' or name == 'mastersthesis' or name == 'article' or \
           name == 'incollection' or name == 'inproceedings' or  name == 'book' or \
           name == 'proceedings'  :



               if not self.dict['author']:
                        self.dict['author'] = 'unknown'
               if not self.dict['year']:
                        self.dict['year'] = 'unknown'
         #     if not self.dict['crossref']:
          #              self.dict['crossref'] = 'unknown'

              # if  name == 'data' :
               #        writer_data.add_document(tipologia=name, key=self.dict['key'], title=self.dict['title'], author=self.dict['author'], date=self.dict['date'], publisher=self.dict['publisher'], journal=self.dict['journal'], booktitle=self.dict['booktitle'], year=self.dict['year'], crossref=self.dict['crossref'])
               if  name == 'incollection' :
                       writer_inco.add_document( key=self.dict['key'], title=self.dict['title'], author=self.dict['author'], date=self.dict['date'],  journal=self.dict['journal'],  year=self.dict['year'], crossref=self.dict['crossref'])

               if name == 'proceedings':
                       writer_pro.add_document( key=self.dict['key'], title=self.dict['title'], author=self.dict['author'], date=self.dict['date'],  journal=self.dict['journal'],  year=self.dict['year'] ,publisher=self.dict['publisher'])
             #  if name == 'www':
            #            writer_www.add_document(tipologia=name, key=self.dict['key'], title=self.dict['title'], author=self.dict['author'], date=self.dict['date'], publisher=self.dict['publisher'], journal=self.dict['journal'], booktitle=self.dict['booktitle'], year=self.dict['year'], crossref=self.dict['crossref'])
               if name == 'article' :
                       writer_article.add_document( key=self.dict['key'], title=self.dict['title'], author=self.dict['author'], date=self.dict['date'],  journal=self.dict['journal'], year=self.dict['year'], crossref=self.dict['crossref'])
               if name == 'phdthesis':
                       writer_phd.add_document( key=self.dict['key'], title=self.dict['title'], author=self.dict['author'], date=self.dict['date'],  journal=self.dict['journal'],  year=self.dict['year'])
               if name == 'mastersthesis':
                       writer_master.add_document( key=self.dict['key'], title=self.dict['title'], author=self.dict['author'], date=self.dict['date'], journal=self.dict['journal'],  year=self.dict['year'])
               if name == 'book'  :
                       writer_book.add_document( key=self.dict['key'], title=self.dict['title'], author=self.dict['author'], date=self.dict['date'], journal=self.dict['journal'],  year=self.dict['year'], publisher=self.dict['publisher'])
               if name == 'inproceedings':

                       writer_Inpro.add_document( key=self.dict['key'], title=self.dict['title'], author=self.dict['author'], date=self.dict['date'], journal=self.dict['journal'],  year=self.dict['year'],  crossref=self.dict['crossref'])


               self.dict['key'] = None
               self.dict['author'] = None
               self.dict['date'] = None
               self.dict['title'] = None
               self.dict['publisher'] = None
               self.dict['journal'] = None
               #self.dict['booktitle'] = None
               self.dict['year'] = None
               self.dict['crossref'] = None
               self._currentdata = ""





    """ gestione del contenuto dei tag"""
    def characters(self, content):
        content=content.replace('\n','')
        if self._currentdata == 'author':
            self._author += content
        elif self._currentdata == 'title':
           self._title += content
        elif self._currentdata == 'publisher':
            self._publisher = content
        elif self._currentdata == 'journal':
            self._journal = content
       # elif self._currentdata == 'booktitle':
        #    self._booktitle = content
        elif self._currentdata == 'year':
            self._year = content
        elif self._currentdata == 'crossref':
            self._crossref = content
        elif self._currentdata == 'i' or self._currentdata =='tt' or self._currentdata == 'sup' or self._currentdata == 'sub' or self._currentdata == 'ref':
            self._title = content


    """fine documento, fa il commit e stampa i contatori"""
    def endDocument(self):
        print('---------------------------------------------------------------')
        print('Incollection :', self.countIncollection)
     #   print('Incollection con cross : ',self.countInco_cross)
        print('Proceedings : ', self.countProceedings)

        print('Book : ', self.countBook)
        print('Article : ', self.countArticle)
      #  print('Article con cross : ',self.countCross)
       # print('WWW : ', self.countWww)
        print('MasterT. : ', self.countMastersthesis)
        print('PhdT. : ', self.countPhdthesis)

        print('Inproceedings : ', self.countInproceedings)
    #    print('Inproceedings con cross : ',self.countInpro_cross)
        #print('Data : ', self.countData)
        print('\nTotal : ---->', self.countIncollection+self.countInproceedings+self.countBook\
              +self.countArticle+self.countMastersthesis+self.countPhdthesis\
              +self.countProceedings)

        writer_pro.commit()
        writer_book.commit()
        writer_phd.commit()
        writer_master.commit()
        #writer_www.commit()
       # writer_data.commit()
        writer_inco.commit()
   #     writer_inco_cross.commit()


        writer_article.commit()
  #      writer_article_cross.commit()

        writer_Inpro.commit()
 #       writer_Inpro_cross.commit()
    #    mydb.close()

def creazione(namefile) :


    if not os.path.exists(namefile):
        os.mkdir(namefile)

    ix = index.create_in(namefile, schema )
    return ix.writer(procs=2,multisegment=True)




start = time.time()

schema = Schema(
                title=TEXT(stored=True),
                key=TEXT(stored=True),
                date=KEYWORD(stored=True),
                author=TEXT(stored=True),
                publisher=TEXT(stored=True),
                journal=TEXT(stored=True),
              #  booktitle=TEXT(stored=True),
                year=TEXT(stored=True),
                crossref=TEXT(stored=True))




####### parsing and indexing


if not os.path.exists("index"):
    os.mkdir("index")


writer_book = creazione('index/book')

writer_pro = creazione('index/Proceedings')
writer_phd = creazione('index/phd')
writer_master = creazione('index/master')
#writer_www = creazione('index/www')
writer_inco = creazione('index/Incollection')
#writer_inco_cross = creazione('index/Incollection_cross')


writer_Inpro = creazione('index/Inproceedings')
#writer_Inpro_cross = creazione('index/Inproceedings_cross')


writer_article = creazione('index/article')
#writer_article_cross = creazione('index/article_cross')
#writer_data = creazione('index/data')


parser = xml.sax.make_parser()
handler = DumpHandler()
parser.setContentHandler(handler)
parser.setFeature(xml.sax.handler.feature_namespaces, 0)
parser.setFeature(xml.sax.handler.feature_external_ges, True)
parser.parse(str(sys.argv[1]))
end = time.time()
print('time:',end-start)
