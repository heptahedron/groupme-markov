# vim:sw=4 ts=4
import re
import http.server
import json
from collections import namedtuple

class GroupmeBotServer:
    
    # cmd_regex = '^(\S+?)[:,]?\s+(.*)$'
    Sender = namedtuple('Sender', ['alias', 'sender_id'])

    def __init__(self, bots=[]):
        self.bots = bots

        class GroupmeMsgHandler(http.server.BaseHTTPRequestHandler):
            def do_POST(self2):
                req_str = self2.rfile.read().decode('utf-8')
                req_json = json.loads(req_str)

                group_id = req_json['group_id']
                sender = Sender(req_json['name'], req_json['sender_id'])
                msg = req_json['text']

                if not req_json['sender_type'] == 'bot':
                    self.process_message(group_id, sender, msg)

        self.req_handler = GroupmeMsgHandler

    def process_message(self, group_id, sender, msg):
        print('{} ({}) in group {}:\n{}'.format(
            sender[0], sender[1], group_id, msg))
        for bot in self.bots:
            if bot.group_id == group_id:
                bot.msg_received(sender, msg)
                if cmd_match:
                    if cmd_match.group(1) == bot.name:
                        bot.cmd_received(sender, cmd_match.group(2))


    def register_bot(self, bot):
        self.bots.append(bot)

    def listen(self, address='', port=80, server_class=http.server.HTTPServer):
        if not len(self.bots) > 0:
            print('No bots to listen with!')
            return False
        server_address = (address, port)
        httpd = server_class(server_address, self.req_handler)
        httpd.serve_forever()
