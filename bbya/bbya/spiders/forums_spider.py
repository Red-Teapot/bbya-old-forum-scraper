import urllib
from scrapy import Spider
from scrapy.http import Response
from scrapy.loader import ItemLoader
from ..items import SectionItem, ForumItem, TopicItem, PostItem


class ForumsSpider(Spider):
    name = 'forums'
    start_urls = ['http://mc.bbcity.ru']

    def __init__(self):
        self.forums = dict() # forum id -> section id
        self.topics = dict() # topic id -> forum id

    def parse(self, response: Response):
        for section in response.xpath('//div[@id="pun-main"]/div[@class="category"]'):
            section_id = int(section.xpath('@id').get()[len('pun-category'):])
            section_title = section.xpath('h2/span/text()').get()

            yield SectionItem(id=section_id, title=section_title)

            for forum in section.xpath('div[@class="container"]//div[@class="intd"]//h3'):
                forum_url = forum.xpath('a/@href').get()
                forum_url_query = urllib.parse.urlparse(forum_url).query
                forum_id = int(urllib.parse.parse_qs(forum_url_query)['id'][0])

                self.forums[forum_id] = section_id

                yield response.follow(forum_url, self.parse_forum)
    
    def parse_forum(self, response: Response):
        forum_url_query = urllib.parse.urlparse(response.url).query
        forum_id = int(urllib.parse.parse_qs(forum_url_query)['id'][0])
        forum_title = response.xpath('//div[@id="pun-main"]/h1/span/text()').get()

        section_id = self.forums[forum_id]

        yield ForumItem(id=forum_id, title=forum_title, section_id=section_id)

        for topic in response.xpath('//div[@class="forum"]/div[@class="container"]//tbody//tr/td[@class="tcl"]/div[@class="tclcon"]'):
            topic_url = topic.xpath('a/@href').get()
            topic_url_query = urllib.parse.urlparse(topic_url).query
            topic_id = int(urllib.parse.parse_qs(topic_url_query)['id'][0])

            self.topics[topic_id] = forum_id

            yield response.follow(topic_url, self.parse_topic)
        
        next_page_url = response.xpath('//div[@class="pagelink"]/a[@class="next"]/@href').get()
        if next_page_url:
            yield response.follow(next_page_url, callback=self.parse_forum)

    def parse_topic(self, response: Response):
        topic_url_query = urllib.parse.urlparse(response.url).query
        topic_id = int(urllib.parse.parse_qs(topic_url_query)['id'][0])

        forum_id = self.topics[topic_id]

        topic_title = response.xpath('//div[@id="pun-main"]/h1/span/text()').get()

        yield TopicItem(id=topic_id, title=topic_title, forum_id=forum_id)

        self.logger.debug('Parsing topic %d %s from %d', topic_id, topic_title, forum_id)