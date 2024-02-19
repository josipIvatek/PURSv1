SELECT proizvod.ime, proizvod.cijena, kartice.nuid FROM skenirano
LEFT JOIN kartice ON kartice.id = skenirano.id_kartice
LEFT JOIN korisnik ON korisnik.id = skenirano.id_korisnik
LEFT JOIN proizvod ON proizvod.id_kartice = kartice.id
where skenirano.id_korisnik = {{id_korisnika}}