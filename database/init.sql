------- Users data -------
CREATE TABLE IF NOT EXISTS teams (
    id                 INT UNIQUE NOT NULL,
    name               TEXT DEFAULT '',
    color              TEXT NOT NULL,
    score              INT DEFAULT 0
);
