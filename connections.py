from WebSocket.WebSocket import WebSocket
from database.database import Database
from utils.utils import read_config


config = read_config('config.json')
DB = Database(
    host=config['db_host'],
    port=config['db_port'],
    user=config['db_user'],
    password=config['db_password'],
    dbname=config['db_database'],
)
WS = WebSocket(port=int(config['ws_port']))
