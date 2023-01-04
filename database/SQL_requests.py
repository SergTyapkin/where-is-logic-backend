# ----- INSERTS -----
insertTeam = \
    "INSERT INTO teams (id, name, color) " \
    "VALUES (%s, %s, %s) " \
    "RETURNING *"

# ----- SELECTS -----
selectAllTeams = \
    "SELECT * FROM teams " \
    "ORDER BY score DESC"

selectTeamById = \
    "SELECT * FROM teams " \
    "WHERE id = %s"

# ----- UPDATES -----
updateTeamById = \
    "UPDATE teams SET " \
    "name = %s, " \
    "color = %s " \
    "WHERE id = %s " \
    "RETURNING *"

updateTeamScoreById = \
    "UPDATE teams SET " \
    "score = %s " \
    "WHERE id = %s " \
    "RETURNING *"

updateTeamScoreIncrementById = \
    "UPDATE teams SET " \
    "score = score + 1 " \
    "WHERE id = %s " \
    "RETURNING *"

# ----- DELETES -----
deleteTeamByid = \
    "DELETE FROM teams " \
    "WHERE id = %s"

deleteTeamByidIfNoScore = \
    "DELETE FROM teams " \
    "WHERE id = %s AND " \
    "score <= 0"
