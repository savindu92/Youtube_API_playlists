# libraries for youtube api, discordWebhook and google client authenfication 

import json 
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from pytube import YouTube
from discord_webhook import DiscordWebhook


scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
scopes2 = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def run():
    
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
    
    #* First step: List all item's ids from convert_mp3 playlist
    playlist_id="PLz9TylT9BWzxb5HqKNAF1xDYY7mI1ulog"

    request = youtube.playlistItems().list(
        part="snippet",
        playlistId= playlist_id,
        maxResults="50"
    )
    res = request.execute()

    ItemsIds = list()

    for search_result in res.get("items", []):
        snippet = search_result.get("snippet")
        item_id = search_result.get("id")
        title = snippet.get("title")

        ItemsIds.append(item_id)
        print("titre: {}, id: {}\n".format(title,item_id))


    #* Second step: Convert items to mp3 with videoId from convert_mp3.json
    filename = "./playlists_saved/convert_mp3.json"
    with open(filename, 'r') as file_ids:
        videoIds = json.load(file_ids)

    for videoId in videoIds:

        yt = YouTube("https://youtu.be/{}".format(videoId))
    
        #* extract only audio
        video = yt.streams.filter(only_audio=True).first()
        
        #* check for destination to save file
        destination = "./download_mp3"
        
        #* download the file
        out_file = video.download(output_path=destination)
     
        #* save the file
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'

        os.rename(out_file, new_file)
       
        #* result of success
        print(yt.title + " has been successfully downloaded.")


    #* Final step: Delete all items from convert mp3 playlist
    
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes2)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    for ItemId in ItemsIds:
        request = youtube.playlistItems().delete(
            id = ItemId
            )
        res = request.execute()
        print(res)

   
    #* initialization of Onizuka weebhook in MrPug servor
    Webhook_url = "https://discordapp.com/api/webhooks/1027572740623970324/hZf1pgD0hmg6mGzuVqmmHExLq1RKV2MXXgfwINW3l1Uso4qb2kvr0cf8590E1Atle5lL"

    download_mp3_files = os.listdir("./download_mp3")
    
    #* send files into Onizuka python channel
    print(download_mp3_files)
    
    for file_name in download_mp3_files:

        webhook = DiscordWebhook(url=Webhook_url, username='{}'.format(file_name))

        path_to_file = "./download_mp3/{}".format(file_name)

        with open(path_to_file, "rb") as f:
            webhook.add_file(file=f.read(), filename='{}'.format(file_name))
        
        
        response = webhook.execute()

    

if __name__=='__main__':
    run()
