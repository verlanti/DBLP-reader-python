from tkinter.ttk import *
from tkinter import *
import tkHyperlinkManager
import query
import frame
import functools
import time




class Venue_union_layout(Frame):


    def __init__(self,note,window,result):
        Frame.__init__(self,note)

        self.window = window
        self.note = note
        self.result = result
        self.T = Text(self,height = 15)
        self.T.pack()
        self.c_start = 0
        self.c_end = 10

        for i in self.result[self.c_start:self.c_end]:

            if 'title' in i:
                self.T.insert(INSERT, 'title: \t'+i['title']+'\n')
            if 'author' in i:
                self.T.insert(INSERT, 'author: \t'+i['author']+'\n')
            if 'publisher' in i:
                self.T.insert(INSERT, 'publisher: \t'+i['publisher']+'\n')
            if 'year' in i:
                self.T.insert(INSERT, 'year: \t'+i['year']+'\n')
            self.T.insert(INSERT, i['key']+'\n')

        self.T.insert(END,"\n\n")

        self.T.config(state=DISABLED)

        Button(self, text="Next", command=lambda : self.next(self.T,True)).place(x = 300 , y = 240)
        Button(self, text='Quit', command= self.destroy).place(x = 250 , y = 240)
        Button(self, text="Past", command=lambda : self.next(self.T,False)).place(x = 200 , y = 240)

    def next(self,T,next):

        self.T.config(state=NORMAL)
        self.T.delete(1.0,END)

        if next :
            if self.c_end <= len(self.result):
                self.c_start += 10
                self.c_end += 10
        else:
            if self.c_start > 0:
                self.c_start -= 10
                self.c_end -= 10
            else:
                    self.c_start = 0

        for i in self.result[self.c_start:self.c_end]:

            if 'title' in i:
                self.T.insert(INSERT, 'title: \t'+i['title']+'\n')
            if 'author' in i:
                self.T.insert(INSERT, 'author: \t'+i['author']+'\n')
            if 'publisher' in i:
                self.T.insert(INSERT, 'publisher: \t'+i['publisher']+'\n')
            if 'year' in i:
                self.T.insert(INSERT, 'year: \t'+i['year']+'\n')
            self.T.insert(INSERT, i['key']+'\n')



        self.T.insert(END,"\n\n")

        self.T.config(state=DISABLED)



class Risultato_layout(Frame):


   def __init__(self,note,window,result):
        Frame.__init__(self,note)

        self.window = window
        self.note = note
        self.result = result

        self.T = Text(self,height = 15)
        self.T.pack()
        self.c_start = 0
        self.c_end = 10

        hyperlink = tkHyperlinkManager.HyperlinkManager(self.T)
        for i in self.result[self.c_start:self.c_end]:


            if 'title' in i:
                self.T.insert(INSERT, 'title: \t'+i['title']+'\n')
            if 'author' in i:
                self.T.insert(INSERT, 'author: \t'+i['author']+'\n')
            if 'publisher' in i:
                    self.T.insert(INSERT, 'publisher: \t'+i['publisher']+'\n')
            if 'date' in i:
                    self.T.insert(INSERT, 'date: \t'+i['date']+'\n')
            if 'journal' in i:
                    self.T.insert(INSERT, 'journal: \t'+i['journal']+'\n')
            if 'crossref' in i and self.control_link(self.result,i):
                self.T.insert(INSERT,i['crossref'], hyperlink.add(functools.partial(self.click, result=self.result,crossref=i['crossref']))) #[] => result
            self.T.insert(END,"\n\n")

        self.T.config(state=DISABLED)

        Button(self, text="Next", command=lambda : self.next(self.T,True)).place(x = 300 , y = 240)
        Button(self, text='Quit', command= window.destroy).place(x = 250 , y = 240)
        Button(self, text="Past", command=lambda : self.next(self.T,False)).place(x = 200 , y = 240)


        self.L = Label(self, text="Totale risultati: "+str(len(self.result)))
        self.L.config(font=('times', 15, 'normal'))
        self.L.place(x=400,y=245)

   def control_link(self,result,element):

       for r in result:
           if element['crossref'] == r['key']:
               return True
       return False


   def next(self,T,next):

        self.T.config(state=NORMAL)
        self.T.delete(1.0,END)

        if next :
            if self.c_end <= len(self.result):
                self.c_start += 10
                self.c_end += 10
        else:
            if self.c_start > 0:
                 self.c_start -= 10
                 self.c_end -= 10
            else:
                 self.c_start = 0

        hyperlink = tkHyperlinkManager.HyperlinkManager(self.T)
        for i in self.result[self.c_start:self.c_end]:
            if 'title' in i:
                self.T.insert(INSERT, 'title: \t'+i['title']+'\n')
            if 'author' in i:
                self.T.insert(INSERT, 'author: \t'+i['author']+'\n')
            if 'publisher' in i:
                self.T.insert(INSERT, 'publisher: \t'+i['publisher']+'\n')
            if 'date' in i:
                self.T.insert(INSERT, 'date: \t'+i['date']+'\n')
            if 'journal' in i:
                self.T.insert(INSERT, 'journal: \t'+i['journal']+'\n')

            if 'crossref' in i and self.control_link(self.result,i):
                self.T.insert(INSERT,i['crossref'],hyperlink.add(functools.partial(self.click, result=self.result,crossref=i['crossref'])))
            self.T.insert(END,"\n\n")

        self.T.config(state=DISABLED)


   def click(self,result,crossref):
        for r in result:
            if crossref == r['key']:
                result = [r]



        tab = Venue_union_layout(self.note,self.window,result)
        self.note.add(tab,text="Risultato Venue union")




class Union_layout(Frame):
   def __init__(self,*args,**kwargs):
      Frame.__init__(self,*args,**kwargs)


      self.rank_text = StringVar()
      self.rank_text.set('BM25F')
      rank_but = Button(self, textvariable=self.rank_text, command=lambda : self.change(self.rank_text)).place(x = 20 , y = 230)

      # Titolo Publication
      self.labelfont = ('times', 20, 'bold')
      self.pubLabel = Label(self, text="Publications")
      self.pubLabel.config(font=self.labelfont)
      self.pubLabel.place(x=240,y=5)
      # Titolo Venue
      self.venueLabel = Label(self, text="Venue")
      self.venueLabel.config(font=self.labelfont)
      self.venueLabel.place(x=250,y=130)

      self.height_checkbox_pub = 40
      self.height_entry_pub = 80

      self.height_entry_venue = 190
      self.height_checkbox_venue = 160

      # Check button both
      self.chk_state_both = [IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar()]
      # chk state pub
      Checkbutton(self, text = 'article', variable = self.chk_state_both [0]).place(x = 20 , y = self.height_checkbox_pub)
      Checkbutton(self, text = 'phd', variable = self.chk_state_both[1]).place(x = 100  , y = self.height_checkbox_pub)
      Checkbutton(self, text = 'master', variable = self.chk_state_both[2]).place(x = 160 , y = self.height_checkbox_pub)
      Checkbutton(self, text = 'incollection', variable = self.chk_state_both[3]).place(x = 240 , y = self.height_checkbox_pub)
      Checkbutton(self, text = 'Inproceedings', variable = self.chk_state_both[4]).place(x =  440, y = self.height_checkbox_pub)
      Checkbutton(self, text = 'publication', variable = self.chk_state_both[5], command = self.change_state).place(x = 340, y = self.height_checkbox_pub)
      # chk state venue
      Checkbutton(self, text = 'book', variable = self.chk_state_both[6]).place(x= 160,y=self.height_checkbox_venue)
      Checkbutton(self, text = 'Proceedings', variable = self.chk_state_both[7]).place(x= 340,y=self.height_checkbox_venue)



      #Pub
      self.title = StringVar()
      self.titleString=StringVar()
      self.titleString.set("Title: ")

      self.titleText=Label(self, textvariable=self.titleString)
      self.titleText.place(x = 10 , y = self.height_entry_pub  )

      self.titleEntry=Entry(self,width=20,textvariable=self.title)
      self.titleEntry.place(x = 50 , y = self.height_entry_pub  )
      #titleText.pack(side="left",padx=10)
      #titleEntry.pack(side="left")

      self.year = IntVar()
      self.yearString=StringVar()
      self.yearString.set("Year: ")

      self.yearText=Label(self, textvariable=self.yearString)
      self.yearText.place(x = 250 , y = self.height_entry_pub )

      self.yearEntry=Entry(self,width=5,textvariable=self.year)
      self.yearEntry.place(x = 290 , y = self.height_entry_pub )


      self.author = StringVar()
      self.authorString=StringVar()
      self.authorString.set("Author: ")

      self.authorText=Label(self, textvariable=self.authorString)
      self.authorText.place(x = 360 , y = self.height_entry_pub )


      self.authorEntry=Entry(self,width=20,textvariable=self.author)
      self.authorEntry.place(x = 420 , y = self.height_entry_pub )

      #Venue

      self.title_venue = StringVar()
      self.title_venueString=StringVar()
      self.title_venueString.set("Title: ")

      self.title_venueText=Label(self, textvariable=self.titleString)
      self.title_venueText.place(x = 80 , y = self.height_entry_venue )

      self.title_venueEntry=Entry(self,width=20,textvariable = self.title_venue)
      self.title_venueEntry.place(x = 120 , y = self.height_entry_venue )

      self.publisher = StringVar()
      self.publisherString=StringVar()
      self.publisherString.set("Publisher: ")

      self.publisherText=Label(self, textvariable=self.publisherString)
      self.publisherText.place(x = 305 , y = self.height_entry_venue )


      self.publisherEntry=Entry(self,width=20, textvariable = self.publisher)
      self.publisherEntry.place(x = 375 , y = self.height_entry_venue )


      Button(self, text='Quit', command=self.quit).place(x = 300 , y = 230)
      Button(self, text='Show', command=lambda: self.get(self.title,self.year,self.author,self.title_venue
      ,self.publisher,self.chk_state_both,self.rank_text)).place(x = 200 , y = 230)


   def change_state(self):
         if self.chk_state_both[5].get() == 1:
             for i in self.chk_state_both[0:5]:
                 i.set(1)
         else:
             for i in self.chk_state_both[0:5]:
                 i.set(0)


   def concatenate(self,result_pub,result_venue):
       start=time.time()


       matches_pub = []
       matches_venue = []
       dict_pub_indexed = {}
       dict_venue_indexed = {}



       for item in result_venue:
            dict_venue_indexed[item['key']] = item

       for item in result_pub:
           if 'crossref' in item:
               if item['crossref'] in dict_venue_indexed:
                   item.score += dict_venue_indexed[item['crossref']].score
           matches_pub.append(item)

################################################################################
       for item in result_pub:
             if 'crossref' in item:
                 dict_pub_indexed[item['crossref']] = item


       for item in result_venue:
             if item['key'] in dict_pub_indexed:

                item.score += dict_pub_indexed[item['key']].score/3
             matches_venue.append(item)


       end=time.time()


       return matches_pub,matches_venue




   def change (self,rank_text):

        if rank_text.get() == 'BM25F':
            rank_text.set('PL2')
        else :
            rank_text.set('BM25F')



   def get(self,title_pub,year,author,title_venue,publisher,chk_state_both,rank_text):
        
         if all(x.get() == 0 for x in chk_state_both):
            return

         try:
             print("title: ",title_pub.get(),"year: ", year.get() ,"publisher: ",publisher.get()," title_venue: ",title_venue.get(),
             "publisher: ",publisher.get())
         except Exception as Ex:
             pass
                #messagebox.showerror("Error", "Type is not valid")
         result_pub = []
         result_venue = []
         results_union_pub = []
         results_union_venue = []
         content = ""
         content_venue = ""


         if title_pub.get() != "" :
            content +=" title:"+title_pub.get()


         try:
             if  year.get() != 0 :
                 content += " year:"+str(year.get())
         except Exception:
             year.set(0)

         if  author.get() != "" :
            content += " author:"+author.get()


         if title_venue.get() != "" :
           content_venue +=" title:"+title_venue.get()

         if publisher.get() != "" :
           content_venue += " publisher:"+publisher.get()


         if chk_state_both[0].get() == 1: #print("Hai selezionato article")
                    result_pub.extend(query.Query.ricerca('index/article',content,rank_text))
                    #result_pub.extend(query.Query.ricerca('index/article_cross',content,rank_text))
         if chk_state_both[1].get() == 1: #print("Hai selezionato phd")
                    result_pub.extend(query.Query.ricerca('index/phd',content,rank_text))
         if chk_state_both[2].get() == 1: #print("Hai selezionato master")
                    result_pub.extend(query.Query.ricerca('index/master',content,rank_text))
         if chk_state_both[3].get() == 1: #print("Hai selezionato incollection")
                    result_pub.extend(query.Query.ricerca('index/Incollection',content,rank_text))
                    #result_pub.extend(query.Query.ricerca('index/Incollection_cross',content,rank_text))
         if chk_state_both[4].get() == 1: #print("Hai selezionato proceedings")
                    result_pub.extend(query.Query.ricerca('index/Inproceedings',content,rank_text))
                    #result_pub.extend(query.Query.ricerca('index/Inproceedings_cross',content,rank_text))
         if chk_state_both[6].get() == 1: result_venue.extend(query.Query.ricerca('index/book',content_venue,rank_text))#print("Hai selezionato book")
         if chk_state_both[7].get() == 1: result_venue.extend(query.Query.ricerca('index/Proceedings',content_venue,rank_text))#print("Hai selezionato inproceedings")
         
         results_union_pub,results_union_venue = self.concatenate(result_pub,result_venue)

         union = results_union_pub
         union.extend(results_union_venue)
         #union = sorted(results_union_pub,key = lambda sorting: .score)

         union = sorted(union,key = lambda sorting: sorting.score, reverse = True)

         #finestra = Result_Frame(results_union_pub,results_union_venue,True)
         print("Lunghezza risultati: ",len(union))
         finestra = frame.Result_Frame(union)
         #finestra2 = Result_Frame(results_union_venue)
