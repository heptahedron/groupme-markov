# vim:sw=4 ts=4
import urllib.request
import urllib.parse

api_url = 'https://api.groupme.com/v3'

class GroupmeBot:

    def __init__(self, group_id, bot_id, name):
        self.group_id = group_id
        self.bot_id = bot_id
        self.name = name

    def msg_received(self, sender, msg):
        pass
        # print('{} ({}): {}'.format(sender[0], sender[1], msg))

    def cmd_received(self, sender, cmd):
        pass
        # print('Command received from {} ({}): {}'.format(
        #     sender[0], sender[1], cmd))

    def say(self, msg):
        print('{} ({}) in group {}: {}'.format(
            self.name, self.bot_id, self.group_id, msg))
        urllib.request.urlopen(
            '{api_url}/bots/post'.format(api_url=api_url),
            urllib.parse.urlencode({
                'bot_id': self.bot_id,
                'text': msg
            }).encode('utf-8')
        )

