SELECT proizvod.id, ime, cijena, kartice.nuid FROM proizvod
LEFT JOIN kartice ON kartice.id = proizvod.id_kartice