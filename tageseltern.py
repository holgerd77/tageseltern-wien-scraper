import time, scrapy

class TageselternSpider(scrapy.Spider):
    name = 'tageseltern'
    start_urls = ['https://www.kinderdrehscheibe.at/de/beratung/online-suche-wiener-kinderbetreuung/']
    
    def parse(self, response):
        #print(response.body)
        items_sel = response.xpath('//div[@id="platzsearchresults"]/div[@class="item"]')
        for item_sel in items_sel:
            title = item_sel.xpath('.//tr[1]//h2/text()').extract()[0].strip()
            last_update = item_sel.xpath('.//tr[4]/td[2]/text()').extract()
            if len(last_update) > 0:
                last_update = last_update[0]
            else:
                last_update = "Not available"
            if 'in:' in title:
                title = title[:-4]
                location = item_sel.xpath('.//tr[1]//span[@class="black"]/text()').extract()[0]
            else:
                location = item_sel.xpath('.//tr[2]/td[1]/text()').extract()[0].strip()
            item_array = {
                'title': title,
                'location': location,
                'plz': location[0:4],
                'available': item_sel.xpath('.//tr[4]/td[1]/text()').extract()[0].strip(),
                'last_update': last_update,
            }
            print(item_array)
            yield item_array
    
    def start_requests(self):
        plz_list = ["1%02d0" % i for i in range(0, 24)]
        start_requests = []
        for plz in plz_list:
            formdata = {
                'initplatzsearch': '1',
                'plz': plz,
                'alter': '1',
                'freeplaces': '1',
                'art[tm]': '1',
                'SUBMIT': 'Betreuungsplätze suchen',
            }
            yield scrapy.http.FormRequest(url=self.start_urls[0],
                        formdata=formdata,
                        dont_filter=True)