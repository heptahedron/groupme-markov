# vim:sw=4 ts=4
from groupme_bot_server import GroupmeBotServer
from markov_bot import MarkovBot
import json
from sys import argv, exit

def create_markov_bot(b):
    if not b['history_file']:
        print('History file required for MarkovBot.')
        return None
    mb = MarkovBot(b['group_id'], b['bot_id'], b['name'])
    mb.parse_history(b['history_file'])
    return mb

bot_types = {
    'markov': create_markov_bot
}

def create_bot_from_dict(b):
    if b['type'] not in bot_types:
        print('Bot type "{}" not recognized.'.format(bot['type']))
        return None

    return bot_types[b['type']](b)

if __name__ == '__main__':
    if len(argv) < 2:
        print('Bot configuration file required.')
        exit(1)

    bots = []

    with open(argv[1]) as f:
        bots_conf = json.load(f)
        print('Parsing bots configuration file...')
        for bot in bots_conf:
            newbot = create_bot_from_dict(bot)
            if newbot: bots.append(newbot)
            else: print('Could not create bot {}'.format(bot['bot_id']))

    print('Initialized bots', bots)
    print('Starting Groupme bot server...')
    gbs = GroupmeBotServer(bots)
    print('Done.')
    print('Listening...')
    gbs.listen()
