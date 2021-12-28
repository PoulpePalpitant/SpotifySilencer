#!/usr/bin/env python3.9

import os   # File manip
import random
from time import (sleep, )

# Mute windows
import pygetwindow as gw    # Pour trouver la fenêtre spotify
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume    # Manipulation avec le mixer windows
from pydub import AudioSegment  # Conversion en mp3
from pygame import mixer        # audio player
import atexit 

#     __  __                 _ __                         __       
#    / / / /___ _      __   (_) /_   _      ______  _____/ /_______
#   / /_/ / __ \ | /| / /  / / __/  | | /| / / __ \/ ___/ //_/ ___/
#  / __  / /_/ / |/ |/ /  / / /_    | |/ |/ / /_/ / /  / ,< (__  ) 
# /_/ /_/\____/|__/|__/  /_/\__/    |__/|__/\____/_/  /_/|_/____/  
                                                                 

# Pour savoir quand muter l'application, on utilise simplement le titre de la fenêtre.
# Quand une chanson joue, la fenêtre spotify change toujours son titre pour ce format : nom_artist - nom_chanson
# On utilise donc la string " - " pour détecter à quel moment muter la fenêtre.

# --------------------------------------------------------------------------------------------------------------------------------------- --- -






possible_window_names = ['Spotify Free', 'Advertisement', 'Spotify']
audio_directory = os.getcwd() + "\\audio\\"



def get_random_file_path(directory):
    """
    Retourne le chemin d'un fichier random dans un dossier
    """

    file = random.choice(os.listdir(directory))
    path = directory + file
    return path


def extract_file_extension(path):
    """
    Retourne le nom de l'extension d'un fichier(sans le point)
    """
    format = os.path.splitext(path)[1]
    format = ''.join(format.split('.', 1))
    return format


def convert_song_to_mp3(directory, fileName):
    """
    Convertie un fichier audio en format mp3. 
    Ceci détruit le fichier original.
    """
    format = extract_file_extension(fileName)
    path = directory + fileName

    if format == "mp3":
        return

    print("Converting \"" + fileName + "\" to mp3")

    audio = None
    if format == "wav":
        audio = AudioSegment.from_wav(path)
    elif format == "ogg":
        audio = AudioSegment.from_ogg(path)
    elif format == "flv":
        audio = AudioSegment.from_flv(path)
    elif format == "mp4":
        audio = AudioSegment.from_file(path, format)
    elif format == "wma":
        audio = AudioSegment.from_file(path, format)
    elif format == "aac":
        audio = AudioSegment.from_file(path, format)
    elif format == "m4a":
        audio = AudioSegment.from_file(path, format)

    if audio:
        songNameWithoutExtension = os.path.splitext(path)[0]
        audio.export(songNameWithoutExtension + ".mp3", format="mp3")
        os.remove(path)
    else:
        print(f'{fileName} couldn\'t be converted to mp3')


def convert_all_songs_to_mp3(directory):
    """
    Convertit tout les fichiers se trouvant dans le dossier audio
    en format mp3. 
    """
    progressCallback = None

    print("Converting all audio files to mp3. This may take awhile...")
    for f in os.listdir(directory):
        convert_song_to_mp3(directory, f)

    print("Files are done!")


def find_spotify_window():
    """
    Trouve l'application spotify à partir du nom de sa fenêtre. Le nom de la fenêtre 
    change selon l'état de l'application
    Lorsque une chanson joue:
        NomArtiste - Chanson

    Pub audio/vidéo:
        Advertisement
        Spotify Free    
        Une string custom provenant de la compagnie

    Pause:
        Spotify
        Spotify Free
    """
    for name in possible_window_names:
        # Retourne une liste de fenêtre avec ce nom
        spotify = gw.getWindowsWithTitle(name)

        if spotify != []:
            print('Fenêtre spotté!')
            return spotify[0]

    print("Fenêtre introuvable. Pèse sur pause et je vais la trouver (:")
    return None


def find_spotify_volume_control():
    """
    Trouve le contrôleur de volume de spotify dans le mixer windows.
    WARNING: Ce contrôleur ne peut apparaître que si l'application à produit du son. 
    Il faut donc laisser l'app jouer de la musique au moins une fois pour le trouver
    """
    volumControl = id = None
    sessions = AudioUtilities.GetAllSessions()
    for s in sessions:
        if s.Process:
            if s.Process.name() == 'Spotify.exe':
                volumControl = s.SimpleAudioVolume
                id = s.ProcessId
                break

    if volumControl == None:
        print("Volume de spotify non détecté. Pèse sur Play et je vais le trouver :)")
    else:
        print("Volume spotté!")

    return volumControl, id


def mute_video_ads_if_playing(id):
    """
    Si une pub vidéo joue, un deuxième process va apparaître dans le mixer windows. 
    On mute celui-ci qu'une seule fois 
    """
    volumControlForVideoAds = None
    sessions = AudioUtilities.GetAllSessions()

    for s in sessions:
        if s.Process:
            if s.Process.name() == 'Spotify.exe':
                if s.ProcessId != id:
                    volumControlForVideoAds = s.SimpleAudioVolume
                    break

    if volumControlForVideoAds == None:
        return False

    volumControlForVideoAds.SetMute(1, None)
    print("Volume de publicité vidéo spotté, et muté à tout jamais")
    return True


def is_song_playing(windowTitle):
    """
        Quand une chanson joue, le format du windowTitle est toujours le même:
        Artist - Song name
        La string " - " est toujours présente. 
        Lorsqu'une pub joue ou que l'application est en pause, cette string n'est jamais ou très très rarement utilisé
    """
    theUltimateCharacter = ' - '
    return theUltimateCharacter in windowTitle




def exit_handler():
    """
    Unmute spotify quand on ferme l'application
    """
    volumControl.SetMute(0, None)   



if __name__ == '__main__':
    atexit.register(exit_handler)
    spotifyWindow = find_spotify_window()

    # Va permettre de muté Spotify dans le mixer de windows
    volumControl, spotifyProcessId = find_spotify_volume_control()
    videoAdsAreMuted = False
    mixer.init()

    # Convertie tout les fichiers du folder audio en mp3, si possible
    convert_all_songs_to_mp3((audio_directory))

    while(True):
        """
        Il faut d'abord détecter la fenêtre spotify et son volume dans le mixer
        windows. Pour ce faire, il faut que l'application est joué de l'audio
        au moins 1 fois et que le titre de la fenêtre soit un de ceux présent 
        dans le dict "possible_window_names"
        """
        if spotifyWindow == None:
            spotifyWindow = find_spotify_window()

        if volumControl == None:
            volumControl, spotifyProcessId = find_spotify_volume_control()

        if volumControl is None or spotifyWindow is None:
            sleep(1)
            continue

        # Pas de chanson qui joue, alors ad ou pause
        if is_song_playing(spotifyWindow.title):
            if volumControl.GetMute() == True:
                volumControl.SetMute(0, None)   # unmute
                print("--- Intermission ended ---\n")
                print(f'Song playing : {spotifyWindow.title}')
                mixer.music.fadeout(1000)
        else:
            if videoAdsAreMuted == False:
                videoAdsAreMuted = mute_video_ads_if_playing(spotifyProcessId)

            if volumControl.GetMute() == False:
                volumControl.SetMute(1, None)   # mute
                print("Ad playing, or paused...")
                if spotifyWindow.title != 'Spotify Free':  # Fais pas jouer de beat au cas où c'était un pause
                    intermission = get_random_file_path(audio_directory)
                    mixer.music.load(intermission)
                    mixer.music.play()
                    print(f'--- Playing intermission : {intermission} ---\n')
        
        sleep(1.5)
        
