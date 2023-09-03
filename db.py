import json
import logging
from datetime import datetime

from sqlalchemy import create_engine, DateTime, text, BigInteger, JSON

from sqlalchemy import Column, String


from sqlalchemy.orm import sessionmaker, declarative_base
import hashlib

logger = logging.getLogger(__name__)

engine = create_engine('postgresql://postgres:123456@db:5432/postgres')
Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'

    user_id = Column(BigInteger, primary_key=True)
    user_tg_name = Column(String)
    user_key = Column(String)
    access_key = Column(String)
    user_balance = Column(BigInteger)
    chat_id = Column(BigInteger)
    registry_datetime = Column(DateTime)



    @classmethod
    def add_user_key(cls, user_id, user_tg_name):
        hash_object = hashlib.sha256(f"{user_id}{user_tg_name}".encode())
        hash_digest = hash_object.hexdigest()
        short_key = hash_digest[:8]
        return short_key

    @classmethod
    def find_user_by_key(cls, access_key):
        logger.info(access_key)
        user = session.query(Users).filter_by(user_key=access_key).first()
        if user:
            return [user.user_id, user.user_tg_name, user.user_key, user.registry_datetime]
        else:
            return None

    @classmethod
    def add_user(cls, user_id, user_tg_name, access_key, user_balance, chat_id, registry_datetime):
        logger.info("Trying to save user.")
        new_user = Users(user_id=user_id, user_tg_name=user_tg_name, user_key=cls.add_user_key(user_id, user_tg_name),
                         access_key=access_key, user_balance=user_balance, chat_id=chat_id,
                         registry_datetime=registry_datetime)
        session.add(new_user)
        session.commit()
        logging.info("User successfully saved!")

    @classmethod
    def get_user(cls, user_id):
        user = session.query(Users).filter_by(user_id=user_id).first()
        if user:
            return [user.user_id, user.user_tg_name, user.user_key, user.access_key, user.user_balance, user.chat_id,
                    user.registry_datetime]
        else:
            return None


    @classmethod
    def update_access_key(cls, user_id, access_key):
        user = session.query(Users).filter_by(user_id=user_id).first()
        if user:
            user.access_key = access_key
            session.commit()
            logger.info("User_key updated successfully!")
        else:
            logger.warning("User not found.")

    @classmethod
    def referral_bonus(cls, access_key):
        referrer = session.query(Users).filter_by(user_key=access_key).first()
        if referrer:
            referral_bonus_points = 10
            referrer.user_balance += referral_bonus_points
            session.commit()
            logger.info(f"Referral bonus of {referral_bonus_points} points added to user {referrer.user_id} balance.")
        else:
            logger.warning("Referrer not found.")







class Items(Base):
    __tablename__ = 'items'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    item = Column(String)
    item_url = Column(String)
    user_id = Column(String)
    user_tg_name = Column(String)
    item_details = Column(String)
    item_price = Column(String)
    item_quantity = Column(BigInteger)
    item_photo = Column(String)
    registry_datetime = Column(DateTime)

    @classmethod
    def _construct_item_list(cls, item_data):
        logger.info(f"You are in _construct_item_list")
        if type(item_data) is list:
            logger.info(f"if type(item_data) is list: ")
            item_list = [{
                "id": str(i.id),
                "item": i.item,
                "item_url": i.item_url,
                "user_id": i.user_id,
                "user_tg_name": i.user_tg_name,
                "item_details": i.item_details,
                "item_price": i.item_price,
                "item_quantity": i.item_quantity,
                "item_photo": i.item_photo,
                "registry_datetime": i.registry_datetime
            } for i in item_data]
            sorted_item_list = sorted(item_list, key=lambda x: x["item"])
            logger.info(f"sorted_item_list: {sorted_item_list} ")
            return sorted_item_list
        else:
            logger.info(f"else: ")
            item_list = {
                "id": str(item_data.id),
                "item": item_data.item,
                "item_url": item_data.item_url,
                "user_id": item_data.user_id,
                "user_tg_name": item_data.user_tg_name,
                "item_details": item_data.item_details,
                "item_price": item_data.item_price,
                "item_quantity": item_data.item_quantity,
                "item_photo": item_data.item_photo,
                "registry_datetime": item_data.registry_datetime
            }
            logger.info(f"item_list: {item_list} ")
            return item_list


    @classmethod
    def add_item(cls, item, item_url, user_id, user_tg_name, item_details, item_price, item_quantity, item_photo, registry_datetime):
        logger.info("Trying to save item.")

        new_item = Items(item=item, item_url=item_url, user_id=user_id, user_tg_name=user_tg_name, item_details=item_details,
                         item_price=item_price, item_quantity=item_quantity, item_photo=item_photo,
                         registry_datetime=registry_datetime)
        session.add(new_item)
        session.commit()
        logger.info("Item successfully saved!")
    @classmethod
    def get_items(cls):
        logger.info("Trying to get all items")
        item_data = session.query(Items).all()
        if item_data:
            sorted_item_list = cls._construct_item_list(item_data)
            logger.info("All items were extracted")
            return sorted_item_list
        else:
            return None

    @classmethod
    def delete_item(cls, item):
        logger.info("Trying to delete item.")
        item_to_delete = session.query(Items).filter_by(item=item).first()

        if item_to_delete:
            session.delete(item_to_delete)
            session.commit()
            logger.info("Item successfully deleted!")
        else:
            logger.warning("Item not found.")
            return None

    @classmethod
    def get_items_by_letters(cls, first_letters):
        logger.info(f"Trying to get items by first letter: {first_letters}")
        item_data = session.query(Items).filter(Items.item.ilike(f"%{first_letters}%")).all()
        logger.info(f"item_data: {item_data}")
        if item_data:
            sorted_item_list = cls._construct_item_list(item_data)
            logger.info(f"Items by {len(first_letters)} letter(s) were extracted")
            logger.info(f"sorted_item_list: {sorted_item_list}")
            return sorted_item_list
        else:
            logger.info("No items found for the given first letter.")
            return None

    @classmethod
    def get_item_by_id(cls, item_id):
        logger.info(f"Trying to get item with id: {item_id}")
        item_data = session.query(Items).filter_by(id=item_id).first()
        logger.info(f"item_data: {item_data}")
        if item_data:
            sorted_item_list = cls._construct_item_list(item_data)
            logger.info(f"Item with id {item_id} was found")
            return sorted_item_list
        else:
            logger.info(f"No item found with id {item_id}.")
            return None

    @classmethod
    def subtract_quantity(cls, item_id, quantity_to_subtract):
        item_to_update = session.query(Items).filter_by(id=item_id).first()
        if item_to_update:
            item_to_update.item_quantity -= quantity_to_subtract
            session.commit()
            logger.info(
                f"Subtracted {quantity_to_subtract} from item with id {item_id}. New quantity: {item_to_update.item_quantity}")
        else:
            logger.info(f"No item found with id {item_id}.")






Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
session.commit()





async def shorten_url(url):
    hash_object = hashlib.sha256(url.encode())
    hash_digest = hash_object.hexdigest()
    short_url = hash_digest[:8]
    return short_url



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





# g = session.query(Users).all()
#print(Users.get_user(683497406))





# __table_args__ = {'schema': 'links'}
#save_link('121313', 'http://link.com')


#print(*[[i.id, i.filetype, i.option, i.user_id, i.user_name, i.datetime] for i in session.query(File).all()], sep='\n')









# del_table('files')
#g = [[i.datetime, i.filename] for i in session.query(File).all()]
#print(len(g), *g, sep='\n')







