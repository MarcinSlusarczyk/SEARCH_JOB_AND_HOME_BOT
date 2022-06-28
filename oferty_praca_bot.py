import requests
from bs4 import BeautifulSoup
import time
import datetime
from pushbullet import Pushbullet

stanowisko = ('finanse-ksiegowosc', 'administracja-biurowa')

token = PUSHBULLET_KEY
pb = Pushbullet(token)


def send_email(link, title):
    try:
        subject = f'NOWA OFERTA!! - {title}'     
        body = link
        pb.push_link(subject, body)
    
    except Exception as err:
        print('błąd wysyłania - {err}')


def main():
    try:
        
        for st in stanowisko:
            site = f'https://www.pracuj.pl/praca/{st};kw/dzierzoniow;wp?rd=5'

            page = requests.get(site, timeout=60)
            soup = BeautifulSoup(page.content, "html.parser")

            for orders in soup.find_all('li', class_='results__list-container-item'):
                
                try:
                    title = orders.find('a', class_="offer-details__title-link").text
                    link = orders.find('a', class_="offer-details__title-link")['href']
                    
                    with open('oferty.csv', 'a+', encoding='UTF8') as file:
                        file.seek(0)                                          
                        if title not in file.read():                            
                            file.write(f'{title}; {link}\n') # in append mode writes will always go to the end, so no need to seek()
                            send_email(link, title)
                            print(f'wysyłam mail z pracuj: {title}')
                except:
                    pass
              
        
        for st in stanowisko:
         
            site = f'https://www.olx.pl/d/praca/{st}/dzierzoniow/'

            page = requests.get(site, timeout=60)
            soup = BeautifulSoup(page.content, "html.parser")

            for orders in soup.find_all(class_='css-14fnihb'):
                title = orders.find('h6').text
                link = 'https://www.olx.pl' + orders.find('a')['href']
                    
                with open('oferty.csv', 'a+', encoding='UTF8') as file:
                    file.seek(0)
                                        
                    if title not in file.read():                            
                        file.write(f'{title}; {link}\n') # in append mode writes will always go to the end, so no need to seek()
                        send_email(link, title)
                        print(f'wysyłam mail z olx: {title}')
          
        print(f'Progam działa -- {datetime.datetime.now()}')
    
    except Exception as err:
        print(err)

while True:
    main()
    time.sleep(300)
