from scrapy.pipelines.images import ImagesPipeline
import hashlib
from pathlib import Path

class CustomImagesPipeline(ImagesPipeline):
    #кастомизируем название файла с картинкой
    def file_path(self, request, response=None, info=None, *, item=None):
        image_guid = hashlib.sha1(request.url.encode()).hexdigest()
        file_name = f"{item['title']}-{image_guid}.jpg"
        item['file_name'] = file_name
        return file_name


