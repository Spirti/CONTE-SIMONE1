from datetime import datetime, date
from flask import Flask, render_template, request, flash, url_for, session, redirect
import sqlite3, random
from string import ascii_letters
from datetime import date

app = Flask(__name__)

app.config['SECRET_KEY'] = ''.join(random.choice(ascii_letters) for i in range(50))
'''
connection = sqlite3.connect('biblioteca.db')
with open ('cose.sql') as f:
	connection.executescript(f.read())
connection.commit()
connection.close()
'''


@app.route('/')
def index ():
    odierno = date.today()
    
    connection = sqlite3.connect('biblioteca.db') #cambiare il nome del database nel caso
    connection.row_factory=sqlite3.Row
    dates  = connection.execute ('SELECT data_partenza FROM Prestito').fetchall()
    for row in dates:
        oggetto_datetime = datetime.strptime(row['data_partenza'], '%Y-%m-%d')
        print(row['data_partenza'])
        if (odierno== oggetto_datetime.date()): #ho messo == per controllare se fa update, risulta un problema. mettere quando risolto >
            print( "siamo tornati")
            #connection.execute('UPDATE Prestito SET Numero_giorni = Numero_giorni - 1 WHERE data_partenza= ?', (row['data_partenza']))
            print( "siamo tornati in due")






    if not session.get("nome"):
        return render_template('index.html')
    user=session.get("nome", None)
    
    return render_template('index.html', user=user)

@app.route('/login') #miao proprio coccode perfino 
def login ():
    return render_template ('log_in.html',messaggio="")

@app.route('/executelogin', methods=('GET', 'POST'))
def execlog():
    if request.method == 'POST':
        user = request.form['username']
        psw = request.form['password']
        #print(user, psw)
        query = 'SELECT Username, Password FROM Utente where Username="' + user + '" and Password="' + psw + '"'
        print(query)
        connection = sqlite3.connect('biblioteca.db')
        connection.row_factory = sqlite3.Row
        result = connection.execute(query).fetchall()
        if (len(result)) == 0:
            print("Credenziali non corrette")
            return render_template('log_in.html')
        else:
            print("Logged in")
            session["nome"] = user
            session["connesso"] = True
            session.modified = True
            print("sessione:", session["nome"])
            return redirect(url_for('logok'))
    return render_template('log_in.html')

@app.route('/logok')
def logok():
    
    #print(session.get("nome", None))
    if not session.get("nome"):
        return render_template('log_in.html')
    #return redirect(url_for('ok'))
    return redirect('/')

@app.route('/signup', methods=("POST","GET"))
def signup ():

    return render_template ('sign_up.html')

@app.route('/signupmanda', methods=("POST",))
def signupmanda ():
    print("Sono qui")
    nome = request.form['nome']
    cognome = request.form['cognome']
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    password2 = request.form['password2']
    print(nome,cognome,email,username,password)
    if(password!=password2):
        return render_template ('sign_up.html',errore="Le password non sono uguali!")
    else:
        connection = sqlite3.connect('biblioteca.db') #cambiare il nome del database nel caso
        connection.row_factory=sqlite3.Row
        connection.execute('INSERT INTO Utente(Username,Nome,Cognome,Email,Password,Tipo) VALUES (?,?,?,?,?,"utente")',(username,nome,cognome,email,password))#same goes for tabella
        connection.commit()
        connection.close()
        return render_template("log_in.html",messaggio="Registrazione avvenuta con successo")
    #return render_template ('sign_up.html',errore="")


@app.route('/collezione')
def collezione ():
    nome = session.get("nome")
    connection = sqlite3.connect('biblioteca.db') #cambiare il nome del database nel caso
    connection.row_factory=sqlite3.Row
    posts = connection.execute ('SELECT * FROM Libro').fetchall() #same goes for tabella
    connection.close()
    print (posts)
    return render_template ('collezione.html',posts=posts, nome=nome)


@app.route('/prenotare', methods=("POST",))
def prenotare ():
    ISBN = request.form['ISBN']
    N_Copie = request.form['N_Copie']

   # ID = session.get("ID")
   # print (ID)
    return render_template('prestito.html', ISBN = ISBN, N_Copie = N_Copie)



@app.route('/prenotazione', methods=("POST",))
def prenotazione ():
    ISBN = request.form['ISBN']
    ID = session.get("nome")
    N_Copie = request.form['N_Copie']
    Numero_giorni = request.form['Numero_giorni']
    data_partenza = date.today()
    print (N_Copie)
    connection = sqlite3.connect('biblioteca.db') #cambiare il nome del database nel caso
    connection.row_factory=sqlite3.Row
    if (N_Copie == "1"):
        print (N_Copie)
        connection.execute('UPDATE Libro SET N_Copie = N_Copie - 1 WHERE ISBN= ?', (ISBN,))
        connection.execute('UPDATE Libro SET Disponibilita = False WHERE ISBN= ?', (ISBN,))
        connection.execute('INSERT INTO Prestito(ISBN,ID,Numero_giorni, data_partenza) VALUES (?,?,?,?)',(ISBN,ID,Numero_giorni,data_partenza))
    else:
         connection.execute('UPDATE Libro SET N_Copie = N_Copie - 1 WHERE ISBN= ?', (ISBN,))
         connection.execute('INSERT INTO Prestito(ISBN,ID,Numero_giorni, data_partenza) VALUES (?,?,?,?)',(ISBN,ID,Numero_giorni,data_partenza))
    connection.commit()
    connection.close()
    flash('Prenotazione effettuata con successo!', 'success') 
    return redirect ('/collezione')

    

@app.route('/ricerca', methods=("POST",))
def ricerca():
    titolo = request.form['Titolo']
    autore = request.form['Autore']
    print(titolo, autore)
    if titolo!="" and autore=="":
        connection = sqlite3.connect('biblioteca.db')
        connection.row_factory=sqlite3.Row
        risultato = connection.execute(" SELECT * FROM Libro WHERE Titolo LIKE (?)",(f'%{titolo}%',)).fetchall()
        connection.commit()
        connection.close( )
    elif titolo=="" and autore!="":
        connection = sqlite3.connect('biblioteca.db')
        connection.row_factory=sqlite3.Row
        risultato = connection.execute(" SELECT * FROM Libro WHERE Autore LIKE (?)",(f'%{autore}%',)).fetchall()
        connection.commit()
        connection.close( )
    elif titolo!="" and autore!="":
        connection = sqlite3.connect('biblioteca.db')
        connection.row_factory=sqlite3.Row
        risultato = connection.execute(" SELECT * FROM Libro WHERE Titolo LIKE ? and Autore LIKE ?",(f'%{titolo}%',f'%{autore}%',)).fetchall()
        connection.commit()
        connection.close()
    return render_template ('collezione.html',posts=risultato)

app.run(host='0.0.0.0', port=81, debug=True) #salviamo i maro
#perche loro sono innocenti 