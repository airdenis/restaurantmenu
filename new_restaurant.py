from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant


def create_restaurant(restaurant_name):
    engine = create_engine('sqlite:///restaurantmenu.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    new_restaurant = Restaurant(name=restaurant_name)
    session.add(new_restaurant)
    session.commit()
    print('{} restaurant has been craeted'.format(restaurant_name))
    return
