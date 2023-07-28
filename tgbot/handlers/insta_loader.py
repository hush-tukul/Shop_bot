import asyncio
import logging
import os

import email

import aiofiles
from imap_tools import MailBox
import re
import random

from instagrapi import Client


from run import mail, mail_pass


class InstaLogin:
    def __init__(self):
        self.cl = Client()

    def login(self):
        self.cl.load_settings('dump.json')
        self.cl.login(mail, mail_pass)



def get_msg() -> str:
    email_url = 'imap.poczta.onet.pl'
    regex= "\d{5}"

    with MailBox(email_url).login(mail, mail_pass, 'Społeczności') as mailbox:
        for msg in mailbox.fetch(limit=1, reverse=True):
            code = re.findall(regex, msg.subject)[0]
            return code


async def download_instagram_video(link, user_id, cl):
    try:
        logging.info('Inside downloading insta_video')
        cl.get_timeline_feed()
        media = cl.media_pk_from_url(link)
        logging.info(media)
        media_path = cl.video_download(media, folder=r"temp")

        # Convert the media file to bytes-like object
        async with aiofiles.open(media_path, 'rb') as file:
            file_data = await file.read()

        os.remove(media_path)
        return file_data

    except Exception as e:
        logging.info(e)






# def get_code_from_email(insta_login):
#     mail = imaplib.IMAP4_SSL("imap.gmail.com")
#     mail.login(gmail, gmail_pass)
#     mail.select("inbox")
#     result, data = mail.search(None, "(UNSEEN)")
#     assert result == "OK", "Error1 during get_code_from_email: %s" % result
#     ids = data.pop().split()
#     for num in reversed(ids):
#         mail.store(num, "+FLAGS", "\\Seen")  # mark as read
#         result, data = mail.fetch(num, "(RFC822)")
#         assert result == "OK", "Error2 during get_code_from_email: %s" % result
#         msg = email.message_from_string(data[0][1].decode())
#         payloads = msg.get_payload()
#         if not isinstance(payloads, list):
#             payloads = [msg]
#         code = None
#         for payload in payloads:
#             body = payload.get_payload(decode=True).decode()
#             if "<div" not in body:
#                 continue
#             match = re.search(">([^>]*?({u})[^<]*?)<".format(u=insta_login), body)
#             if not match:
#                 continue
#             print("Match from email:", match.group(1))
#             match = re.search(r">(\d{6})<", body)
#             if not match:
#                 print('Skip this email, "code" not found')
#                 continue
#             code = match.group(1)
#             if code:
#                 return code
#     return False






# async def download_instagram_video(link, user_id):
#     # Create an instance of Instaloader
#     loader = instaloader.Instaloader()
#     loader.save_session_to_file()
#     loader.context.get_json(link, )
#     video_path = fr'C:\Users\hush-\PycharmProjects\new_abilities\temp'
#
#     post = instaloader.Post.from_shortcode(loader.context, link.split("/")[-2])
#     loader.download_post(post, target=video_path)
#     file_name = post.url.split("/")[-1]  # Extract the file name from the post URL
#
#     file_path = os.path.join(video_path, file_name)
#     with open(file_path, 'rb') as file:
#         video_bytes = file.read()
#
#     return video_bytes



# # Open the compressed file
# with lzma.open('2023-04-17_05-43-34_UTC.json.xz', 'rb') as file:
#     # Read the decompressed data
#     decompressed_data = file.read()
#
# # Decode the decompressed data as a string
# json_data = decompressed_data.decode('utf-8')
#
# # Parse the JSON data
# parsed_json = json.loads(json_data)
#
# # Now you can work with the JSON data as a Python object
# # For example, print the parsed JSON data
# print(parsed_json)