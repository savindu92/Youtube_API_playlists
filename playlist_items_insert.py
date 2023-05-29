# -*- coding: utf-8 -*-

#* Sample Python code for youtube.playlistItems.insert
#* See instructions for running these code samples locally:
#* https://developers.google.com/explorer-help/guides/code_samples#python

import os
import json
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors


scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def main():
    #* Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"
    
    #* Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    #* List of playlist contain in Mr Pug channel
    playlist_names = {

        "1":"Best_kpop",
        "2":"Favorite_kpop_mvs",
        "3":"Favorite_English_songs",
        "4":"Favorite_japanese_songs",
        "5":"Ost",
        "6":"Favorite_anime_ops_ends",
        "7":"music_mp3"

    }

    #* Creation of a new playlist in Mr pug with selected playlist name
    playlist_id_name = playlist_names.get("5")

    request_create = youtube.playlists().insert(
        part="snippet",
        body={
            "snippet": {
                "title": playlist_id_name
            }

        }
    )
    response_create = request_create.execute()

    #* Inserting of all items contain in selected json file in the new playlist created
    playlistId = response_create.get('id')

    filename = "./playlists_saved/{}.json".format(playlist_id_name)
    with open(filename, 'r') as file_ids:
        videoIds = json.load(file_ids)

    for videoId in videoIds:
        request = youtube.playlistItems().insert(
            part="snippet",
            body={
              "kind": "youtube#playlistItem",
              "snippet": {
                "playlistId": playlistId,
                "position": 0,
                "resourceId": {
                  "kind": "youtube#video",
                  "videoId": videoId
                }
              },
            }
        )
        response = request.execute()

        print("\n\n\n{}".format(response))

if __name__ == "__main__":
    main()