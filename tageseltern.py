import scrapy

class TageselternSpider(scrapy.Spider):
    name = 'tageseltern'
    start_urls = ['https://www.kinderdrehscheibe.at/de/beratung/online-suche-wiener-kinderbetreuung/']
    
    def after_post(self, response):
        #print(response.body)
        for item_sel in response.xpath('//div[@id="platzsearchresults"]/div[@class="item"]'):
            title = item_sel.xpath('.//tr[1]//h2/text()').extract()[0].strip()
            if 'in:' in title:
                title = title[:-5]
                location = item_sel.xpath('.//tr[1]//span[@class="black"]/text()').extract()[0]
            else:
                location = item_sel.xpath('.//tr[2]/td[1]/text()').extract()[0].strip()
            item_array = {
                'title': title,
                'location': location,
                'plz': location[0:4],
                'available': item_sel.xpath('.//tr[4]/td[1]/text()').extract()[0].strip(),
                'last_update': item_sel.xpath('.//tr[4]/td[2]/text()').extract()[1],
            }
            print(item_array)
    
    def parse(self, response):
        plz_list = ['1130', '1140',]
        for plz in plz_list:
            formdata = {
                'initplatzsearch': '1',
                'plz': plz,
                'alter': '1',
                'freeplaces': '1',
                'art[tm]': '1',
                'SUBMIT': 'Betreuungsplätze suchen',
            }
            return [scrapy.http.FormRequest(url=self.start_urls[0],
                        formdata=formdata,
                        callback=self.after_post)]