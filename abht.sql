
CREATE TABLE Data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    jour DATE,
    id_station INT,
    auto_cumul FLOAT,
    nbr_missing_values INT,
    rate FLOAT,
    manual_cumul FLOAT,
    missing_state_manual TINYINT(1),
    difference FLOAT
);

CREATE TABLE ActionCorrective (
    id INT AUTO_INCREMENT PRIMARY KEY,
    description TEXT
);

CREATE TABLE ActionCorrective_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    idAction INT,
    id_Data INT,
    duree INT,
    datedebut DATE,
    dateFinPrevu DATE,
    dateFinReel DATE,
    statut ENUM('en cours', 'complété', 'annulé'),
    cout FLOAT,
    description TEXT,
    FOREIGN KEY (idAction) REFERENCES ActionCorrective(id),
    FOREIGN KEY (id_Data) REFERENCES Data(id)
);



CREATE TABLE Pluviometre_manuel (
    id INT AUTO_INCREMENT  PRIMARY KEY,
    cout FLOAT,
    conditions_installation FLOAT
);

CREATE TABLE Pluviometre_automatique (
    id INT AUTO_INCREMENT  PRIMARY KEY,
    basculement FLOAT,
    marque enum('Paratronic', 'Komatsu', 'Nippon' ),
    cout FLOAT,
    conditions_installation FLOAT
);

CREATE TABLE Observateur (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255),
    prenom VARCHAR(255),
    expertise FLOAT,
    affiliation ENUM('abht', 'autre')
);

CREATE TABLE Station (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    region VARCHAR(255),
    bassin VARCHAR(255),
    id_observateur INT,
    altitude FLOAT,
    id_pluviometre_man INT,
    id_pluviometre_auto INT,
    mode_transmission_auto ENUM('GPRS','RADIO','VSAT','filaire'),
    relai ENUM('relai1', 'relai2'),
    FOREIGN KEY (id_observateur) REFERENCES Observateur(id),
    FOREIGN KEY (id_pluviometre_man) REFERENCES Pluviometre_manuel(id),
    FOREIGN KEY (id_pluviometre_auto) REFERENCES Pluviometre_automatique(id)

);



CREATE TABLE Stations_proches (
    id_stationA INT,
    id_stationB INT,
    PRIMARY KEY (id_stationA, id_stationB),
    FOREIGN KEY (id_stationA) REFERENCES Station(id) ON DELETE CASCADE,
    FOREIGN KEY (id_stationB) REFERENCES Station(id) ON DELETE CASCADE
);

CREATE TABLE User (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255),
    prenom VARCHAR(255),
    droit ENUM('admin','user'),
    login VARCHAR(255) UNIQUE,
    password VARCHAR(255)
);