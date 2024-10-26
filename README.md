# Robocalypse code

## Components

1. Raspberry Pi
1. Cheap USB Audio device to provide microphone
1. Dig-Uno
1. 5v individually addressable LED string
1. Several battery packs
1. Buttons
1. Pyle PWMA50B portable PA

## System Setup

1. Installs:
   ```sudo apt update
   sudo apt dist-upgrade
   sudo apt install sox libsox-fmt-mp3 alsa-tools alsaplayer-text
   ```

1. Configure system to use USB Audio as default via `raspi-config`

1. Enable SSH

1. Install `git` certifcates to talk to internal Git repo properly

## Button functions

| Button | Press Type | Action |
|---|---|---|
| Red | Short | Reset to breathe effect |
| Blue | Short | Play/Stop Mr. Roboto |
| Left White | Short | Play/Stop walking sound |
| Green | Short | Play/Stop Thriller |
| Yellow | Short | Activate/Deactivate voice changes |
| Black | Short | Play/Stop fart sounds |
| Right White | Short | Play/Stop thinking sound |
| Right White | Long Press | Turn Headlights on |

At start-up, only the red button will be activated.  This allows for a wait until the WLED box is booted and available.  Press the red button to initialize the lights and enable the rest of the buttons.
