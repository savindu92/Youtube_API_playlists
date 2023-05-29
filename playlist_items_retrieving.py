#-*- coding: utf-8 -*-

#* Sample Python code for youtube.playlistItems.list
#* See instructions for running these code samples locally:
#* https://developers.google.com/explorer-help/code-samples#python

import os
import json
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def main():
    #* Disable OAuthlib's HTTPS verification when running locally.
    #* *DO NOT* leave this option enabled in production.
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

    #* all playlists available from Mr Pug youtube channel
    playlist_ids = {

        "Best_kpop": "PLz9TylT9BWzyMILiAYktXdVj2Bm8zzYeV",
        "Favorite_kpop_mvs": "PLz9TylT9BWzw82G8vRHtqsxUXlL8OjcsC",
        "Favorite_English_songs": "PLz9TylT9BWzxKOOOdiuN1G06TmQG9biNm",
        "Favorite_japanese_songs": "PLz9TylT9BWzzWC2FI4-jRNdqp_4G5OE0e",
        "Ost": "PLz9TylT9BWzzb1jJxgX9o6waH0hhEL1s9",
        "Favorite_anime_ops_ends": "PLz9TylT9BWzztfxKfmPVGvrQjcPYjv-BV",
        "music_mp3": "PLz9TylT9BWzw4Gw1Py4cBWDFAIOFr66PM",
        "convert_mp3": "PLz9TylT9BWzxb5HqKNAF1xDYY7mI1ulog"
    }

    #* loop for collecting ids in each playlist
    for cle, valeur in playlist_ids.items():

        
        playlist_id = playlist_ids.get(cle)

        #* collect data from all playlists in Mr Pug channel
        request = youtube.playlistItems().list(
            part="snippet",
            playlistId= playlist_id,
            maxResults="50"
        )
        res = request.execute()


        nextPageToken = res.get('nextPageToken')
        while ('nextPageToken' in res):
            nextPage = youtube.playlistItems().list(
                part="snippet",
                playlistId = playlist_id,
                maxResults="50",
                pageToken=nextPageToken
            ).execute()
            res['items'] = res['items'] + nextPage['items']

            if 'nextPageToken' not in nextPage:
                res.pop('nextPageToken', None)
            else:
                nextPageToken = nextPage['nextPageToken']
        

        videoIds = []

        print(res)
        
        #* add id's video into list and display data
        for search_result in res.get("items", []):

            snippet = search_result.get("snippet")
            title = snippet.get("title")
            resourceId = snippet.get("resourceId")
            videoId = resourceId.get("videoId")

            videoIds.append(videoId)
            print("titre: {}, id: {}\n".format(title,videoId))
            
        print("{}\n".format(videoIds))

        print("Le nombre d'items dans cette playlist est de: {} \n\n\n".format(len(videoIds)))

        
        list_ids = json.dumps(videoIds)

        filename = "./playlists_saved/{}.json".format(cle)
        with open(filename, 'w') as convert_file:
            convert_file.write(list_ids)

if __name__ == "__main__":
    main()