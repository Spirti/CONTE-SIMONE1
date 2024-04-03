CREATE TABLE Libro (
ISBN		smallint (13) primary key,
Titolo		varchar	 (100),
Autore 		varchar  (100),
N_Copie	        varchar  (100),
disponibilità	boolean		
CHECK (LENGTH(ISBN) == 13)	
);


CREATE TABLE Utente(
ID		varchar	 (100) primary key,
Nome		varchar	 (100),
Cognome		varchar	 (100),
Email		varchar	 (100),
Password	varchar	 (100),
Tipo		varchar	 (100)
);


CREATE TABLE Prestito (
ISBN		smallint (13)  ,
ID		varchar	 (100) ,
Numero_giorni	int (256),
data_partenza        date,
Foreign Key (ID) REFERENCES Utente (ID),
Foreign Key (ISBN) REFERENCES Libro (ISBN),
Primary key (ISBN, ID)
)