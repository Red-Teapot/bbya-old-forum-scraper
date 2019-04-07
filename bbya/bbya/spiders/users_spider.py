import urllib
from scrapy import Spider
from scrapy.http import Response
from scrapy.loader import ItemLoader
from ..items import UserItem


class UsersSpider(Spider):
    name = 'users'
    start_urls = ['http://mc.bbcity.ru/userlist.php']

    def parse(self, response: Response):
        for row in response.xpath('//div[@class="usertable"]//div[@class="container"]//tbody/tr'):
            profile_url = row.xpath('td[@class="tcl"]//a/@href').get()
            yield response.follow(profile_url, callback=self.parse_profile)
        
        next_page_url = response.xpath('//div[@class="pagelink"]/a[@class="next"]/@href').get()
        if next_page_url:
            yield response.follow(next_page_url, callback=self.parse)
    
    def parse_profile(self, response: Response):
        query = urllib.parse.urlparse(response.url).query
        id = int(urllib.parse.parse_qs(query)['id'][0])

        l = ItemLoader(item=UserItem(), response=response)
        l.add_value('id', id)
        l.add_xpath('name', '//div[@id="viewprofile"]//td[@id="profile-left"]/li[@id="profile-name"]/strong/text()')
        l.add_xpath('avatar_url', '//div[@id="viewprofile"]//td[@id="profile-left"]//img//@src')
        l.add_xpath('registration_date', '//div[@id="viewprofile"]//td[@id="profile-right"]//li/span[text()="Зарегистрирован:"]/following-sibling::strong/text()')
        return l.load_item()

