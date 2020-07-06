CREATE TABLE UrlMap
(
    original_url TEXT NOT NULL,
    short_hash   TEXT primary key
);

CREATE TABLE HashIdGen
(
    id INTEGER PRIMARY KEY AUTOINCREMENT
);
