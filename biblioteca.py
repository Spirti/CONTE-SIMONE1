from datetime import datetime, date
from flask import Flask, render_template, request, flash, url_for, session, redirect
import sqlite3, random
from string import ascii_letters
from datetime import date,timedelta

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


   


    if not session.get("nome"):
        return render_template('index.html')
    user=session.get("nome", None)
    tipo=session.get("tipo", None)
    print(user)
    messaggio =""
    odierno = date.today()
    print(odierno)
    connection = sqlite3.connect('biblioteca.db') #cambiare il nome del database nel caso
    connection.row_factory=sqlite3.Row
    dates  = connection.execute ('SELECT data_partenza,Numero_giorni FROM Prestito').fetchall()
    posts = connection.execute ('SELECT ISBN, ID FROM Prestito').fetchall() 
    pasts = connection.execute ('SELECT ISBN, Titolo FROM Libro').fetchall() 
    for row in dates:
        partenza = datetime.strptime(row['data_partenza'], '%Y-%m-%d')
        #print((odierno-oggetto_datetime.date()).days)
        print(row['data_partenza'])
        print(type(row['Numero_giorni']))
        differenza = odierno - partenza.date() #oggi - data di partenza
        print(differenza.days) #quanti giorni sono
        diffG = row['Numero_giorni'] - differenza.days #giorni di differenza tra i giorni del prestito e i giorni effettivamente passati
        if ( diffG == 0):
            messaggio = "scade oggi"
        elif ( diffG < 0):
            messaggio= "La durata del prestito è terminata, restituire" 
        elif (diffG > 0):
            messaggio = f"Giorni rimanenti:  { diffG} " 
            print (messaggio)
        print(diffG)
        #fare il controlllo su questa differenza (se >0 tutto a posto se =0 scade oggi se <0 problema)
        #print( "siamo tornati in due")

    

    return render_template('loggato.html', user=user, tipo=tipo, messaggio = messaggio, posts = posts, pasts = pasts)

@app.route('/login') #miao proprio coccode perfino 
def login ():
    return render_template ('log_in.html',messaggio="")

@app.route('/executelogin', methods=('GET', 'POST'))
def execlog():
    if request.method == 'POST':
        user = request.form['username']
        psw = request.form['password']
        #print(user, psw)
        query = 'SELECT Username, Password, Tipo FROM Utente where Username="' + user + '" and Password="' + psw + '"'
        print(query)
        connection = sqlite3.connect('biblioteca.db')
        connection.row_factory = sqlite3.Row
        result = connection.execute(query).fetchall()
        print(result)
        if (len(result)) == 0:
            print("Credenziali non corrette")
            return render_template('log_in.html')
        else:
            print("Logged in")
            session["nome"] = user
            session["connesso"] = True
            print(result[0])
            session["tipo"]=result[0]["Tipo"]  
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

@app.route('/logout')
def logout():
    session.clear()
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


@app.route('/admin')
def admin():
    user=session.get("nome", None)
    tipo=session.get("tipo", None)
    return render_template("admin.html",user=user,tipo=tipo)

@app.route('/inserisci', methods=("POST",))
def inserisci():
    titolo = request.form['titolo']
    autore = request.form['autore']
    ISBN = int(request.form['ISBN'])
    n_copie = request.form['n_copie']
    descrizione = request.form['descrizione']
    connection = sqlite3.connect('biblioteca.db')
    connection.row_factory = sqlite3.Row
    connection.execute('INSERT INTO Libro(Titolo,Autore,ISBN,N_copie,Descrizione,Disponibilita) VALUES(?,?,?,?,?,true)',(titolo,autore,ISBN,n_copie,descrizione))
    connection.commit()
    connection.close()
    return redirect('/admin')


@app.route('/collezione')
def collezione ():
    user = session.get("nome")
    tipo=session.get("tipo", None)
    connection = sqlite3.connect('biblioteca.db') #cambiare il nome del database nel caso
    connection.row_factory=sqlite3.Row
    posts = connection.execute ('SELECT * FROM Libro').fetchall() #same goes for tabella
    connection.close()
    print (posts)
    return render_template ('collezione.html',posts=posts, user=user, tipo=tipo)

@app.route('/<int:ISBN>/cancella', methods=("POST",))
def cancella (ISBN):
    connection = sqlite3.connect('biblioteca.db') #cambiare il nome del database nel caso
    connection.row_factory=sqlite3.Row
    posts = connection.execute ('DELETE FROM Libro WHERE ISBN=?',(ISBN,)) #same goes for tabella
    connection.commit()
    connection.close()
    #print (posts)
    return redirect('/collezione')



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


@app.route('/restituire', methods=("POST",))
def restituisco ():
    ISBN = request.form["ISBN"]
    user = request.form['user']
    connection = sqlite3.connect('biblioteca.db')
    connection.row_factory=sqlite3.Row
    connection.execute("DELETE FROM Prestito WHERE ISBN = ? AND ID = ?", (ISBN, user))

    
    connection.commit()
    connection.close()
    return redirect ('/')
app.run(host='0.0.0.0', port=81, debug=True) #salviamo i maro
#perche loro sono innocenti 