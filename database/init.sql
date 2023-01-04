------- Users data -------
CREATE TABLE IF NOT EXISTS teams (
    id                 SERIAL PRIMARY KEY,
    name               TEXT DEFAULT '',
    color              TEXT NOT NULL,
    score              INT DEFAULT 0
);
