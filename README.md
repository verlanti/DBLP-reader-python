# DBLP-reader-python
Example of DBLP reader in python

Progetto creato da Palazzi Luca  e Verlanti Emanuele 

Protocollo Teta e' un sistema full-text search che consente ad un
utente di effettuare ricerche avanzate nella bibliografia di
DBLP e che mostri i risultati ordinati in base a vari modelli
di ranking.

Protocollo Teta mette a disposizione due file principali:
	tahiti.py e' in grado di eseguire il parsing di un file xml e creare un oggetto indicizzato in grado di memorizzare i dati bibliografici
 			di uno dei file di DBLP.

	argo.py e' in grado di far eseguire query all'utente

In Protocollo Teta sono presenti due oggetti indicizzati (index directory):
	index : indice che si riferisce al dump del 2015-03-02

dblp_prova.xml contiene un campione di 10MB di un dump utile per provare il parser tahiti.py

Installazione
-------------

python3 

Librerie esterne da installare 

Tkinter 

sudo apt-get install python3-tk 

Sax 

sudo apt-get install python-lxml

Whoosh 

pip3 install Whoosh 


Quick start
-----------

Tahiti 

0.  python3 tahiti.py file_da_leggere.xml 

	Attenzione!!! tahiti.py sovrascrive ogni directory chiamata index

Argo

0. python3 argo.py
        
	Attenzione!!! argo.py prende come indice per la ricerca la directory index, quindi rinominare la cartella che si vuole
			      utilizzare.



