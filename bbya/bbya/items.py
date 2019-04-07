from scrapy import Item, Field


class UserItem(Item):
    id = Field()
    name = Field()
    avatar_url = Field()
    avatar = Field()
    registration_date = Field()

class SectionItem(Item):
    id = Field()
    title = Field()

class ForumItem(Item):
    id = Field()
    title = Field()
    section_id = Field()

class TopicItem(Item):
    id = Field()
    title = Field()
    forum_id = Field()

class PostItem(Item):
    id = Field()
    # TODO
