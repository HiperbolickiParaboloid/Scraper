def scrape_links(page_link):
    from bs4 import BeautifulSoup
    import requests
    import scrape_page
    import pymongo

    def ajdi(link):
        lista = link.split("listing/")
        int_ajdi = int(lista[1])
        return int_ajdi
    
    def scrape_date(link):
        source = requests.get(link).text
        soup = BeautifulSoup(source, "lxml")
        listing_body = soup.find("div", id = "listing_body")
        cont = listing_body.div.extract().stripped_strings
        tekst = listing_body.text
        x = tekst.split("\n")
        for i in x:
            if i.count("Zadnja Promjena") > 0:
                indeks = x.index(i)
        zadnja_promjena = x[indeks].split(": ")[1]
        zadnja_promjena = datetime.datetime.strptime(zadnja_promjena, "%d %b, %Y")
        return zadnja_promjena


    myclient = pymongo.MongoClient("mongodb+srv://mirko:admin@scrapermirko-3rjq2.mongodb.net/test?retryWrites=true&w=majority")
    mydb = myclient["Realitica"]
    mycol = mydb["Accommodation"]

    source = requests.get(page_link).text

    soup = BeautifulSoup(source, "lxml")

    links = soup.find("div", id = "left_column_holder").find_all("a")

    lista_linkova = []
    for link in links:
        if link["href"].count("https://www.realitica.com/hr/listing") > 0:
            lista_linkova.append(link["href"])
    lista_linkova = list(dict.fromkeys(lista_linkova))

    #br = 0
    
    for link in lista_linkova:
        idd = ajdi(link)
        indikator = mycol.find_one({"Oglas_Broj": idd})
        if indikator:
            zadnja_promjena = scrape_date(link)
            if zadnja_promjena == indikator.get("zadnja promjena"):
                print("Already scraped "+link)
            else:
                stan = scrape_page.scrape_page(link)
                mycol.insert_one(stan)
                print(stan)
        else:
            stan = scrape_page.scrape_page(link)
            mycol.insert_one(stan)
            print(stan)