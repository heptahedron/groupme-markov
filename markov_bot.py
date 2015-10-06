# vim:sw=4 ts=4
from groupme_bot import GroupmeBot
import groupme_message_fetch
import re
import json
import random
from sys import argv, exit

class MarkovBot(GroupmeBot):
    def __init__(self, bot_id, name):
        super().__init__(bot_id)
        self.name = name
        self.members = {}
        self.member_aliases = {}

    def parse_history(self, filename):
        print('Parsing group history...')
        with open(filename) as f:
            messages = json.load(f)
            for msg in messages:
                if msg['sender_type'] == 'bot': continue
                if not msg['text']: continue
                if msg['text'].startswith(self.name): continue

                sender_id = msg['sender_id']
                if not sender_id in self.members:
                    self.members[sender_id] = []

                if not msg['name'] in self.member_aliases:
                    self.member_aliases[msg['name']] = msg['sender_id']
                
                words = re.split('\s+', msg['text'])
                # this should be changed at some point
                words = list(filter(lambda word: word != '', words))
                self.members[sender_id].append((None, words[0]))
                for i, word in enumerate(words):
                    if i < len(words) - 1:
                        nextword = words[i+1]
                    else: 
                        nextword = None
                    self.members[sender_id].append((word, nextword))
        print('Done.')

        
    def msg_received(self, sender, msg):
        res = re.match('^{}[,:!]?\s+(.*)$'.format(self.name), msg)
        if res == None or res.group(1) == '':
            return

        self.command(res.group(1), sender)

    def command(self, cmd, sender):
        res = re.match('^what would (.*) say (right now|[^\?]*)\??$', cmd)
        if res:
            if res.group(2) == 'right now':
                situation = None
            else:
                situation = res.group(2)
            if res.group(1) == 'I':
                subject = sender[0]
                s_id = sender[1]
            elif res.group(1) in self.member_aliases:
                subject =  res.group(1)
                s_id = self.member_aliases[subject]
            
            if situation:
                self.say('{}, {}: {}'.format(
                    subject, situation, self.gen_sentence(s_id)))
            else:
                self.say('{}: {}'.format(
                    subject, self.gen_sentence(s_id)))
        
    def gen_sentence(self, sender_id):
        samp_space = self.members[sender_id]
        cur_word = None
        sentence_words = []
        while True:
            preceded_by = lambda pair: pair[0] == cur_word
            next_words = list(filter(preceded_by, samp_space))
            next_idx = random.randint(0, len(next_words)-1)
            if next_words[next_idx][1] == None: break
            cur_word = next_words[next_idx][1]
            sentence_words.append(cur_word)

        return ' '.join(sentence_words)

if __name__ == '__main__':
    if len(argv) < 4:
        print('arguments: bot id, name, history file')
        exit(1)
    mb = MarkovBot(argv[1], argv[2])
    mb.parse_history(argv[3])
    mb.listen()
