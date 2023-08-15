# import logging
# import os
#
# import dropbox
#
#
#
# logger = logging.getLogger(__name__)
#
# class DropboxUploader:
#     def __init__(self):
#         self.dbx = dropbox.Dropbox(os.getenv("DROPBOX_TOKEN"))
#
#     def upload_bytes(self, file_bytes, dropbox_path):
#         try:
#             self.dbx.files_upload(file_bytes, dropbox_path)
#             logger.info("File successfully uploaded to Dropbox")
#         except dropbox.exceptions.ApiError as e:
#             logger.info(f"An error occurred while uploading: {e.user_message_text}")
#
#
#     def get_shared_link(self, dropbox_path):
#         try:
#             link = self.dbx.sharing_create_shared_link(dropbox_path).url
#             return link
#         except dropbox.exceptions.ApiError as e:
#             if e.error.is_shared_link_already_exists():
#                 links = self.dbx.sharing_list_shared_links(dropbox_path).links
#                 if links:
#                     return links[0].url
#             return None


