import firebase_admin
from firebase_admin import credentials, db
import os
import pygame
import random
import time
import sys

# Initialize Firebase
cred = credentials.Certificate("clap.json")  # Ensure this file is in the same directory
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://clap-9b5d9-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# Initialize pygame mixer
pygame.mixer.init()

# Global variables to track the current playing song and folder
current_song = None
current_folder = None

# Base folder containing "Happy", "Sad", and "Folk" subfolders
base_folder = 'My_Playlist'

# Create 'clap' node in Firebase
ref = db.reference('clap')
ref.set(0)  # Default status set to 0

# Function to play a random song from the specified folder
def play_random_song(folder_name):
    global current_song, current_folder
    folder_path = os.path.join(base_folder, folder_name)
    
    if not os.path.exists(folder_path):
        print(f"Folder '{folder_name}' not found.")
        return
    
    files = [f for f in os.listdir(folder_path) if f.endswith('.mp3')]  # Get only .mp3 files
    
    if not files:
        print(f"No songs found in the '{folder_name}' folder.")
        return
    
    # Choose a random song that is not currently playing
    if current_song in files:
        files.remove(current_song)
    
    if not files:  # If only one song exists and it's already played, reload the list
        files = [f for f in os.listdir(folder_path) if f.endswith('.mp3')]
    
    song_path = os.path.join(folder_path, random.choice(files))
    
    # Stop the current song if it's playing
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
        print(f"Stopped: {current_song}")
    
    # Load and play the new song
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play()
    current_song = os.path.basename(song_path)  # Update the current song
    current_folder = folder_name
    
    print(f"Playing: {song_path}")

# Firebase listener callback
def listener(event):
    global current_folder
    if event.data is not None:
        try:
            value = int(event.data)  # Convert Firebase value to integer
            if value == 1:
                if current_folder != "Happy":
                    play_random_song("Happy")
            elif value == 2:
                if current_folder != "Sad":
                    play_random_song("Sad")
            elif value == 3:
                if current_folder != "Folk":
                    play_random_song("Folk")
            else:
                print(f"Invalid value ({value}) received from Firebase.")
        except ValueError:
            print("Received non-integer value from Firebase.")

# Start listening for Firebase changes
listener_handle = ref.listen(listener)

# Keep the script running and monitor song completion
def monitor_music():
    try:
        while True:
            time.sleep(1)  # Keeps the script alive without excessive CPU usage
            if not pygame.mixer.music.get_busy() and current_folder:
                play_random_song(current_folder)  # Play another song from the same folder
    except KeyboardInterrupt:
        print("\n[INFO] KeyboardInterrupt detected. Stopping music and clearing Firebase data.")

        # Stop music and quit pygame
        pygame.mixer.music.stop()
        pygame.mixer.quit()

        # Clear Firebase data
        ref.set(0)  # Reset the 'clap' node to 0

        # Stop Firebase listener
        listener_handle.close()

        print("[INFO] Firebase data cleared. Exiting program.")

        # Exit the script properly
        sys.exit(0)

# Run the monitor function
monitor_music()