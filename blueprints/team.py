from connections import DB, WS

import database.SQL_requests as sql


teamsCount = []
def register_callbacks():
    def joinToTeam(client, data):
        print(client, data)
        foundTeam = None
        for team in teamsCount:
            if team['id'] == data['teamId']:
                team['count'] += 1
                foundTeam = team
        if foundTeam is None:
            foundTeam = {
                'id': data['teamId'],
                'name': data['teamName'],
                'count': 1
            }
            DB.execute(sql.insertTeam, [data['teamName']])
            teamsCount.append(foundTeam)

        WS.send_player_connected(data['userName'], foundTeam['id'], foundTeam['name'])
    WS.setCallback("join_to_team", joinToTeam)

    def quitFromTeam(client, data):
        print(client, data)
        for team in teamsCount:
            if team['id'] == data['teamId']:
                team['count'] -= 1
                WS.send_player_disconnected(data['userName'], team['id'], team['name'])

                if team['count'] <= 0:
                    teamsCount.remove(team)
                    DB.execute(sql.deleteTeamByid, [team['id']])
                return
    WS.setCallback("quit_from_team", quitFromTeam)

    def getAllTeams(client, data):
        return WS.prepare_teams_count(teamsCount)
    WS.setCallback("get_teams_count", getAllTeams)
