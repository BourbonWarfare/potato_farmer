CREATE DATABASE IF NOT EXISTS potato_missions;
USE `potato_missions`;
CREATE TABLE IF NOT EXISTS history(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    mission_uuid VARCHAR(255) NOT NULL,
    player_count INT,
    players_present JSON,
    length INT,
    date DATETIME
);

CREATE TABLE IF NOT EXISTS replays(
    id VARCHAR(255) NOT NULL PRIMARY KEY,
    history_id INT NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    FOREIGN KEY (history_id) REFERENCES history(id)
);
