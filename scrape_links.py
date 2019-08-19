def scrape_links(page_link):
    from bs4 import BeautifulSoup
    import requests
    import scrape_page
    import pymongo

    def ajdi(link):
        lista = link.split("listing/")
        int_ajdi = int(lista[1])
        return int_ajdi

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
        if not indikator:
            stan = scrape_page.scrape_page(link)
            mycol.insert_one(stan)
            print(scrape_page.scrape_page(link))
        else:
            print("Already scraped.")