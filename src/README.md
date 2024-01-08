# PyCharms Info

## Copyrights and license

Created by Maciej Kuczynski for Czestochowa University of Technology
2023 &copy; All rights reserved.

## File structure

- _ai-global-var.py_ – contains global variables relating to the training data set and the trained neural network model.

- _ai-recommendation.py_ – contains functions for generating a recommended playlist using AI.

- _ai.py_ – defines the neural network model, determines parameters and supervises the learning process.

- _classes.py_ - contains the definition of the Track class.

- _database-global-var.py_ – a set of global variables relating to database operations, e.g. access, reading and writing operations.

- _database-py_ – contains functions that allow you to establish or close a connection to the database, create tables and add data to them.

- _dl-data.py_ – a set of functions that use the Spotify API, allowing you to download data about the user and songs from it.

- _flask-app.py_ – the most extensive file that handles the routing of pages and function calls by the Flask framework throughout the entire operation of the PyCharts application.

- _learning-set.py_ – contains functions that prepare and adjust the data set before the neural network training process.

- _login-global-var.py_ – stores global data about the logged in user, access to Spotify API and the ongoing session.

- _main.py_ - boot file that starts the application.

- _maths-and-stats.py_ – contains functions for calculating correlations between playlists and numerical statistics of the selected user.

- _no-ai-recommendation.py_ – a file analogous to ai_recommendation.py, with the difference that it supports the functions of generating a recommended playlist without the use of AI.

- _ul-data.py_ – stores a function that uses the Spotify API, allowing the generated playlist to be uploaded to the user's account.
