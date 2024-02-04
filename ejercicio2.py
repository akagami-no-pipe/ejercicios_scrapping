import requests
from bs4 import BeautifulSoup

url = 'https://stackoverflow.com/questions'
encabezados = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
}

respuesta      = requests.get(url, headers=encabezados)
soup           = BeautifulSoup(respuesta.text, features="lxml")
div_preguntas  = soup.find(id='questions')
preguntas      = div_preguntas.find_all('div', class_=('s-post-summary','js-post-summary'))

for pregunta in preguntas:
    titulo      = pregunta.find('h3', class_='s-post-summary--content-title').text.replace('\n', '').replace('\r', '').strip()
    descripcion = pregunta.find('div', class_='s-post-summary--content-excerpt').text.replace('\n', '').replace('\r', '').strip()
    #la ventaja de bs4 a lxml es que provee diversos metodos para acceder a los elemntos del arbol como el siguiente: 
    # titulo = pregunta.find('h3', class_='s-post-summary--content-title')
    # titulo.find_next_sibling('div').text
    print('Título: ', titulo)
    print('Descripción: ', descripcion)
    print('-------------------------------------------------------------------------------------')