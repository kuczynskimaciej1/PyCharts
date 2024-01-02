-- Create User table
CREATE TABLE User (
    user_id INTEGER PRIMARY KEY,
    spotify_name TEXT,
    uri TEXT,
    user_internal_id TEXT
);

-- Create Playlist table
CREATE TABLE Playlist (
    playlist_id INTEGER PRIMARY KEY,
    user_id TEXT,
    playlist_name TEXT,
    date_of_creation DATE,
    playlist_internal_id TEXT,
    generation_method TEXT,
	parameters TEXT,
    correlation REAL,
    FOREIGN KEY (user_id) REFERENCES User(user_internal_id)
);

-- Create Track table
CREATE TABLE Track (
    track_id INTEGER PRIMARY KEY,
    playlist_id TEXT,
    mark_given INTEGER,
    rank_on_list INTEGER,
    uri TEXT,
    dataset_id INTEGER,
    title TEXT,
    artist TEXT,
    album TEXT,
    FOREIGN KEY (playlist_id) REFERENCES Playlist(playlist_internal_id)
);