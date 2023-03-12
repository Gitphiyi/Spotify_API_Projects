import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import os

class APIProject:
    def __init__(self, clientID, clientSecret, scope, redirectURI, deviceType):
        self.clientID = clientID
        self.clientSecret = clientSecret
        self.scope = scope
        self.redirectURI = redirectURI
        self.auth_manager = SpotifyOAuth(client_id=clientID, client_secret=clientSecret, redirect_uri=redirectURI, scope = scope)
        token_dict = self.auth_manager.get_access_token()
        token = token_dict['access_token']
        self.sp = spotipy.Spotify(auth = token)
        self.deviceID = self.setDeviceID(deviceType=deviceType)

    def setDeviceID(self, deviceType):
        devices = self.sp.devices()
        id = None
        for device in devices['devices']:
            #print(device["type"])
            if deviceType == device['type']:
                id = device['id']
                break
        return id

    def playAlbum(self, albumName):
        result = self.sp.search(albumName, 1, 0, "album")
        alb = result["albums"]
        alb_items= alb["items"]
        album = alb_items[0]["uri"]
        self.sp.start_playback(device_id=self.deviceID, context_uri=album, offset={"position":0})

    def playSong(self, songName):
        result = self.sp.search(songName, 1, 0, "track")
        track = result["tracks"]
        track_items= track["items"]
        track = track_items[0]["uri"]
        #print(track)
        self.sp.start_playback(device_id=self.deviceID, uris=[track])

def main():
    clientID = "29b5ad5e71a64356a845998113a935af" #my Spotify client ID
    clientSecret = os.environ['SPOTIFY_PRIVATE_ID']
    redirectURI = os.environ["SPOTIPY_REDIRECT_URI"]
    scope = 'user-modify-playback-state app-remote-control streaming user-read-playback-state'
    deviceType = ['Computer', 'Smartphone']

    proj = APIProject(clientID=clientID, clientSecret=clientSecret, redirectURI=redirectURI, scope=scope, deviceType=deviceType[1])
    
    proj.playSong("Pompeii")

if __name__ == "__main__":
    main()
    

