-- Create User table
CREATE TABLE User (
    user_id INT PRIMARY KEY,
    spotify_nickname VARCHAR(255)
);

-- Create Playlist table
CREATE TABLE Playlist (
    playlist_id INT PRIMARY KEY,
    user_id INT,
    playlist_name VARCHAR(255),
    created_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES User(user_id)
);

-- Create Track table
CREATE TABLE Track (
    track_id INT PRIMARY KEY,
    playlist_id INT,
    track_name VARCHAR(255),
    artist VARCHAR(255),
    duration TIME,
    FOREIGN KEY (playlist_id) REFERENCES Playlist(playlist_id)
);

-- Create PlaylistTrack table
CREATE TABLE PlaylistTrack (
    playlist_id INT,
    track_id INT,
    PRIMARY KEY (playlist_id, track_id),
    FOREIGN KEY (playlist_id) REFERENCES Playlist(playlist_id),
    FOREIGN KEY (track_id) REFERENCES Track(track_id)
);

--
GRANT ALL PRIVILEGES ON pycharts TO mkuczyns@localhost;track
