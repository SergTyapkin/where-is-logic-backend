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

        DB.execute(sql.updateTeamScoreIncrementById, [data['teamId']])

        WS.send_team_answered(data['userName'], data['teamId'], data['teamName'])
    WS.setCallback("answer", answer)

    def answerResult(client, data):
        global answeringTeam
        if answeringTeam is None:
            return
        answeringTeam = None

        WS.send_answer_result(data['result'])
    WS.setCallback("answer_result", answerResult)

    def getAnsweringState(client, data):
        return WS.prepare_answering_state(answeringTeam)
    WS.setCallback("get_answering_state", getAnsweringState)
