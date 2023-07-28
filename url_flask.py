
import logging

from urllib.parse import urlparse, urlencode, urlunparse




'''-----------------CLASS VERSION-----------------'''
class UTMTracker:
    def __init__(self, link_id):
        self.link_id = link_id

    def add_link_id(self):
        g = f"http://127.0.0.1:5000/{self.link_id}"
        return g
        # parsed_url = urlparse('http://127.0.0.1:5000')
        # params = {
        #     'a': self.link_id,
        # 
        # }
        # 
        # # Build the updated URL with UTM parameters
        # updated_query_params = urlencode(params)
        # updated_url = urlunparse((
        #     parsed_url.scheme,
        #     parsed_url.netloc,
        #     parsed_url.path,
        #     parsed_url.params,
        #     updated_query_params,
        #     parsed_url.fragment
        # ))
        # logging.info(updated_url)
        # return updated_url







