# vim:sw=4 ts=4 sts=4
from sys import argv, exit
import urllib.request
import urllib.parse
import json

api_url = 'https://api.groupme.com/v3'

class GroupmeMsgFetcher:

    def __init__(self, group_id, token):
        self.group_id = group_id
        self.token = token
        self.msg_queue = []
        self.total_count = 0
        self.processed = 0

    def dump(self, filename):
        self._init_queue()
        try:
            while not self._done():
                self._enqueue()
        except urllib.request.HTTPError:
            pass

        with open(filename, 'w') as f:
            json.dump(self.msg_queue, f)

    def _create_req(self, d={}):
        d['token'] = self.token
        d = urllib.parse.urlencode(d)
        url = '{}/groups/{}/messages?{}'.format(
            api_url, self.group_id, d)
        req = urllib.request.Request(url)

        return req

    def _init_queue(self):
        req = self._create_req({'limit':100})
        res_text = urllib.request.urlopen(req).read().decode('utf-8')
        res_json = json.loads(res_text)
        if not res_json['response']:
            raise Exception('Could not fetch messages')

        self.msg_queue = res_json['response']['messages']
        self.total_count = res_json['response']['count']

    def _enqueue(self):
        left = self.total_count - len(self.msg_queue)
        if left <= 0: return
        req = self._create_req({
            'limit': 100,
            'before_id': self.msg_queue[-1]['id']
        })
        res_text = urllib.request.urlopen(req).read().decode('utf-8')
        res_json = json.loads(res_text)
        if not res_json['response']:
            raise Exception('Could not fetch messages')

        self.msg_queue.extend(res_json['response']['messages'])

    def _done(self):
        return self.processed >= self.total_count

    def __iter__(self):
        self._init_queue()
        return self

    def __next__(self):
        try:
            if not self._done():
                if self.processed >= len(self.msg_queue): 
                    self._enqueue()
                self.processed += 1
                res = self.msg_queue[0]
                self.msg_queue.pop(0)

                return res

            else: raise StopIteration
        except urllib.request.HTTPError:
            raise StopIteration

            
if __name__ == '__main__':
    iterate = False

    if len(argv) < 4:
        print('python3 groupme_message_fetch.py <group_id> <token> <filename> [-d]')
        exit(1)
    elif len(argv) == 5:
        iterate = true

    f = GroupmeMsgFetcher(argv[1], argv[2])

    if not iterate:
        print('Dumping log of group {} to file {}.'.format(argv[1], argv[3]))
        f.dump(argv[3])
    else:
        for message in f:
            print(message)

    exit(0)
