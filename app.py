import logging
import os
from datetime import datetime
from urllib.parse import urlparse, parse_qs
from quart import request, redirect, Quart, send_file

logger = logging.getLogger(__name__)


app = Quart(__name__)

@app.route('/download/<filename>', methods=['GET'])
async def handle_request(filename):
    logger.info(filename)
    file_path = os.path.join('/usr/src/app/tg_bot/tgbot/keyboards/photos/', filename)

    if os.path.exists(file_path):
        return await send_file(file_path, as_attachment=True)
    else:
        return "File not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)



#http://<адрес_вашего_контейнера>:5000/download/file_name
#http://172.19.0.5:5000/download/file_name

# parsed_url = urlparse(request.url)
    # query_params = parse_qs(parsed_url.query)
    # link_id = query_params.get('link_id', [0])[0]
    # client_ip = request.remote_addr
    # client_data = request.headers     # Get the client's IP address
    # reg_time = datetime.now()
    # if link_id == 0:
    #     return "<h1>Please stand by. All Jedi are busy.</h1>" \
    #            "<h1><p>\nPlease write to Our support in TrackerBot menu.</p></h1>"
    #
    # try:
    #     link = Reflink.get_original_link(link_id)
    #     if link is None:
    #         return "Invalid link_id", 400
    #     #Stat.save_click(link_id, client_ip, client_data, reg_time)
    #     return redirect(link)
    # except Exception as e:
    #     logging.error(f"An error occurred: {str(e)}")
    #     return "An error occurred", 500