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
            try:
                DB.execute(sql.insertTeam, [data['teamId'], data['teamName'], data['teamName']])
            except:
                pass
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
                    DB.execute(sql.deleteTeamByidIfNoScore, [team['id']])
                return
    WS.setCallback("quit_from_team", quitFromTeam)

    def getAllTeams(client, data):
        teams = DB.execute(sql.selectAllTeams, [], manyResults=True)
        for team in teams:
            for findTeam in teamsCount:
                if team['id'] == findTeam['id']:
                    team['count'] = findTeam['count']
                    break
        return WS.prepare_teams_count(teams)
    WS.setCallback("get_teams_count", getAllTeams)
