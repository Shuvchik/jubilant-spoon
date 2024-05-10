import scrapy


class VinylSpiderSpider(scrapy.Spider):
    name = "vinyl_spider"
    allowed_domains = ["vinyl.ru"]
    start_urls = ["https://vinyl.ru/catalog/music_style/rock/"]

#Функция парсит первую страницу каталога
    def parse(self, response):
        records = response.xpath('//html/body/main/div/div/div/div[2]/div[2]/div/div')

        for record in records:
            artist = record.xpath('.//div/div[2]/h4/a/text()[1]').get()
            album_title = record.xpath('.//div/div[2]/h4/a/text()[2]').get()
            price = record.xpath('.//div/div[3]/div/div/span/text()').get().replace(' ', '')[:-1]
            link = record.xpath('.//div/div[2]/h4/a/@href').get()
            yield response.follow(url=link, callback=self.parse_record,
                                  meta={'artist': artist,
                                        'album_title': album_title,
                                        'price': price})


#Функция парсит каждую страницу с альбомом, все поля извлекатьне стала
    def parse_record(self, response):
        album = response.xpath('/html/body/main/div/div[2]/div[1]/div[1]/div[2]/ul')
        album_release = album.xpath('.//li[1]/p/text()').get()[-4:]
        year_release = album.xpath('.//li[2]/p/text()').get()[-4:]
        type_release = album.xpath('.//li[3]/a/text()').get().strip()
        label = album.xpath('.//li[4]/a/text()').get().strip()
        country = album.xpath('.//li[8]/p/text()').get().split(':')[-1].strip()
        album_title = response.request.meta['album_title']
        artist = response.request.meta['artist']
        price = response.request.meta['price']
        yield {
            'artist': artist,
            'album_title': album_title,
            'price': int(price),
            'album_release': int(album_release),
            'year_release': int(year_release),
            'type_release': type_release,
            'label': label,
            'country': country
        }
