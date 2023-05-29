# Python Youtube Data API v3 on personal playlists

Project using the YouTube API from Google with Python to access and interact with playlists on my personal account.

-The files "playlist_items_retrieving.py" and "playlist_items_insert.py" are Python scripts for making requests with the YouTube Data API v3 using OAuth 2.0 authentication to access my personal channel. The requests involve retrieving information about my playlists and the items within them.
-The "convert_mp3" file converts the selected items from a chosen playlist into MP3 files and sends them to the Mr. Pug server on Discord(my personal server). Finally, it deletes the selected items from the YouTube playlist.

## Technologies used:

-Google API client
-YouTube Data API v3
-JSON
-Pytube (converting YouTube videos to MP3)
-Discorweebhook (sending MP3 files to Discord)
-OAuth 2.0 (to create a token for authorization of requests)

## Setting up the Google API environment:

Google Cloud -> Create a project -> Enable YouTube Data API v3
-> Create an OAuth client -> YOUR_CLIENT_SECRET_FILE.JSON

## Limits:

Maximum of 80 webhook requests to send MP3 files in Python.
