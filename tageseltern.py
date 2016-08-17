import scrapy

class TageselternSpider(scrapy.Spider):
    name = 'tageseltern'
    start_urls = ['https://www.kinderdrehscheibe.at/de/beratung/online-suche-wiener-kinderbetreuung/']
    
    def after_post(self, response):
        #print(response.body)
        print(response.xpath('//*[@id="platzsearchresults"]/div/table/tbody/tr[1]/td/h2'))
    
    def parse(self, response):
        formdata = {
            'initplatzsearch': '1',
            'plz': '1010',
            'alter': '1',
            'freeplaces': '1',
            'art[tm]': '1',
            'SUBMIT': 'Betreuungsplätze suchen',
        }
        return [scrapy.http.FormRequest(url=self.start_urls[0],
                    formdata=formdata,
                    callback=self.after_post)]