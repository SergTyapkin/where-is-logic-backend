import os

from connections import WS
from utils.utils import read_config


import blueprints.team as team
import blueprints.answer as answer
team.register_callbacks()
answer.register_callbacks()

config = read_config('config.json')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', config['ws_port']))  # get environment variable "PORT" or port from config
    WS.start(thread=True)
    WS.waitThread()
