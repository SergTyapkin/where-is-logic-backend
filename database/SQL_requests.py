# ----- INSERTS -----
insertTeam = \
    "INSERT INTO teams (color) " \
    "VALUES (%s) " \
    "RETURNING *"

# ----- SELECTS -----
selectAllTeams = \
    "SELECT * FROM teams"

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
