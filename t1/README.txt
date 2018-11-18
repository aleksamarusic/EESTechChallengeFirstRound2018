OPISI FAJLOVA:
    - album_list_getter.py: obilazi sajt i sakuplja url-ove svih albuma (i ostalih zapisa) za zadatu državu
      Država se zadaje izmenom stringa na liniji 214, takođe treba zadati i koliko strana sadrži lista urlova za tu državu
      rezultate skladišti u albums.pickle

    - album_data_getter.py: obilazi url-ove za zadatu zemlju uskladištene u fajlu albums.pickle i kešira sadržaje tih stranica
      u cache.pickle. Potrebno je zadati zemlju na liniji 214

    - artists.py: obilazi sve sadržaje iz cache.pickle i generiše listu linkova do stranica umetnika u artisturls.pickle

    - credparse.py: obilazi sve url-ove iz artisturls.pickle i generiše insert upite u fajl inserts.pickle
    - dumpins.py: na osnovu inserts.pickle generiše skriptu inserts.sql pomoću koje se može popuniti tabela 'person'
      u bazi

U slučaju da programi šalju zahteve na sajt, može se desiti da se aktivira DoS zaštita sajta, u tom slučaju, program se
eventualno zaustavlja i javlja koliko url-ova nije uspelo da bude dohvaćeno. Kada sajt ponovo počne da sarađuje (ili
kada se dobije nova IP adresa), moguće je ponovo pokrenuti program i on će nastaviti rad. Ako nije obrisan cache.pickle,
biće korišćen sadržaj odatle kako bise izbeglo nepotrebno slanje zahteva
Dodatno, u credparse je implementirana i upotreba proxy servera kako bi se smanjio broj zahteva koje sajt odbije zbog
sumnje na DoS napad