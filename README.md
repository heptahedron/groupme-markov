# groupme-markov

With some trivial configuration, you too can have a bot in your Groupme that will spout nonsense sounding similar to your friends.

## Running

The bots require a configuration file and a group history file to build up the user dictionaries.
An example is provided for the former in `bots_conf.json.example`, the latter can be fetched using
`groupme_message_fetch.py`. If one were so inclined, it would be possible to integrate dialogue from
artbitrary people not found in the group into the history file, thus allowing for everyone from 
Jaden Smith to Barack Obama to be emulated.

When these files have been created, just use `run_bots.py` to start the server. Make sure everything on
your Groupme Developers account is configured appropriately.
