from connections import DB, WS
from utils.utils import *

import database.SQL_requests as sql


# Timer(3, party_time, args=None, kwargs=None).start()


answeringTeam = None
def register_callbacks():
    def answer(client, data):
        global answeringTeam
        if answeringTeam is not None:
            return
        answeringTeam = {
            'userName': data['userName'],
            'teamId': data['teamId'],
            'teamName': data['teamName'],
        }

        WS.send_team_answered(data['userName'], data['teamId'], data['teamName'])
    WS.setCallback("answer", answer)

    def answerResult(client, data):
        global answeringTeam
        if answeringTeam is None:
            return

        if data['result']:
            DB.execute(sql.updateTeamScoreIncrementById, [answeringTeam['teamId']])

        team = DB.execute(sql.selectTeamById, [answeringTeam['teamId']])
        WS.send_answer_result(data['result'], team['score'])

        answeringTeam = None
    WS.setCallback("answer_result", answerResult)

    def getAnsweringState(client, data):
        return WS.prepare_answering_state(answeringTeam)
    WS.setCallback("get_answering_state", getAnsweringState)
