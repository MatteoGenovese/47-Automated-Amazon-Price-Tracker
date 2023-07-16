import smtplib

import requests
from bs4 import BeautifulSoup

from data import password

headers = {
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 "
                  "Safari/537.36"
}


def sendEmail(products):
    # search your smtp information by google it
    with smtplib.SMTP("smtp.gmail.com") as connection:
        # create transport layer security, it protect the connection at our e-mail server
        connection.starttls()
        connection.login(user=password.myEmail, password=password.myPassword)
        msg = f"Subject:YourPriceTracker\n\n"
        for product in products:
            msg += f"{product['url']}\n{product['title']}\n{product['price']}\n\n\n"
        print(msg)
        connection.sendmail(from_addr=password.myEmail, to_addrs="matteo.genovese@icloud.com",
                            msg=msg.encode('utf-8'))
        connection.close()


products_to_track = [
    {
        "url": "https://www.amazon.it/Punteggio-segnapunti-portatile-racchetta-mantenere/dp/B09QZ9G22S/ref"
               "=sr_1_1_sspa?keywords=segnapunti%2Bpadel&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1",
        "price_for_advise": 25
    },
    {
        "url": "https://www.amazon.it/adidas-Pala-Granite-Carbon-Ctrl/dp/B0B4SW92VS/ref=sr_1_2_sspa?__mk_it_IT=%C3"
               "%85M%C3%85%C5%BD%C3%95%C3%91&keywords=padel&sr=8-2-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1",
        "price_for_advise": 170
    },
]

product_with_good_price = []

for product in products_to_track:
    response = requests.get(product["url"], headers=headers)
    sp = BeautifulSoup(response.text, "lxml")
    title = sp.select("div h1 span")[0].get_text().strip()
    price = sp.select("div.a-section span.a-price span.a-offscreen")[0].get_text()
    price_as_float = float(".".join(price.split(",")).split("€")[0])
    # check if price is lower than price_to_advise than send email
    if price_as_float < product["price_for_advise"]:
        productAlert = {
            "url": product["url"],
            "title": title,
            "price": "{:.2f}".format(price_as_float)+"€",
        }
        product_with_good_price.append(productAlert)
if len(product_with_good_price) > 0:
    sendEmail(product_with_good_price)
