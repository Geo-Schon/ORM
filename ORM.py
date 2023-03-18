import sqlalchemy
from sqlalchemy.orm import sessionmaker
import json

from models import create_tables, Publisher, Sale, Book, Stock, Shop

DSN = 'postgresql://postgres:2450200@localhost:5432/postgres'

engine = sqlalchemy.create_engine(DSN)

Session = sessionmaker(bind=engine)
session = Session()

create_tables(engine)

with open('DataBaseBooks.json', 'r') as db:
    data = json.load(db)

for line in data:
    method = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[line['model']]
    session.add(method(id=line['pk'], **line.get('fields')))

session.commit()

pub_name = input('Введите название издательства издательства: ')
# pub_id = input('Введите идентификатор издательства:')

def get_shop_by_publisher(publisher_name=None, publisher_id=None):

    if publisher_name is not None and publisher_id is None:
        for c in session.query(Shop.name).join(Stock.shop).join(Stock.book).join(Book.publisher).filter(
                publisher_name == Publisher.name):
            print(c)

    # elif publisher_id is not None and publisher_name is None:
    #     for c in session.query(Shop.name).join(Stock.shop).join(Stock.book).join(Book.publisher).filter(
    #             int(publisher_id) == Publisher.id):
    #         print(c)

    # elif publisher_name is not None and publisher_id is not None:
    #     for c in session.query(Shop.name).join(Stock.shop).join(Stock.book).join(Book.publisher).filter(
    #             publisher_name == Publisher.name, Publisher.id == int(publisher_id)):
    #         print(c)

session.close()
