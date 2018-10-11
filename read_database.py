from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant


def get_restaurants():
    engine = create_engine('sqlite:///restaurantmenu.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    restaurants = session.query(Restaurant).all()

    results = []
    for restaurant in restaurants:
        results.append(restaurant)
    return results


if __name__ == '__main__':
    get_restaurants()
