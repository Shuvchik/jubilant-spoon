"""
Создайте новый проект Scrapy. Дайте ему подходящее имя и убедитесь, что ваше окружение правильно настроено для работы с проектом.
Создайте нового паука, способного перемещаться по сайту www.unsplash.com. Ваш паук должен уметь перемещаться по
категориям фотографий и получать доступ к страницам отдельных фотографий.
Определите элемент (Item) в Scrapy, который будет представлять изображение. Ваш элемент должен включать такие детали,
как URL изображения, название изображения и категорию, к которой оно принадлежит.
Используйте Scrapy ImagesPipeline для загрузки изображений. Обязательно установите параметр IMAGES_STORE в файле settings.py.
 Убедитесь, что ваш паук правильно выдает элементы изображений, которые может обработать ImagesPipeline.
Сохраните дополнительные сведения об изображениях (название, категория) в CSV-файле. Каждая строка должна соответствовать одному
 изображению и содержать URL изображения, локальный путь к файлу (после загрузки), название и категорию.
"""

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from ..items import UnsplashItem
from itemloaders.processors import MapCompose
from urllib.parse import urljoin


class UnsplashSpiderSpider(CrawlSpider):
    name = "unsplash_spider"
    allowed_domains = ["unsplash.com"]
    start_urls = ["https://unsplash.com"]

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="aD8H3"]/a'), callback="parse_item",
                           follow=True), )

    # Получаем ссылки на страницы фотографий

    def parse_item(self, response):
        # print(response.url)
        loader = ItemLoader(item=UnsplashItem(), response=response)
        loader.default_input_processor = MapCompose(str.strip)
        #парсим категорию
        loader.add_xpath('category', '//span[@class="i_yon"]/a/text()') #//div[@class = "bZFNy"]/span/span/a
        # автор фотографии
        loader.add_xpath('author', '//div[@class="TeuLI"]/a/text()')
        # название фотографии
        title = response.xpath('//div[@class="c489k UVQ9u nKDrT"]/h1/text()').get()
        if title:
            loader.add_value('title', title)
        else:
            loader.add_value('title', 'no_information')
        # дата публикации
        loader.add_xpath('published_on', '//time/text()')

        # название камеры
        camera = response.xpath('//span[@class="i_yon"]/text()').get()
        if camera:
            loader.add_value('camera', camera)
        else:
            loader.add_value('camera', 'no_information')

        # список тэгов
        tags = response.xpath('//div[@class ="zDHt2 N9mmz"]/a/text()').getall()
        loader.add_value('tags', tags)

        # ссылка на полную картинку
        image_url = response.xpath('//div[@class = "WxXog"]/img/@src').get()
        loader.add_value('image_urls', image_url)

        yield loader.load_item()
