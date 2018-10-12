from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def create_restaurant(restaurant_name):
    new_restaurant = Restaurant(name=restaurant_name)
    session.add(new_restaurant)
    session.commit()
    print('{} restaurant has been craeted'.format(restaurant_name))
    return


def reset_name(restaurant_id, new_name):
    restaurant_change = session.query(Restaurant).filter_by(
            id=restaurant_id
            ).one()
    if restaurant_change != []:
        restaurant_change.name = new_name
        session.add(restaurant_change)
        session.commit()
    return


def delete_restaurant(restaurant_id):
    restaurant_delete = session.query(Restaurant).filter_by(
            id=restaurant_id
            ).one()
    if restaurant_delete != []:
        session.delete(restaurant_delete)
        session.commit()
        return
