import requests
from bs4 import BeautifulSoup
import time
import datetime
import pymsgbox as pg
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pushbullet import Pushbullet

token = 'o.lGOcxCB8xKCqakqyriANUr2X1uqJMlta'
pb = Pushbullet(token)


link_table = {}
link_table_actual = {}

def send_email_alert_new(link, title, price):
    
    subject = f'NOWE MIESZKANIE NA OLX - {price} - {title}'
    
    msg = MIMEMultipart()
    msg['From'] = gmail_address
    msg['To'] = gmail_address
    msg['Subject'] = subject

    body = f'link: {link}'
    msg.attach(MIMEText(body, 'plain'))

    part = MIMEBase('application', 'octet-stream')

    text = msg.as_string()


    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(gmail_address, password)
    server.sendmail(gmail_address, 'marcink442@gmail.com', text)
    server.quit()
    
def send_email(link, title):
    try:
        subject = f'MIESZKANIA - NOWA OFERTA!! - {title}'     
        body = link
        pb.push_link(subject, body)
    
    except Exception as err:
        print('błąd wysyłania - {err}')

def main():
    try:
        for page_nr in range(1,5):
            
            site = f'https://www.olx.pl/d/nieruchomosci/mieszkania/sprzedaz/dzierzoniow/?page={page_nr}'

            page = requests.get(site)
            soup = BeautifulSoup(page.content, "html.parser")

            for orders in soup.find_all('div', class_='css-qfzx1y'):
                
                title=orders.find('strong').text.strip()
                price=orders.find(class_='price').text.strip().replace(' zł', '').replace(' ', '.')
                link = orders.find('a')['href']

                link_table_actual[link]= title, price
                
                if link not in link_table:
                    link_table[link]= title, price
                    print(f'wysyłam maila - {title}')
                    send_email_alert_new(link, title, price)

            if link_table_actual != link_table:
                
                try:
                    for key in link_table:
                        if key not in link_table_actual:
                            link_table.pop(key, None)
                except RuntimeError:
                    pass
        print(f'ilość ofert: {len(link_table)} -- {datetime.datetime.now()}')   
    except:
        print('Coś poszło nie tak :(')
        


while True:
    main()
    time.sleep(400)