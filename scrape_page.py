def scrape_page(link):
    from bs4 import BeautifulSoup
    import requests
    import datetime

    source = requests.get(link).text

    soup = BeautifulSoup(source, "lxml")
    try:
        naslov = soup.find("div", id = "content_holder").h2.text  #naslov skrejpovan
    except Exception as e:
        naslov = None

    try:
        web_stranica = soup.find("div", id = "aboutAuthor").a["href"]
        if web_stranica.count("//") == 0:       #moze ozbiljnija provjera
            web_stranica = None
    except Exception as e:
        web_stranica = None

    try:
        slike = soup.find("div", id = "rea_blueimp").find_all("img")
        spremne_slike = []
        for slika in slike:
            if slika["src"].count("https://www.realitica.com") == 0:
                spremna_slika = "https://www.realitica.com" + slika["src"]
                spremne_slike.append(spremna_slika)
            else:
                spremne_slike.append(slika["src"])
    except Exception as e:
        spremne_slike = []

    listing_body = soup.find("div", id = "listing_body")

    cont = listing_body.div.extract().stripped_strings

    tekst = listing_body.text
    x = tekst.split("\n")


    for i in x:
        if i.count("Opis") > 0:
            indeks = x.index(i)
    opis = x[indeks].split(": ")[1]

    for i in x:
        if i.count("Oglas Broj") > 0:
            indeks = x.index(i)
    broj_id = int(x[indeks].split(": ")[1])

    for i in x:
        if i.count("Zadnja Promjena") > 0:
            indeks = x.index(i)
    zadnja_promjena = x[indeks].split(": ")[1]
    zadnja_promjena = datetime.datetime.strptime(zadnja_promjena, "%d %b, %Y")

    for i in x:
        if i.count("Vrsta") > 0:
            indeks = x.index(i)
    y = x[indeks].split(": ")

    for i in x:
        if i.count("Oglasio") > 0:
            indeks = x.index(i)
    z = x[indeks].split(": ")

    lista = ["Vrsta", "Područje", "Lokacija", "Adresa", "Energetski Razred", "Cijena", "Godina Gradnje", "Spavaćih Soba", "Kupatila", "Stambena Površina", "Parking Mjesta", "Od Mora (m)", "Novogradnja", "Klima Uređaj"]
    listaZ = ["Oglasio", "Registarski broj", "Mobitel", "Telefon", "Kontaktiraj Oglašivača"]

    def scrape(name):
        for i in y:
            if i.count(name)>0:
                value = y[y.index(i)+1]
                break
            else:
                value = None
        if value != None:
            for i in lista:
                if value.count(i) > 0:
                    new_value = value.split(i)
                    break
                else:
                    new_value = [y[len(y)-1], ""]
        else:
            new_value = [None, ""]

        return (new_value[0])

    def scrape_bool(name):
        znak = False
        for i in y:
            if i.count(name) > 0:
                znak = True
        return znak


    def scrapeZ(name):
        for i in z:
            if i.count(name)>0:
                value = z[z.index(i)+1]
                break
            else:
                value = None
        if value != None:
            for i in listaZ:
                if value.count(i) > 0:
                    new_value = value.split(i)
                    break
                else:
                    new_value = [z[len(z)-1], ""]
        else:
            new_value = [None, ""]

        return (new_value[0])

    try:
        cijena = float(scrape("Cijena").split("€")[1])
    except Exception as e:
        cijena = None
    try:
        godina_gradnje = int(scrape("Godina Gradnje"))
    except Exception as e:
        godina_gradnje = None
    try:
        spavacih_soba = int(scrape("Spavaćih Soba"))
    except Exception as e:
        spavacih_soba = None
    try:
        kupatila = int(scrape("Kupatila"))
    except Exception as e:
        kupatila = None
    try:
        stambena_povrsina = int(scrape("Stambena Površina").split(" ")[0])
    except Exception as e:
        stambena_povrsina = None
    try:
        parking_mjesta = int(scrape("Parking Mjesta"))
    except Exception as e:
        parking_mjesta = None
    try:
        od_mora = int(scrape("Od Mora (m)"))
    except Exception as e:
        od_mora = None
    
    document = {"naslov": naslov, "vrsta": scrape("Vrsta"), "podrucje": scrape("Područje"), "lokacija": scrape("Lokacija"), "adresa": scrape("Adresa"), "energetski_razred": scrape("Energetski Razred"), "cijena": cijena,
    "godina_gradnje": godina_gradnje, "spavacih_soba": spavacih_soba, "kupatila": kupatila, "stambena_povrsina_(m2)": stambena_povrsina,
    "parking_mjesta": parking_mjesta, "od_mora_(m)": od_mora, "novogradnja": scrape_bool("Novogradnja"), "klima_uredjaj": scrape_bool("Klima Uređaj"), "opis": opis, 
    "web_stranica": web_stranica, "oglasio": scrapeZ("Oglasio"), "mobitel": scrapeZ("Mobitel"), "telefon": scrapeZ("Telefon"), "Oglas_Broj": broj_id, "zadnja_promjena": zadnja_promjena, "slike": spremne_slike
    }

    return(document)    