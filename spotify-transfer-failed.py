import json
import logging
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from ytmusicapi import YTMusic

# Set up logging to see what is happening
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Spotify API info (Put your stuff here)
spotifyClientId = "YOUR_SPOTIFY_CLIENT_ID"
spotifyClientSecret = "YOUR_SPOTIFY_CLIENT_SECRET"
spotifyRedirectUri = "http://localhost:8888/callback"  # Where Spotify sends you back

# Use YouTube Music API (Get your auth file first)
ytmusic = YTMusic('oauth.json')

# Create Spotify client to talk to Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spotifyClientId,
                                               client_secret=spotifyClientSecret,
                                               redirect_uri=spotifyRedirectUri,
                                               scope='playlist-read-private'))

# Load failed tracks from the JSON file
def loadFailedPlaylists():
    with open('failed_tracks.json', 'r') as f:
        failedTracks = json.load(f)
    return failedTracks

# Save updated failed tracks back to the JSON file
def saveFailedTracks(failedTracks):
    with open('failed_tracks.json', 'w') as f:
        json.dump(failedTracks, f, indent=4)

# Function to move playlists
def transferPlaylists():
    failedTracksData = loadFailedPlaylists()
    failedPlaylists = set(track['playlist'] for track in failedTracksData)
    updatedFailedTracks = []

    # Get playlists from Spotify
    playlists = sp.current_user_playlists()

    for playlist in playlists['items']:
        playlistName = playlist['name']

        # Only process playlists in the failed list
        if playlistName not in failedPlaylists:
            continue

        logger.info(f'Processing failed playlist: {playlistName}')

        # Check if playlist already exists on YouTube Music
        existingPlaylists = ytmusic.get_library_playlists(limit=500)
        if any(existingPlaylist['title'] == playlistName for existingPlaylist in existingPlaylists):
            logger.warning(f'Skipping existing playlist: {playlistName}')
            continue

        # Create a new playlist on YouTube Music
        try:
            newPlaylistId = ytmusic.create_playlist(title=playlistName, description=playlist['description'])
            logger.info(f'Created new playlist: {playlistName}')

            # Get tracks from Spotify playlist
            tracks = sp.playlist_tracks(playlist['id'])
            for track in tracks['items']:
                trackName = track['track']['name']
                artistNames = [artist['name'] for artist in track['track']['artists']]
                query = f"{trackName} {' '.join(artistNames)}"
                
                # Look for the track on YouTube Music
                searchResults = ytmusic.search(query, filter='songs')
                if searchResults:
                    # Add first found result to new playlist
                    ytmusic.add_playlist_items(newPlaylistId, [searchResults[0]['videoId']])
                    logger.info(f'Added track: {trackName} by {", ".join(artistNames)}')
                else:
                    logger.error(f'Track not found: {trackName} by {", ".join(artistNames)}')
                    updatedFailedTracks.append({'playlist': playlistName, 'track': trackName, 'error': 'Track not found'})

        except Exception as e:
            logger.error(f'Failed to create playlist: {playlistName} - {e}')
            updatedFailedTracks.append({'playlist': playlistName, 'error': str(e)})

    # Save updates to failed tracks
    if updatedFailedTracks != failedTracksData:
        saveFailedTracks(updatedFailedTracks)
        logger.info(f'Updated failed tracks in failed_tracks.json')

# Run the transfer function
if __name__ == "__main__":
    transferPlaylists()
