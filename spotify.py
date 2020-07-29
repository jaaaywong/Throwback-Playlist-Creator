import sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util
import subprocess as sp
import eyed3
import glob

from billboard.spiders.billboard_spider import billboards

scope = 'user-library-modify playlist-modify-private playlist-modify-public user-read-private'

#input your own client ID and client secret from spotify developers website
client_id = ''
client_secret = ''
username = ''

redirect_uri = 'http://localhost:8888/callback' # Setup the call back you want to 

def createTemporaryServer():
	print("Starting Temporary Server")
	s = sp.Popen(['python','redirectServer.py'])
	return s

def closeTemporaryServer(server):
	print("Closing Temporary Server")
	sp.Popen.terminate(server)

def assignUser(user):
	username = user
	print('USERNAME: ' + username)

def createPlaylist(sp,username):
	playlistName = 'Throwbacks'
	#check for currently labled "throwbacks" playlist
	#if found, number it as throwbacks i + 1
	description = 'issa blast from the past'
	playlist = sp.user_playlist_create(username,playlistName,False,description)

	#testing, make create playlist
	playlistID = playlist['uri']
	return playlistID
	
def getUserInfo(sp):

	return user

def searchSong(sp, song):
	artistName = song.artist
	songName = song.name
	if (artistName.find('Featuring')):
		artistName = artistName.replace('Featuring ', '')
	if (artistName.find('& ')):
		artistName = artistName.replace('& ', '')
	if (artistName.find('With ')):
		artistName = artistName.replace('With ', '')
	if (artistName.find('Duet ')):
		artistName = artistName.replace('Duet ', '')
	if (artistName.find('Cast of')):
		artistName = artistName.replace('Cast Of ', '')
	if (artistName.find(' x ')):
		artistName = artistName.replace(' x ', ' ')
	if (songName.find('.')):
		songName = songName.replace('.','')
	
	res = sp.search(q=songName + ' ' + artistName , type="track")
	items = res['tracks']['items']
	if len(items) > 0:
		item = items[0]
		uri = item['uri']
		if uri:
			return uri

	return False

def addToPlaylist(playlistName, songInfo):
	user_playlist_add_tracks()

	return False

# main function to be called from main.py, this handles all spotify related interactions
def spotify_main(playlist, user):
	assignUser(user)
	#create token to be used for specified user
	server = createTemporaryServer()
	token = util.prompt_for_user_token(user, scope, client_id , client_secret,redirect_uri)
	closeTemporaryServer(server)
	
	if token:
		sp = spotipy.Spotify(auth=token)
		
		tracks = []
		#add each song
		
		for song in playlist:
			songID = searchSong(sp, song)
			if songID: 
				tracks.append(songID)
				print('SONGID: ' + songID)
		
		#get distinct tracks only
		tracks = list(dict.fromkeys(tracks))

		#can only upload 100 songs at a time
		tempTracks = []
		j = 0
		#create playlist as long as there are songs queued up
		if (len(tracks) > 0):
			playlistID = createPlaylist(sp,user)
			for song in tracks:
				tempTracks.append(song)
				j = j + 1
				if j%99 == 0:
					sp.user_playlist_add_tracks(username,playlistID,tempTracks)
					tempTracks.clear()
			#imports the rest of the songs in the list
			sp.user_playlist_add_tracks(username,playlistID,tempTracks)
		