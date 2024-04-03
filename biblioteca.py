from flask import Flask, render_template, request, flash, url_for, session, redirect, session
import sqlite3
app = Flask(__name__)
'''
connection = sqlite3.connect('biblioteca.db')
with open ('cose.sql') as f:
	connection.executescript(f.read())
connection.commit()
connection.close()
'''


@app.route('/')
def index ():
    
    
    
    return render_template ('index.html') #posts = posts 

@app.route('/login') #miao proprio coccode perfino 
def login ():
    return render_template ('log_in.html')



@app.route('/signup')
def signup ():
    return render_template ('sign_up.html')




@app.route('/collezione')
def collezione ():

    connection = sqlite3.connect('biblioteca.db') #cambiare il nome del database nel caso
    connection.row_factory=sqlite3.Row
    posts = connection.execute ('SELECT * FROM Libro').fetchall() #same goes for tabella
    connection.close()
    
    return render_template ('collezione.html',posts=posts)



app.run(host='0.0.0.0', port=81, debug=True) #salviamo i maro
#perche loro sono innocenti 