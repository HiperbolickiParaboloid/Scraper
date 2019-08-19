import scrape_links
import requests
from bs4 import BeautifulSoup
from flask import Flask

app = Flask(__name__)

#num = 100

@app.route("/")
def scraper():
    num = 100
    link_part_one = "https://www.realitica.com/?cur_page="
    link_part_two = "&for=DuziNajam&pZpa=Crna+Gora&pState=Crna+Gora&type%5B%5D=&lng=hr"

    while 1:
        link = link_part_one + str(num) + link_part_two
        source = requests.get(link).text
        soup = BeautifulSoup(source, "lxml")
        try:
            indicator = soup.find("div", id = "content_holder2").h3.text
            if indicator == "Oglas Nije Pronađen":
                print ("Zavrseno!")
                break
        except Exception as e:
            pass
        scrape_links.scrape_links(link)
        num = num + 1
    return "ok"

app.run(port=5000, debug=True)