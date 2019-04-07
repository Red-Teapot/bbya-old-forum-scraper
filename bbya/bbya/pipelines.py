import urllib, os
from scrapy import Item, Spider
from .items import UserItem
from pony import orm
from pony.orm import db_session


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
        
        db.generate_mapping(create_tables=True)
        orm.set_sql_debug(True)
        
        self.User = User
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