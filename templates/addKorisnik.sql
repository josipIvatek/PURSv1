INSERT INTO Korisnik (ime, prezime, username, password, id_ovlasti)
VALUES ('{{ime}}', '{{prezime}}', '{{username}}', UNHEX(SHA2('{{lozinka}}', 256)), {{id_ovlasti}})