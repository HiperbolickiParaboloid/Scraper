import scrape_links
import requests
from bs4 import BeautifulSoup
from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def scraper():
    num = 0
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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)