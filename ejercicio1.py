import requests
from lxml import html

url = 'https://www.wikipedia.org/'
#Es necesario pasarle el user-agent para que sea más difícil 
#para la página detectar que estamos haciendo web scrapping
encabezados = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
}

respuesta  = requests.get(url, headers=encabezados)
parse_html = html.fromstring(respuesta.text)

#a traves de metodos
espaniol = parse_html.get_element_by_id('js-link-box-es')
print(espaniol.text_content())
idiomas = parse_html.find_class('central-featured-lang')
for idioma in idiomas:
    print(idioma.text_content())

#a traves de xpath
espaniol2 = parse_html.xpath("//a[@id='js-link-box-es']/strong/text()")
print(espaniol2)
idiomas2 = parse_html.xpath("//div[contains(@class, 'central-featured-lang')]/a/strong/text()")
print(idiomas2)