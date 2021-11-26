
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import pandas as pd



lista_jogos = []

navegador = webdriver.Chrome()
navegador.get('https://steamdb.info/sales/')
sleep(3)

site_debug = BeautifulSoup(navegador.page_source, 'html.parser')

jogos = site_debug.find_all('tr', attrs={'class' : 'app'})

for jogo in jogos:

    jogo_nome = jogo.find('a', attrs={'class' : 'b'}).text

    jogo_link = jogo.find('a', attrs={'class' : 'info-icon'})['href']

    jogo_desconto = jogo.find('td', attrs={'class' : 'price-discount-major'})


    jogo_tempo_promo = jogo.find('td', attrs={'class' : 'timeago'}).text


    lista_jogos.append([jogo_nome,jogo_link,jogo_desconto,jogo_tempo_promo])



df = pd.DataFrame(lista_jogos, columns=['Nome','Link','Desconto','Tempo promoção'])

df.to_excel('jogos_Steam.xls',sheet_name='Jogos_Steam', na_rep='#N/A', header=True,index=False)

