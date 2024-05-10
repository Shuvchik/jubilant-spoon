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
from ..items import UnplashWithCategoriesItem
from itemloaders.processors import MapCompose


class UnsplashSpiderSpider(CrawlSpider):
    name = "unsplash_spider"
    allowed_domains = ["unsplash.com"]
    start_urls = ["https://unsplash.com"]

    # Получаем ссылки на страницы категорий
    rules = (
        # ссылки на категории картинок
        Rule(LinkExtractor(restrict_xpaths='//a[@class="oaSYM ZR5jm"]')),
        # ссылки на страницы картинок
        Rule(LinkExtractor(restrict_xpaths='//div[@class="aD8H3"]/a'), callback="parse_item", follow=True)
    )

    def parse_item(self, response):
        loader = ItemLoader(item=UnplashWithCategoriesItem(), response=response)
        loader.default_input_processor = MapCompose(str.strip)

        #категория картинки
        category = response.xpath('//span[@class="i_yon"]/a/text()').get()
        if category:
            loader.add_value('category', category)
        else:
            loader.add_value('category', 'no_information')

        # автор фотографии
        loader.add_xpath('author', '//div[@class="TeuLI"]/a/text()')

        # название фотографии
        loader.add_xpath('title', '//div[@class="c489k UVQ9u nKDrT"]/h1/text()')

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
