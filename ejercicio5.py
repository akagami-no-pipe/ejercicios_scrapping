from scrapy.item import Field, Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess

class Noticia(Item):
    #campos que quiero extraer
    titular     = Field()
    descripcion = Field()

class NoticiaSpider(Spider):
    #importante definir un name
    name = 'ElUniversoSpider'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }
    #debe ser el nombre start_urls, con otro no funciona
    start_urls = ['https://www.eluniverso.com/deportes/']

    #para usar el parse de scrapy
    # def parse(self, response):
    #     sel      = Selector(response)
    #     noticias = sel.xpath('//div[contains(@class, "content-feed")]//li[@class = "relative "]')
    #     for noticia in noticias:
    #         item = ItemLoader(Noticia(), noticia)
    #         item.add_xpath('titular', './/h2/a/text()')
    #         item.add_xpath('descripcion', './/p[contains(@class, "summary")]/text()')
    #         yield item.load_item()

    #para utilizar el parse de bs4
    def parse(self, response):
        soup         = BeautifulSoup(response.body, features="lxml")
        contenedores = soup.find_all('div', class_=('content-feed'))
        for contenedor in contenedores:
            #recursive = False es para que busque solo en los hijos directos 
            noticias = contenedor.find_all('li', class_='relative')
            for noticia in noticias:
                #como no estoy usando selectores, le paso como segundo parametro el arbol entero (response.body) para rellenar
                item        = ItemLoader(Noticia(), response.body)
                titular     = noticia.find('h2').find('a').text if noticia.find('h2').find('a') else 'Sin titular'
                descripcion = noticia.find('p', class_='summary').text if noticia.find('p', class_='summary') else 'Sin descripción'
                item.add_value('titular', titular)
                item.add_value('descripcion', descripcion)
                yield item.load_item()

#para ejecutar el script se hacer de la siguiente forma: scrapy runspider nombre.py -o data_ejercicio5.json -t json

#para correr el archivo directamente como cualquier archivo py y no con el comando scrapy runspider
#se puede utilizar el crawlerprocess:
process = CrawlerProcess({
    'FEED_FORMAT': 'csv',
    'FEED_URI': 'data_ejercicio5_3.csv'
})  
process.crawl(NoticiaSpider)      
process.start()        
