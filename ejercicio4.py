from scrapy.item import Field, Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader

class Pregunta(Item):
    #campos que quiero extraer
    id          = Field()
    titulo      = Field()
    descripcion = Field()

class PreguntaSpider(Spider):
    #importante definir un name
    name = 'stackoverflowSpider'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }
    #debe ser el nombre start_urls, con otro no funciona
    start_urls = ['https://stackoverflow.com/questions']

    def parse(self, response):
        sel = Selector(response)
        preguntas = sel.xpath('//div[@id="questions"]//div[contains(@id, "question-summary")]')
        id_value = 1
        for pregunta in preguntas:
            item = ItemLoader(Pregunta(), pregunta)
            item.add_xpath('titulo', './/h3/a/text()')
            item.add_xpath('descripcion', './/div[@class="s-post-summary--content-excerpt"]/text()')
            item.add_value('id', id_value)
            yield item.load_item()
            id_value += 1

#para ejecutar el script se hacer de la siguiente forma: scrapy runspider ejercicio4.py -o data.csv -t csv