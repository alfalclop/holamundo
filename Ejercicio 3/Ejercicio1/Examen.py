# -*- coding: utf-8 -*-

import Tkinter
import urllib2
import sqlite3
import tkMessageBox
import re
from pattern.server import HTTPError
from urllib2 import URLError
from bs4 import BeautifulSoup

root = Tkinter.Tk()
root.geometry("500x500")


def conexionPagina(url):
    try:
        f= urllib2.urlopen(url)
        texto = f.read()

        f.close()
        soup = BeautifulSoup(texto)
        lista = soup.find_all('a', "LinkIndice") 
        
        listaDevolver= []
                
        for link in lista:
            listaDevolver.append(link.get('href'))
            first_link = soup.find("a","LinkIndice", text = link.get('href'))
            print first_link.find_previous("font","TituloIndice")
            
        return soup
    except HTTPError, e:
        print "ocurrio un error"
        print e.code
    except URLError, e:
        print "Ocurrio un error"
        print e.reason

def almacenar():
    
    lista = conexionPagina("http://www.sevillaguia.com/sevillaguia/agendacultural/agendacultural.asp")
   
        
    conn = sqlite3.connect('test.db')
    print "Base de datos abierta correctamente";
    
   
    conn.execute('''DROP TABLE IF EXISTS ENLACES''')
    conn.execute('''CREATE TABLE ENLACES
            (LINK TEXT PRIMARY KEY     NOT NULL,
             CATEGORIA           TEXT    NOT NULL);''')
    
    print "Tabla creada correctamente";
    
    conn.text_factory = str
    
    for e in lista:
        offer = None
        if len(e) == 6 :
            offer =e[4]
            
        datos=(e[0],e[1],e[5],offer)
        conn.execute("INSERT INTO PRODUCTO (LINK,NAME,PRICE,OFFER) VALUES (?,?,?,?)",datos);
    conn.commit()
    
    cursor = conn.execute("SELECT NAME, LINK  from PRODUCTO")
    for row in cursor:
        print "NAME = ", row[0]
        print "LINK = ", row[1] + "\n"
        
    tkMessageBox.showinfo("PRODUCTOS", "BD creada correctamente")
    conn.close()

def ofertas():
    conn = sqlite3.connect('test.db')
    cursor = conn.execute("SELECT NAME,LINK,PRICE,OFFER  from PRODUCTO where OFFER != '' ")
  
    
    scrollbar = Tkinter.Scrollbar(root)
    scrollbar.pack( side = Tkinter.RIGHT, fill= Tkinter.Y)
    
    mylist = Tkinter.Listbox(root, yscrollcommand = scrollbar.set,width=480)
    for row in cursor:
        mylist.insert('end', "Nombre: " + row[0])
        mylist.insert('end', "Link: " + row[1])
        mylist.insert('end', "Precio: " + row[3])
        mylist.insert('end', "Precio oferta: " + row[2])
        mylist.insert('end', " ")
    
    mylist.pack( side = Tkinter.LEFT, fill = Tkinter.BOTH )
    scrollbar.config( command = mylist.yview )
 
    print "Operation done successfully";
    
    conn.close()

def busqueda(): 
    
    conn = sqlite3.connect('test.db')
    
    
    top = Tkinter.Tk()  
    
    L1 = Tkinter.Label(top, text="Introduzca el nombre del producto:")
    L1.pack( side = Tkinter.LEFT)
    E1 = Tkinter.Entry(top, width=16, bd = 5)
    E1.pack()
    
    def busca(texto):
        filtra(texto)
    
    def filtra(texto):
        lista = []
        top2 = Tkinter.Tk()
        top2.geometry("500x500")
        scrollbar = Tkinter.Scrollbar(top2)
        scrollbar.pack( side = Tkinter.RIGHT, fill= Tkinter.Y)
        cursor = conn.execute("SELECT NAME,LINK,PRICE,OFFER  from PRODUCTO WHERE NAME LIKE '%"+str(texto)+"%'")
        
        mylist = Tkinter.Listbox(top2, yscrollcommand = scrollbar.set,width=480)
        for row in cursor:
            mylist.insert('end',"Nombre: "+row[0])
            mylist.insert('end',"Link: "+row[1])
            mylist.insert('end',"Precio: "+row[2])
            if row[3] != None:
                mylist.insert('end',"Precio oferta: "+row[3])
            mylist.insert('end'," ")
            lista.append(row[1]+"\n"+"\n")
        
        mylist.pack( side = Tkinter.LEFT, fill = Tkinter.BOTH )
        scrollbar.config( command = mylist.yview )
        top.destroy()   
            
    B = Tkinter.Button(top, text ="Hello", command = lambda:busca(E1.get()))
    B.pack()
    top.mainloop()
    
    conn.close()

menubar = Tkinter.Menu(root)
filemenu = Tkinter.Menu(menubar, tearoff=0)
filemenu.add_command(label="Almacenar", command=lambda:almacenar())

filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="Menu", menu=filemenu)

root.config(menu=menubar)
root.mainloop()
