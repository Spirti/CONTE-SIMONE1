CREATE TABLE Libro (
    ISBN          SMALLINT (13) PRIMARY KEY,
    Titolo        VARCHAR (100),
    Autore        VARCHAR (100),
    N_Copie       VARCHAR (100),
    Descrizione   TEXT,
    Disponibilita BOOLEAN       CHECK (LENGTH(ISBN) == 13) 
);


CREATE TABLE Utente (
    Username VARCHAR (100) PRIMARY KEY,
    Nome     VARCHAR (100),
    Cognome  VARCHAR (100),
    Email    VARCHAR (100),
    Password VARCHAR (100),
    Tipo     VARCHAR (100) 
);


CREATE TABLE Prestito (
    ISBN          SMALLINT (13),
    ID            VARCHAR (100),
    Numero_giorni INT,
    data_partenza DATE,
    FOREIGN KEY (
        ID
    )
    REFERENCES Utente (Username),
    FOREIGN KEY (
        ISBN
    )
    REFERENCES Libro (ISBN),
    PRIMARY KEY (
        ISBN,
        ID
    )
);
