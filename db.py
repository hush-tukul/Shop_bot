import json
import logging
from datetime import datetime

from sqlalchemy import create_engine, DateTime, text, BigInteger, JSON

from sqlalchemy import Column, String


from sqlalchemy.orm import sessionmaker, declarative_base
import hashlib

from run import db_login, db_password, db_host_name, db_name

engine = create_engine(f'postgresql://{db_login}:{db_password}@{db_host_name}:5432/{db_name}')
Base = declarative_base()




class Reflink(Base):
    __tablename__ = 'links'

    link_id = Column(String, primary_key=True)
    user_id = Column(BigInteger)
    orig_link = Column(String)
    datetime = Column(DateTime)

    @classmethod
    def save_link(cls, user_id, link, link_id):
        try:
            # Check if a record with the given link_id already exists
            existing_link = session.query(Reflink).filter_by(user_id=user_id, orig_link=link).first()
            if existing_link:
                logging.info("Link already exists!")
                return 'exist'

            time = datetime.now()
            # Create a new Reflink object with the provided values
            new_link = Reflink(link_id=link_id, user_id=user_id, orig_link=link, datetime=time)

            # Add the new_link object to the session
            session.add(new_link)

            # Commit the changes to the database
            session.commit()
            logging.info("Link saved successfully!")
        except Exception as e:
            # Handle any exceptions that may occur during the saving process
            logging.info("An error occurred while saving the link:", str(e))
            session.rollback()

    @classmethod
    def get_original_link(cls, link_id):
        logging.info("Trying to get orig_link")
        try:
            link = session.query(Reflink).filter_by(link_id=link_id).first()
            if link:
                logging.info("Successfully get link")
                return link.orig_link
            else:
                logging.info("No such link_id")
                return None
        except Exception as e:
            logging.error(f"An error occurred while retrieving the original link: {str(e)}")
            return None


    @classmethod
    def get_original_link_by_user_id(cls, user_id, link_id):
        logging.info("Trying to get orig_link")
        try:
            link = session.query(Reflink).filter_by(user_id=user_id, link_id=link_id).first()
            if link:
                logging.info("Successfully get link")
                return link.orig_link
            else:
                logging.info("No such link_id")
                return None
        except Exception as e:
            logging.error(f"An error occurred while retrieving the original link: {str(e)}")
            return None

    @classmethod
    def get_user_links(cls, user_id):
        logging.info("Trying to get user links")
        try:
            links = session.query(Reflink).filter_by(user_id=user_id).all()
            if links:
                logging.info("Successfully retrieved user links")
                return [link.orig_link for link in links]
            else:
                logging.info("No links found for the user")
                return None
        except Exception as e:
            logging.error(f"An error occurred while retrieving user links: {str(e)}")
            return None

    @classmethod
    def replace_link(cls, user_id, old_link_id, new_link):
        try:
            logging.info(f"DB/replace_link: {old_link_id}")
            # Check if a record with the given user_id and old_link exists
            existing_link = session.query(Reflink).filter_by(user_id=user_id, link_id=old_link_id).first()
            if existing_link:
                existing_link.orig_link = new_link  # Replace the original link with the new one
                session.commit()
                logging.info("Link replaced successfully!")
                return 'replaced'
            else:
                logging.info("No such link found!")
                return 'not_found'
        except Exception as e:
            logging.error("An error occurred while replacing the link:", str(e))
            session.rollback()

    @classmethod
    def delete_link(cls, user_id, link_id):
        try:
            # Check if a record with the given user_id and link exists
            existing_link = session.query(Reflink).filter_by(user_id=user_id, link_id=link_id).first()
            if existing_link:
                # Delete the existing link
                session.delete(existing_link)
                session.commit()
                logging.info("Link deleted successfully!")
                return 'deleted'
            else:
                logging.info("No such link found!")
                return 'not_found'
        except Exception as e:
            logging.error("An error occurred while deleting the link:", str(e))
            session.rollback()

    @classmethod
    def get_link_id(cls, link):
        logging.info("Trying to get link_id")
        try:
            link_obj = session.query(Reflink).filter_by(orig_link=link).first()
            if link_obj:
                logging.info("Successfully retrieved link_id")
                return link_obj.link_id
            else:
                logging.info("No link_id found for the link")
                return None
        except Exception as e:
            logging.error(f"An error occurred while retrieving the link_id: {str(e)}")
            return None

class Users(Base):
    __tablename__ = 'users'

    user_id = Column(BigInteger, primary_key=True)
    user_name = Column(String)
    user_lang = Column(String)
    registry_datetime = Column(DateTime)


    @classmethod
    def add_user(cls, user_id, user_name, user_lang, registry_datetime):
        logging.info("Trying to save user.")
        new_user = Users(user_id=user_id, user_name=user_name, user_lang=user_lang,
                        registry_datetime=registry_datetime)
        session.add(new_user)
        session.commit()
        logging.info("User successfully saved!")

    @classmethod
    def get_user(cls, user_id):
        user = session.query(Users).filter_by(user_id=user_id).first()
        if user is not None:
            return [user.user_id, user.user_name, user.user_lang, user.registry_datetime]
        else:
            return None

    @classmethod
    def update_user_lang(cls, user_id, new_lang):
        user = session.query(Users).filter_by(user_id=user_id).first()
        if user:
            user.user_lang = new_lang
            session.commit()
            logging.info("User language updated successfully!")
        else:
            logging.warning("User not found.")

class Stat(Base):
    __tablename__ = 'stat'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    link_id = Column(String)
    client_ip = Column(String)
    client_data = Column(JSON)
    registry_datetime = Column(DateTime)

    @classmethod
    def set_client_data(self, data):
        return json.dumps(dict(data))

    @classmethod
    def get_client_data(self):
        return json.loads(self.client_data) if self.client_data else {}
    @classmethod
    def save_click(cls, link_id, client_ip, data, registry_datetime):
        new_click = Stat(link_id=link_id, client_ip=client_ip, client_data=Stat.set_client_data(data), registry_datetime=registry_datetime)
        session.add(new_click)
        session.commit()
        return "Click succesfully saved!"


#[[i.id, i.filetype, i.option, i.user_id, i.user_name, i.datetime] for i in session.query(File).all()]
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
session.commit()


async def shorten_url(url):
    hash_object = hashlib.sha256(url.encode())
    hash_digest = hash_object.hexdigest()
    short_url = hash_digest[:8]
    return short_url




# g = session.query(Users).all()
#print(Users.get_user(683497406))





# __table_args__ = {'schema': 'links'}
#save_link('121313', 'http://link.com')


#print(*[[i.id, i.filetype, i.option, i.user_id, i.user_name, i.datetime] for i in session.query(File).all()], sep='\n')









# del_table('files')
#g = [[i.datetime, i.filename] for i in session.query(File).all()]
#print(len(g), *g, sep='\n')












# def items(item: str):
#     g = {
#         'planets': [(i.planet_name, i.planet_name) for i in session.query(Planets).all()],
#         'passengers': [(i.passenger_name, i.passenger_name) for i in session.query(Passengers).all()],
#         'ships': [(i.ship_name, i.ship_name) for i in session.query(Ships).all()]
#
#     }
#     return g[item]
#
#
#
#
# def table_info(tablename: str, item = None):
#     pl = session.query(Planets).filter(Planets.planet_name == item).all()
#     ps = session.query(Passengers).filter(Passengers.passenger_name == item).all()
#     sh = session.query(Ships).filter(Ships.ship_name == item).all()
#
#     tables = {
#         'planets': {
#             False: '\n'.join([f"Space object: {i.planet_name}\nType: {i.planet_class}\nMain parameters: {i.parameters}\nAge (th.years): {i.age}"
#                              for i in session.query(Planets).all()]),
#             True: f"Planet name: {pl[0].planet_name}\nType: {pl[0].planet_class}\nMain parameters: {pl[0].parameters}\nAge (th.years): {pl[0].age}"
#             if session.query(exists().where(Planets.planet_name == item)).scalar() else 'No such planet in our database'
#             },
#         'passengers': {
#             False: '\n'.join([f"Passenger name: {i.passenger_name}\nMain data: {i.parameters}\nAge (years): {i.age}"
#                              for i in session.query(Passengers).all()]),
#             True: f"Passenger name: {ps[0].passenger_name}\nMain data: {ps[0].parameters}\nAge (years): {ps[0].age}"
#             if session.query(exists().where(Passengers.passenger_name == item)).scalar() else 'No such passenger in our database'
#         },
#         'ships': {
#             False: '\n'.join(
#                 [f"Ship name: {i.ship_name}\nShip class: {i.ship_class}\nMain parameter: {i.parameters}"
#                  for i in session.query(Ships).all()]),
#             True: f"Ship name: {sh[0].ship_name}\nShip class: {sh[0].ship_class}\nMain parameter: {sh[0].parameters}"
#             if session.query(
#                 exists().where(Ships.ship_name == item)).scalar() else 'No such ship in our database'
#         }
#         }
#     return tables[tablename][bool(item)]
#
#
#
# def del_table(table):
#     session.query(Planets).delete()
#     session.commit()
#
#
# def del_item(kind, item):
#     g = {
#         'planets': session.query(Planets).where(Planets.planet_name == item).delete(),
#         'passengers': session.query(Passengers).where(Passengers.passenger_name == item).delete(),
#         'ships': session.query(Ships).where(Ships.ship_name == item).delete(),
#     }
#     g[kind]
#     session.commit()
#
#
#
# def add_new_object(tablename, *args):
#     g = list(args)
#     if len(args) < 4:
#         g.append(None)
#     tables = {
#         'planets': Planets(
#             planet_name=g[0],
#             planet_class=g[1],
#             parameters=g[2],
#             age=g[3]
#         ),
#         'passengers': Passengers(
#             passenger_name=g[0],
#             parameters=g[1],
#             age=g[2]
#         ),
#         'ships': Ships(
#             ship_name=g[0],
#             ship_class=g[1],
#             parameters=g[2]
#         )
#     }
#     session.add(tables[tablename])
#     session.commit()



#add_new_object('planets', 'Tatooine', 'desert planet', "Homeland of person who had to fight evil Not to join it! And his kidness son.", 8)

#add_new_object('passengers', 'Luke Skywalker', 'experience - New Hope of Jedi kind - 83kg, height - 183cm, sex - man', 25)
#
#add_new_object('ships', 'Millennium Falcon', 'YT-series', "weight - 30 t. tons, length - 34 m, width - 25 m, height - 8 m")

#print(table_info('planets'))
#del_item('passengers', 'ps_Serg.Ripley')

# print(items('ships'))












