PRAGMA foreign_keys = ON;

CREATE TABLE game (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    release_date TEXT,
    genre TEXT,
    cover TEXT,
    banner TEXT
);

CREATE TABLE company (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    started TEXT NOT NULL
);

CREATE TABLE game_developer (
    id INTEGER PRIMARY KEY,
    game_id INTEGER NOT NULL,
    company_id INTEGER NOT NULL,

    UNIQUE (game_id, company_id),

    FOREIGN KEY (game_id)
        REFERENCES game(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    FOREIGN KEY (company_id)
        REFERENCES company(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE game_publisher (
    id INTEGER PRIMARY KEY,
    game_id INTEGER NOT NULL,
    company_id INTEGER NOT NULL,

    UNIQUE (game_id, company_id),

    FOREIGN KEY (game_id)
        REFERENCES game(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    FOREIGN KEY (company_id)
        REFERENCES company(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL
);

CREATE TABLE favourite (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    game_id INTEGER NOT NULL,

    UNIQUE (user_id, game_id),

    FOREIGN KEY (user_id)
        REFERENCES user(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    FOREIGN KEY (game_id)
        REFERENCES game(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE company_favourite (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    company_id INTEGER NOT NULL,

    UNIQUE (user_id, company_id),

    FOREIGN KEY (user_id)
        REFERENCES user(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    FOREIGN KEY (company_id)
        REFERENCES company(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE browsing_history (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    game_id INTEGER NOT NULL,
    viewed_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    UNIQUE (user_id, game_id),

    FOREIGN KEY (user_id)
        REFERENCES user(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    FOREIGN KEY (game_id)
        REFERENCES game(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE INDEX idx_game_developer_game
    ON game_developer(game_id);

CREATE INDEX idx_game_developer_company
    ON game_developer(company_id);

CREATE INDEX idx_game_publisher_game
    ON game_publisher(game_id);

CREATE INDEX idx_game_publisher_company
    ON game_publisher(company_id);

CREATE INDEX idx_favourite_user
    ON favourite(user_id);

CREATE INDEX idx_favourite_game
    ON favourite(game_id);

CREATE INDEX idx_company_favourite_user
    ON company_favourite(user_id);

CREATE INDEX idx_company_favourite_company
    ON company_favourite(company_id);

CREATE INDEX idx_browsing_history_user
    ON browsing_history(user_id);

CREATE INDEX idx_browsing_history_game
    ON browsing_history(game_id);