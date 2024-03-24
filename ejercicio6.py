from scrapy.item import Field, Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

class Hotel(Item):
    nombre      = Field()
    precio      = Field()
    descripcion = Field()
    amenities   = Field()
    
class TripAdvisor(CrawlSpider):
    name = 'Hoteles'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }
    start_urls = ['https://www.tripadvisor.com/Hotels-g303506-Rio_de_Janeiro_State_of_Rio_de_Janeiro-Hotels.html']
    
    #para decirle a scrapy cuanto tiempo se debe demorar en hacer una consulta nueva 
    #esto para que no nos detecten como un robot
    download_delay = 3
    
    #aqui se definen las reglas para el crawlSpider sobre a donde tiene que ir y a donde no tiene que ir para buscar la información
    #son escritas en base a los patrones que encuentro en las urls a las que quiero ir
    #follow es para ir hacia la url
    #la funcion del callback se llama cuando se haga un requerimiento a los links que cumplan con el patron del linkestractor
    rules = (
        Rule( LinkExtractor(allow=r'/Hotel_Review-g303506'), follow = True, callback = 'parse_hotel'),
    )
    
    #se crea funcion para procesar el texto con MapCompose
    def quitarSimboloDolar(self, texto):
        nuevoTexto = texto.replace('$', '')
        return nuevoTexto
    
    def parse_hotel(self, response):
        sel  = Selector(response)
        item = ItemLoader(Hotel(), sel)
        
        item.add_xpath('nombre', '//h1[@id="HEADING"]/text()')
        item.add_xpath('precio', '//div[@data-automation="metaPrice"]/text()', MapCompose(self.quitarSimboloDolar))
        item.add_xpath('descripcion', '//div[@data-tab="TABS_ABOUT"]/div[@style="max-height: none; line-break: normal; cursor: auto;"]/text()')
        item.add_xpath('amenities', '//div[@data-test-target="hr-about-group-property"]/following-sibling::div[1]/div[@data-test-target="amenity_text"]/text()')
        
        yield item.load_item()