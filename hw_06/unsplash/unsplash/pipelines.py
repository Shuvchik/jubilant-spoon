from scrapy.pipelines.images import ImagesPipeline
import hashlib


class CustomImagesPipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None, *, item=None):
        image_guid = hashlib.sha1(request.url.encode()).hexdigest()
        return f"{item['title']}-{image_guid}.jpg"
