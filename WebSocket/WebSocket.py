import json
import logging
from WebSocket.websocket_server.cb_websocket_server import CallbacksWebSocketServer


# Singleton
class WebSocket(CallbacksWebSocketServer):
    def __new__(cls, *args, **kwargs):  # make singleton
        if not hasattr(cls, 'instance'):
            cls._init(cls, *args, **kwargs)
            cls.instance = super(WebSocket, cls).__new__(cls)
        return cls.instance

    def onConnected(self, client):
        print(client.address)
    def onDisconnected(self, client):
        print(client.address)

    def _init(self, *args, **kwargs):
        print("WS server created")
        self.onConnectedCallback = self.onConnected
        self.onDisconnectedCallback = self.onDisconnected
        super().__init__(self, *args, **kwargs, logLevel=logging.DEBUG)


    def send_player_connected(self, playerName, teamId, teamName):
        self.send_broadcast(json.dumps({
            "event": "player_connected",
            "data": {
                "userName": playerName,
                "teamId": teamId,
                "teamName": teamName,
            }
        }))
    def send_player_disconnected(self, playerName, teamId, teamName):
        self.send_broadcast(json.dumps({
            "event": "player_disconnected",
            "data": {
                "userName": playerName,
                "teamId": teamId,
                "teamName": teamName,
            }
        }))

    def send_team_answered(self, playerName, teamId, teamName):
        self.send_broadcast(json.dumps({
            "event": "team_answered",
            "data": {
                "userName": playerName,
                "teamId": teamId,
                "teamName": teamName,
            }
        }))

    def send_answer_result(self, result, score):
        self.send_broadcast(json.dumps({
            "event": "answer_rated",
            "data": {
                "result": result,
                "score": score,
            }
        }))

    def prepare_teams_count(self, teamsCount: list):
        return {
            "event": "teams_count",
            "data": {
                "teams": teamsCount
            }
        }

    def prepare_answering_state(self, answeringTeam):
        return {
            "event": "answering_state",
            "data": {
                "team": answeringTeam,
            }
        }
