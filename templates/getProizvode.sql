select proizvod.id, ime, cijena, kartice.nuid from proizvod
LEFT JOIN kartice on kartice.id = proizvod.id_kartice