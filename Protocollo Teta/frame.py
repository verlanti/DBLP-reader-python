from tkinter.ttk import *
from tkinter import *
from tkinter import messagebox
import layout


class Master(Tk):

    def __init__(self,*args,**kwargs):
       Tk.__init__(self,*args,**kwargs)
       self.title("ARGO")
       self.geometry("600x300")
       self.resizable(width=False, height=False)
       self.notebook = Notebook(self)
       self.notebook.pack(expand=1, fill='both')
       self.add_tab()


    def add_tab(self):
        self.tab3 = layout.Union_layout(self.notebook)
        self.notebook.add(self.tab3,text="Union")








class Result_Frame(Tk):

    def __init__(self,union):
       Tk.__init__(self)


       self.union = union
       self.title("Results")
       self.geometry("600x300")
       self.resizable(width=False, height=False)
       self.note = Notebook(self)
       self.note.pack(expand=1, fill='both')

       self.add_tab()




    def add_tab(self):

         self.tab = layout.Risultato_layout(self.note,self,self.union)
         self.note.add(self.tab,text="Risultato")
