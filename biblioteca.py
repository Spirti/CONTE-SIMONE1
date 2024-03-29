from flask import Flask, render_template, request, flash, url_for, session, redirect, session
app = Flask(__name__)
'''
connection = sqlite3.connect('biblioteca.db')
with open ('crea_table.sql') as f:
	connection.executescript(f.read())
connection.commit()
connection.close()
'''
@app.route('/')
def index ():
    '''
    connection = sqlite3.connect('biblioteca.db') #cambiare il nome del database nel caso
    connection.row_factory=sqlite3.Row
    posts = connection.execute ('SELECT * FROM tabella').fetchall() #same goes for tabella
    connection.close()
    '''
    return render_template ('index.html') #posts = posts 

@app.route('/login') #miao proprio coccode perfino 
def login ():
    return render_template ('log_in.html')



@app.route('/signup')
def signup ():
    return render_template ('sign_up.html')




@app.route('/collezione')
def collezione ():
    return render_template ('collezione.html')



app.run(host='0.0.0.0', port=81, debug=True) #salviamo i maro
#perche loro sono innocenti 