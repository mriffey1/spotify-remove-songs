import tkinter as tk
from tkinter import messagebox
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv()
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
redirect_uri = os.getenv('REDIRECT_URI')
scope = os.getenv('SCOPE')

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope))


def load_playlist():
    playlist_id = playlist_id_entry.get()
    if not playlist_id:
        messagebox.showerror("Error", "Please enter a playlist ID.")
        return

    tracks_listbox.delete(0, tk.END)
    track_data.clear()

    try:
        results = sp.playlist_tracks(playlist_id)
        tracks = results['items']

        while results['next']:
            results = sp.next(results)
            tracks.extend(results['items'])

        for i, item in enumerate(tracks):
            track = item['track']
            track_info = f"{track['name']} by {track['artists'][0]['name']}"
            tracks_listbox.insert(tk.END, track_info)
            track_data.append(track['uri'])

    except Exception as e:
        messagebox.showerror("Error", str(e))


def remove_selected_songs():
    selected_indices = tracks_listbox.curselection()
    if not selected_indices:
        messagebox.showerror("Error", "Please select one or more songs to remove.")
        return

    uris_to_remove = [track_data[i] for i in selected_indices]
    playlist_id = playlist_id_entry.get()

    try:
        sp.playlist_remove_all_occurrences_of_items(playlist_id, uris_to_remove)
        messagebox.showinfo("Success", "Selected songs removed successfully!")
        load_playlist()
    except Exception as e:
        messagebox.showerror("Error", str(e))


root = tk.Tk()
root.title("Spotify Playlist Manager")

tk.Label(root, text="Playlist ID:").grid(row=0, column=0, padx=10, pady=10)
playlist_id_entry = tk.Entry(root, width=40)
playlist_id_entry.grid(row=0, column=1, padx=10, pady=10)

load_button = tk.Button(root, text="Load Playlist", command=load_playlist)
load_button.grid(row=0, column=2, padx=10, pady=10)

tracks_listbox = tk.Listbox(root, width=60, height=20, selectmode=tk.MULTIPLE)
tracks_listbox.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

remove_button = tk.Button(root, text="Remove Selected Songs", command=remove_selected_songs)
remove_button.grid(row=2, column=0, columnspan=3, pady=10)

track_data = []

root.mainloop()
