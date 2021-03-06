import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import pandas as pd


conection = requests.get('https://steamdb.info/sales/')
lista_jogos = []
if (conection.status_code != 200):
    navegador = webdriver.Chrome()
    navegador.get('https://steamdb.info/sales/')

down_page=0
while down_page != 30:
    navegador.execute_script("window.scrollTo(0, window.scrollY + 200)")
    sleep(0.1)
    site_debug = BeautifulSoup(navegador.page_source, 'html.parser')

    jogos = site_debug.find_all('tr', attrs={'class' : 'app'})

    down_page = down_page+1


for jogo in jogos:

    jogo_nome = jogo.find('a', attrs={'class': 'b'}).text

    jogo_link = jogo.find('a', attrs={'class': 'info-icon'})['href']

    jogo_desconto = jogo.find('td', attrs={'class': 'price-discount-major'})
    if(jogo_desconto):
        jogo_desconto = jogo.find('td', attrs={'class': 'price-discount-major'}).text
    else:
        jogo_desconto = jogo.find_all('td')[3].text

    jogo_tempo_promo = jogo.find_all('td', attrs={'class': 'timeago'})[0].text

    jogo_inicio_promo = jogo.find_all('td', attrs={'class': 'timeago'})[1].text

    ultima_atualização = jogo.find_all('td', attrs={'class': 'timeago'})[-1].text

    jogo_preço = jogo.find_all('td')[4].text

    jogo_rating = jogo.find_all('td')[5].text



    lista_jogos.append([jogo_nome,jogo_link,jogo_preço,jogo_desconto,jogo_rating,jogo_tempo_promo,jogo_inicio_promo,ultima_atualização])


df = pd.DataFrame(lista_jogos, columns=['Nome','Link','Preço','Desconto','Rating','A promoção terminará em','Promoção Iniciada há:','A ultima atualização ocorreu há:'])

df.to_excel('jogos_Steam.xls',sheet_name='Jogos_Steam', na_rep='#N/A', header=True,index=False)

