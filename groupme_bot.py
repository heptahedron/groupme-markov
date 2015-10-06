# vim:sw=4 ts=4
import http.server
import urllib.request
import urllib.parse
import json

api_url = 'https://api.groupme.com/v3'

class GroupmeBot:

    def __init__(self, bot_id):
        self.bot_id = bot_id

        class GroupmeMsgHandler(http.server.BaseHTTPRequestHandler):
            def do_POST(self2):
                req_str = self2.rfile.read().decode('utf-8')
                req_json = json.loads(req_str)
                sender = (req_json['name'], req_json['sender_id'])
                msg = req_json['text']
                if not req_json['sender_type'] == 'bot':
                    self.msg_received(sender, msg)

                print('Data posted: {}'.format(req_str))

        self.req_handler = GroupmeMsgHandler

    def msg_received(self, sender, msg):
        self.say('{}, your user id is {}'.format(sender[0], sender[1]))

    def listen(self, address='', port=80, server_class=http.server.HTTPServer):
        server_address = (address, port)
        httpd = server_class(server_address, self.req_handler)
        httpd.serve_forever()

    def say(self, msg):
        print(msg, self.bot_id)
        urllib.request.urlopen(
            '{api_url}/bots/post'.format(api_url=api_url),
            urllib.parse.urlencode({
                'bot_id': self.bot_id,
                'text': msg
            }).encode('utf-8')
        )


if __name__ == '__main__':
    b = GroupmeBot('a390b55c0ae2a7ea7fd8249b46')
    b.listen()
