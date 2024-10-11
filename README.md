# Playlist Transfer Tool

This tool enables you to effortlessly transfer playlists from Spotify to YouTube Music. It uses the Spotipy library to access the Spotify API and the YTMusicAPI for interacting with YouTube Music.

## Requirements

To get started, you will need:

- **Python**: Ensure you have Python installed on your machine. You can download it from [python.org](https://www.python.org/downloads/).
- **Spotify API Developer Key and Secret**: Sign up for a Spotify Developer account and create an application to obtain your API credentials. More information can be found [here](https://developer.spotify.com/documentation/general/guides/app-settings/).
- **Spotipy**: This Python library allows access to the Spotify Web API. Install it using pip:

  ```bash
  pip install spotipy
  ```

- **ytmusicapi**: This library provides access to YouTube Music. Install it with:

  ```bash
  pip install ytmusicapi
  ```

- **OAuth for YouTube Music**: Before running the scripts, you need to execute the following command to set up authentication for YouTube Music:

  ```bash
  ytmusicapi oauth
  ```

## Getting Started

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/JohnMcWhirter10/spotify-to-youtube-music.git
   cd spotify-to-youtube-music
   ```

2. **Set Up Your Credentials**:

   Open the script files and replace the placeholders for `spotifyClientId`, `spotifyClientSecret`, and `spotifyRedirectUri` with your actual Spotify API credentials.

   You can use the default localhost URL provided as an example on the Spotify API website for `spotifyRedirectUri`.

3. **Run the Scripts**:

   Execute the following command to transfer your playlists from Spotify to YouTube Music:

   ```bash
   python spotify-transfer.py
   ```

   This will create new playlists on YouTube Music based on your Spotify playlists.

4. **Check for Failed Transfers**:

   If any tracks fail to transfer, they will be logged in a `failed_tracks.json` file. You can rerun the transfer for those specific playlists using:

   ```bash
   python spotify-transfer-failed.py
   ```

## Notes

- Keep your credentials safe and do not share them publicly.
- This tool is intended for personal use and is not affiliated with Spotify or YouTube Music.
- If you encounter issues, check the logs for errors and ensure your API keys are set up correctly.
- If you receive an error message indicating to wait before creating a playlist, don’t worry—nothing is broken! Simply come back to it tomorrow.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

---

Happy transferring! 🎶
