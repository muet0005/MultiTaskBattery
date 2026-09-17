import os
# Blindfold SDL so it doesn't try to open a black window over PsychoPy
os.environ["SDL_VIDEODRIVER"] = "dummy"

import csv
from psychopy import visual, event, core, gui
from ffpyplayer.player import MediaPlayer
from ffpyplayer.tools import set_loglevel

# Silenced now that connections are working smoothly
set_loglevel("quiet")

# 1. Read stations from the CSV
stations = {}
with open('nl_popular_radio_stations.csv', mode='r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)  # Skip header row
    for row in reader:
        stations[row[0].strip()] = row[1].strip()

station_names = list(stations.keys())

player = None
is_paused = False

def play_station(url):
    global player, is_paused
    if player is not None:
        player.close_player()
    player = MediaPlayer(url, ff_opts={'vn': True, 'sn': True})
    is_paused = False

def stop_station():
    global player
    if player is not None:
        player.close_player()
        player = None

# 2. Main App Loop
running = True
win = None

while running:
    # --- SCREEN 1: The Dialog Box ---
    info = {'Station': station_names}
    dlg = gui.DlgFromDict(dictionary=info, title='MRI Radio - Select Station', sortKeys=False)
    
    if not dlg.OK:
        running = False
        break
        
    current_idx = station_names.index(info['Station'])
    selected_url = stations[station_names[current_idx]]
    
    # --- SCREEN 2: The Main Window ---
    if win is None:
        win = visual.Window(size=(800, 550), color='#ECECEC', units='norm', title="MRI Radio")
        
        btn_style = {'size': (0.32, 0.13), 'fillColor': '#D3D3D3', 'color': 'black'}
        
        # Row 1: Playback Controls
        btn_play = visual.ButtonStim(win, text="Play", pos=(-0.25, 0.1), **btn_style)
        btn_pause = visual.ButtonStim(win, text="Pause", pos=(0.25, 0.1), **btn_style)
        
        # Row 2: Station Navigation
        btn_prev = visual.ButtonStim(win, text="< Back", pos=(-0.25, -0.15), **btn_style)
        btn_next = visual.ButtonStim(win, text="Next >", pos=(0.25, -0.15), **btn_style)
        
        # Row 3: App Controls
        btn_menu = visual.ButtonStim(win, text="Menu", pos=(-0.25, -0.4), **btn_style)
        btn_exit = visual.ButtonStim(win, text="Exit", pos=(0.25, -0.4), **btn_style)
        
        # Station Title Display
        status_text = visual.TextStim(win, text="", pos=(0, 0.4), color='black', height=0.08, wrapWidth=1.8)

    status_text.text = f"Now Playing: {station_names[current_idx]}"
    
    # --> NEW: Start playing immediately upon selection <--
    play_station(selected_url)
    
    # Inner loop for the visual window
    in_window = True
    while in_window:
        status_text.draw()
        btn_play.draw()
        btn_pause.draw()
        btn_prev.draw()
        btn_next.draw()
        btn_menu.draw()
        btn_exit.draw()
        win.flip()
        
        # Button handlers
        if btn_exit.isClicked or 'escape' in event.getKeys():
            in_window = False
            running = False
            
        elif btn_menu.isClicked:
            # Returns to the drop-down dialog
            in_window = False
            stop_station()
            core.wait(0.2)
            
        elif btn_next.isClicked:
            # Advance to the next station (loops to the start if at the end)
            current_idx = (current_idx + 1) % len(station_names)
            selected_station = station_names[current_idx]
            selected_url = stations[selected_station]
            
            status_text.text = f"Selected: {selected_station}"
            
            # Auto-play if a stream was already active
            if player is not None:
                play_station(selected_url)
            core.wait(0.2)

        elif btn_prev.isClicked:
            # Go back to the previous station (loops to the end if at the start)
            current_idx = (current_idx - 1) % len(station_names)
            selected_station = station_names[current_idx]
            selected_url = stations[selected_station]
            
            status_text.text = f"Selected: {selected_station}"
            
            # Auto-play if a stream was already active
            if player is not None:
                play_station(selected_url)
            core.wait(0.2)
            
        elif btn_play.isClicked:
            if player is not None and is_paused:
                player.set_pause(False)
                is_paused = False
            else:
                play_station(selected_url)
            core.wait(0.2)
            
        elif btn_pause.isClicked:
            if player is not None and not is_paused:
                player.set_pause(True)
                is_paused = True
            core.wait(0.2)

# Clean up
stop_station()
if win is not None:
    win.close()
core.quit()
