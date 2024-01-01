-- Create User table
CREATE TABLE User (
    user_id INTEGER PRIMARY KEY,
    spotify_name TEXT,
    uri TEXT
);

-- Create Playlist table
CREATE TABLE Playlist (
    playlist_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    playlist_name TEXT,
    date_of_creation DATE,
    FOREIGN KEY (user_id) REFERENCES User(user_id)
);

-- Create Track table
CREATE TABLE Track (
    track_id INTEGER PRIMARY KEY,
    playlist_id INTEGER,
    mark_given INTEGER,
    rank_on_list INTEGER,
    uri TEXT,
    dataset_id INTEGER,
    FOREIGN KEY (playlist_id) REFERENCES Playlist(playlist_id)
);