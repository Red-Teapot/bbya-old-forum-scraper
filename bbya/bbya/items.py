from scrapy import Item, Field


class UserItem(Item):
    id = Field()
    name = Field()
    avatar_url = Field()
    avatar = Field()
    registration_date = Field()


