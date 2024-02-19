DROP DATABASE IF EXISTS Seminarski;
CREATE DATABASE Seminarski;
USE Seminarski;

DROP USER IF EXISTS app;
CREATE USER app@'%' IDENTIFIED BY '1234';
GRANT SELECT, INSERT, UPDATE, DELETE ON Seminarski.* TO app@'%';

CREATE TABLE ovlasti (
	id INT PRIMARY KEY AUTO_INCREMENT,
    ovlast VARCHAR(100) NOT NULL
);

INSERT INTO ovlasti(ovlast) VALUES 
	('Admin'),
    ('Korisnik');
    
CREATE TABLE kartice (
	id INT PRIMARY KEY AUTO_INCREMENT,
    nuid VARCHAR(100) NOT NULL
);

INSERT INTO kartice(nuid) VALUES
	('EA 4C C0 2E'),
    ('A3 CB DA 2B'),
    ('06 E5 F5 12'),
    ('E1 F7 E8 2B'),
    ('51 B8 E8 2B'),
    ('D4 F8 F2 1E'),
    ('B4 F8 01 1E'),
    ('C4 7D AA 1E');
    
CREATE TABLE korisnik (
	id INT PRIMARY KEY AUTO_INCREMENT,
    ime CHAR(50) NOT NULL,
    prezime CHAR(50) NOT NULL,
    username VARCHAR(50) NOT NULL,
    password BINARY(32) NOT NULL,
    id_ovlasti INT,
    FOREIGN KEY (id_ovlasti) REFERENCES ovlasti(id) ON UPDATE CASCADE ON DELETE SET NULL
);

INSERT INTO korisnik(ime, prezime, username, password, id_ovlasti) VALUES
	('Josip', 'Ivatek', 'jivatek', UNHEX(SHA2('0000', 256)), 1),
    ('Stipe', 'Karuza', 'skaruza', UNHEX(SHA2('1986', 256)), 1),
    ('Ante', 'Antić', 'aantic', UNHEX(SHA2('1111', 256)), 2),
    ('Ivo', 'Ivić', 'iivic', UNHEX(SHA2('2222', 256)), 2);
    
CREATE TABLE proizvod (
	id INT PRIMARY KEY AUTO_INCREMENT,
    ime CHAR(50) NOT NULL,
    cijena INT NOT NULL,
    id_kartice INT,
    FOREIGN KEY (id_kartice) REFERENCES kartice(id) ON UPDATE CASCADE ON DELETE SET NULL
);

INSERT INTO proizvod(ime, cijena, id_kartice) VALUES
	('Sok od jabuke', 3, 1),
    ('Pivo', 1, 2),
    ('Bijelo vino', 8, 3),
    ('Kruh', 2, 4),
    ('Sir', 4, 5),
    ('Tirolska kobasica', 6, 6),
    ('Hrenovke', 5, 7),
    ('Jaja', 3, 8);

