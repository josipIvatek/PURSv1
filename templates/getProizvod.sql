SELECT ime, cijena, kartice.nuid FROM proizvod
LEFT JOIN kartice ON kartice.id = proizvod.id_kartice
WHERE kartice.nuid = {{nuid}}
