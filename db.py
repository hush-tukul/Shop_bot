import json
import logging
from datetime import datetime

from sqlalchemy import create_engine, DateTime, text, BigInteger, JSON

from sqlalchemy import Column, String


from sqlalchemy.orm import sessionmaker, declarative_base
import hashlib



engine = create_engine('postgresql://postgres:123456@db:5432/postgres')
Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'

    user_id = Column(BigInteger, primary_key=True)
    user_tg_name = Column(String)
    user_key = Column(String)
    access_key = Column(String)
    user_balance = Column(BigInteger)
    registry_datetime = Column(DateTime)



    @classmethod
    def add_user_key(cls, user_id, user_tg_name):
        hash_object = hashlib.sha256(f"{user_id}{user_tg_name}".encode())
        hash_digest = hash_object.hexdigest()
        short_key = hash_digest[:8]
        return short_key

    @classmethod
    def find_user_by_key(cls, access_key):
        logging.info(access_key)
        user = session.query(Users).filter_by(user_key=access_key).first()
        if user is not None:
            return [user.user_id, user.user_tg_name, user.user_key, user.registry_datetime]
        else:
            return None

    @classmethod
    def add_user(cls, user_id, user_tg_name, access_key, user_balance, registry_datetime):
        logging.info("Trying to save user.")
        new_user = Users(user_id=user_id, user_tg_name=user_tg_name, user_key=cls.add_user_key(user_id, user_tg_name),
                         access_key=access_key, user_balance=user_balance, registry_datetime=registry_datetime)
        session.add(new_user)
        session.commit()
        logging.info("User successfully saved!")

    @classmethod
    def get_user(cls, user_id):
        user = session.query(Users).filter_by(user_id=user_id).first()
        if user is not None:
            return [user.user_id, user.user_tg_name, user.user_key, user.access_key, user.user_balance, user.registry_datetime]
        else:
            return None

    @classmethod
    def update_access_key(cls, user_id, access_key):
        user = session.query(Users).filter_by(user_id=user_id).first()
        if user:
            user.access_key = access_key
            session.commit()
            logging.info("User_key updated successfully!")
        else:
            logging.warning("User not found.")

    @classmethod
    def referral_bonus(cls, access_key):
        referrer = session.query(Users).filter_by(user_key=access_key).first()
        if referrer:
            referral_bonus_points = 10
            referrer.user_balance += referral_bonus_points
            session.commit()
            logging.info(f"Referral bonus of {referral_bonus_points} points added to user {referrer.user_id} balance.")
        else:
            logging.warning("Referrer not found.")



# class Reflink(Base):
#     __tablename__ = 'links'
#
#     link_id = Column(String, primary_key=True)
#     user_id = Column(BigInteger)
#     orig_link = Column(String)
#     datetime = Column(DateTime)
#
#     @classmethod
#     def save_link(cls, user_id, link, link_id):
#         try:
#             # Check if a record with the given link_id already exists
#             existing_link = session.query(Reflink).filter_by(user_id=user_id, orig_link=link).first()
#             if existing_link:
#                 logging.info("Link already exists!")
#                 return 'exist'
#
#             time = datetime.now()
#             # Create a new Reflink object with the provided values
#             new_link = Reflink(link_id=link_id, user_id=user_id, orig_link=link, datetime=time)
#
#             # Add the new_link object to the session
#             session.add(new_link)
#
#             # Commit the changes to the database
#             session.commit()
#             logging.info("Link saved successfully!")
#         except Exception as e:
#             # Handle any exceptions that may occur during the saving process
#             logging.info("An error occurred while saving the link:", str(e))
#             session.rollback()
#
#     @classmethod
#     def get_original_link(cls, link_id):
#         logging.info("Trying to get orig_link")
#         try:
#             link = session.query(Reflink).filter_by(link_id=link_id).first()
#             if link:
#                 logging.info("Successfully get link")
#                 return link.orig_link
#             else:
#                 logging.info("No such link_id")
#                 return None
#         except Exception as e:
#             logging.error(f"An error occurred while retrieving the original link: {str(e)}")
#             return None
#
#
#     @classmethod
#     def get_original_link_by_user_id(cls, user_id, link_id):
#         logging.info("Trying to get orig_link")
#         try:
#             link = session.query(Reflink).filter_by(user_id=user_id, link_id=link_id).first()
#             if link:
#                 logging.info("Successfully get link")
#                 return link.orig_link
#             else:
#                 logging.info("No such link_id")
#                 return None
#         except Exception as e:
#             logging.error(f"An error occurred while retrieving the original link: {str(e)}")
#             return None
#
#     @classmethod
#     def get_user_links(cls, user_id):
#         logging.info("Trying to get user links")
#         try:
#             links = session.query(Reflink).filter_by(user_id=user_id).all()
#             if links:
#                 logging.info("Successfully retrieved user links")
#                 return [link.orig_link for link in links]
#             else:
#                 logging.info("No links found for the user")
#                 return None
#         except Exception as e:
#             logging.error(f"An error occurred while retrieving user links: {str(e)}")
#             return None
#
#     @classmethod
#     def replace_link(cls, user_id, old_link_id, new_link):
#         try:
#             logging.info(f"DB/replace_link: {old_link_id}")
#             # Check if a record with the given user_id and old_link exists
#             existing_link = session.query(Reflink).filter_by(user_id=user_id, link_id=old_link_id).first()
#             if existing_link:
#                 existing_link.orig_link = new_link  # Replace the original link with the new one
#                 session.commit()
#                 logging.info("Link replaced successfully!")
#                 return 'replaced'
#             else:
#                 logging.info("No such link found!")
#                 return 'not_found'
#         except Exception as e:
#             logging.error("An error occurred while replacing the link:", str(e))
#             session.rollback()
#
#     @classmethod
#     def delete_link(cls, user_id, link_id):
#         try:
#             # Check if a record with the given user_id and link exists
#             existing_link = session.query(Reflink).filter_by(user_id=user_id, link_id=link_id).first()
#             if existing_link:
#                 # Delete the existing link
#                 session.delete(existing_link)
#                 session.commit()
#                 logging.info("Link deleted successfully!")
#                 return 'deleted'
#             else:
#                 logging.info("No such link found!")
#                 return 'not_found'
#         except Exception as e:
#             logging.error("An error occurred while deleting the link:", str(e))
#             session.rollback()
#
#     @classmethod
#     def get_link_id(cls, link):
#         logging.info("Trying to get link_id")
#         try:
#             link_obj = session.query(Reflink).filter_by(orig_link=link).first()
#             if link_obj:
#                 logging.info("Successfully retrieved link_id")
#                 return link_obj.link_id
#             else:
#                 logging.info("No link_id found for the link")
#                 return None
#         except Exception as e:
#             logging.error(f"An error occurred while retrieving the link_id: {str(e)}")
#             return None
#
# class Users(Base):
#     __tablename__ = 'users'
#
#     user_id = Column(BigInteger, primary_key=True)
#     user_name = Column(String)
#     user_lang = Column(String)
#     registry_datetime = Column(DateTime)
#
#
#     @classmethod
#     def add_user(cls, user_id, user_name, user_lang, registry_datetime):
#         logging.info("Trying to save user.")
#         new_user = Users(user_id=user_id, user_name=user_name, user_lang=user_lang,
#                         registry_datetime=registry_datetime)
#         session.add(new_user)
#         session.commit()
#         logging.info("User successfully saved!")
#
#     @classmethod
#     def get_user(cls, user_id):
#         user = session.query(Users).filter_by(user_id=user_id).first()
#         if user is not None:
#             return [user.user_id, user.user_name, user.user_lang, user.registry_datetime]
#         else:
#             return None
#
#     @classmethod
#     def update_user_lang(cls, user_id, new_lang):
#         user = session.query(Users).filter_by(user_id=user_id).first()
#         if user:
#             user.user_lang = new_lang
#             session.commit()
#             logging.info("User language updated successfully!")
#         else:
#             logging.warning("User not found.")
#
# class Stat(Base):
#     __tablename__ = 'stat'
#     id = Column(BigInteger, primary_key=True, autoincrement=True)
#     link_id = Column(String)
#     client_ip = Column(String)
#     client_data = Column(JSON)
#     registry_datetime = Column(DateTime)
#
#     @classmethod
#     def set_client_data(self, data):
#         return json.dumps(dict(data))
#
#     @classmethod
#     def get_client_data(self):
#         return json.loads(self.client_data) if self.client_data else {}
#     @classmethod
#     def save_click(cls, link_id, client_ip, data, registry_datetime):
#         new_click = Stat(link_id=link_id, client_ip=client_ip, client_data=Stat.set_client_data(data), registry_datetime=registry_datetime)
#         session.add(new_click)
#         session.commit()
#         return "Click succesfully saved!"


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







