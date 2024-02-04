import requests
from bs4 import BeautifulSoup

url = 'https://news.ycombinator.com/'
encabezados = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
}

respuesta    = requests.get(url, headers=encabezados)
soup         = BeautifulSoup(respuesta.text, features="lxml")
div_noticias = soup.find_all('tr', class_='athing')
for noticia in div_noticias:
    titulo      = noticia.find('span', class_='titleline').text.strip()
    url         = noticia.find('span', class_='titleline').find('a').get('href')
    metadata    = noticia.find_next_sibling()
    puntaje     = metadata.find('span', class_='score').text if metadata.find('span', class_='score') else 'Sin puntaje'
    #el parametro attrs sirve para pasarle un diccionario con atributos
    datos       = metadata.find('span', attrs={'class': 'subline'})
    comentarios = datos.text.split('|')[-1] if 'comments' in metadata.text.split('|')[-1] else 'Sin comentarios'
    print('Título: ', titulo)
    print('URL: ', url)
    print('Puntaje: ', puntaje)
    print('Comentarios: ', comentarios)
    print('---------------------------------------------------------')
