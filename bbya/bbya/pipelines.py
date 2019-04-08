import urllib, os
from scrapy import Item, Spider
from scrapy.exceptions import DropItem
from .items import UserItem, SectionItem, ForumItem, TopicItem, PostItem
from pony import orm
from pony.orm import db_session


class UniqueIdPipeline(object):

    def __init__(self):
        self.items = dict() # item class => item ids list
    
    def process_item(self, item: Item, spider: Spider):
        if 'id' not in item:
            return item
        
        key = str(type(item))
        id = int(item['id'][0] if type(item['id']) is list else item['id'])
        
        if key not in self.items:
            self.items[key] = set()
        
        if id not in self.items[key]:
            self.items[key].add(id)
            return item
        else:
            raise DropItem()


DB_FILENAME = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data.sqlite'))
class DBSavePipeline(object):
    
    def __init__(self):
        db = orm.Database()
        db = orm.Database()
        db.bind(provider='sqlite', filename=DB_FILENAME, create_db=True)

        class User(db.Entity):
            id = orm.PrimaryKey(int)
            name = orm.Required(str)
            avatar_url = orm.Optional(str)
            avatar = orm.Optional(bytes)
            registration_date = orm.Required(str)
            posts = orm.Set(lambda: Post)
        
        class Section(db.Entity):
            id = orm.PrimaryKey(int)
            title = orm.Required(str)
            forums = orm.Set(lambda: Forum)
        
        class Forum(db.Entity):
            id = orm.PrimaryKey(int)
            title = orm.Required(str)
            section = orm.Required(Section)
            topics = orm.Set(lambda: Topic)
        
        class Topic(db.Entity):
            id = orm.PrimaryKey(int)
            title = orm.Required(str)
            forum = orm.Required(Forum)
            posts = orm.Set(lambda: Post)
        
        class Post(db.Entity):
            id = orm.PrimaryKey(int)
            topic = orm.Required(Topic)
            number = orm.Required(int)
            date = orm.Required(int)
            author = orm.Required(User)
            text = orm.Required(str)
        
        db.generate_mapping(create_tables=True)
        orm.set_sql_debug(True)
        
        self.User = User
        self.Section = Section
        self.Forum = Forum
        self.Topic = Topic
        self.Post = Post
        self._db = db
    
    @db_session
    def process_item(self, item: Item, spider: Spider):
        if type(item) is UserItem:
            if 'avatar_url' in item:
                avatar_url = item['avatar_url'][0]
                if avatar_url[0] == '/':
                    avatar_url = avatar_url[1:]
                avatar_url = 'http://mc.bbcity.ru/' + avatar_url
                
                avatar_response = urllib.request.urlopen(avatar_url)
                avatar = avatar_response.read()

                self.User(
                    id=int(item['id'][0]),
                    name=item['name'][0], 
                    avatar_url=item['avatar_url'][0], 
                    avatar=avatar,
                    registration_date=item['registration_date'][0])
                orm.commit()
            else:
                self.User(
                    id=int(item['id'][0]),
                    name=item['name'][0],
                    registration_date=item['registration_date'][0])
                orm.commit()
        elif type(item) is SectionItem:
            self.Section(
                id=int(item['id']),
                title=item['title']
            )
            orm.commit()
        elif type(item) is ForumItem:
            self.Forum(
                id=int(item['id']),
                title=item['title'],
                section=int(item['section_id'])
            )
            orm.commit()
        elif type(item) is TopicItem:
            self.Topic(
                id=int(item['id']),
                title=item['title'],
                forum=int(item['forum_id'])
            )
            orm.commit()
        elif type(item) is PostItem:
            self.Post(
                id=int(item['id']),
                topic=int(item['topic']),
                number=int(item['number']),
                date=int(item['date']),
                author=int(item['author']),
                text=str(item['text'])
            )
            orm.commit()
        
        return item