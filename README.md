# Robocalypse code

Code and system configuration for my 2024 Halloween costume.  It's a cardboard box robot costume that has a LED and button panel on the front and is equipped with a voice changer/audio playback.


## Components

1. Raspberry Pi 4
1. Cheap USB Audio device to provide microphone ([zdyCGTime Hi-Speed USB 2.0 7.1-Channel Virtual USB 3D Stereo Audio Adapter](https://www.amazon.com/dp/B083V3JGMF) - [info](hardware_info/usb_audio.txt))
1. [QuinLED Dig-Uno](https://quinled.info/quinled-dig-uno/)
1. 5v individually addressable LED string
1. 26800 mAH battery pack
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

1. Create a WLAN Hotspot for the WLED to connect to.  Make sure the subnet is small enough that the IP for the Dig-Uno is predictable.
    [Hotspot Config](images/hotspot_config.png)

1. Configure the Dig-Uno to connect to the hotspot Wifi.

## WLED Configuration

There's several segments used in WLED to control lights.  Most are light corresponding to buttons to indicate what is "active".

| Segment name | # Lights | Function |
| --- | --- | --- |
| `red_button` | 1 | Light indicating that red button is active |
| `blue_button` | 1 | Light indicating that blue button is active |
| `r_white_button` | 1 | Light indicating that right white button is active |
| `green_button` | 1 | Light indicating that green button is active |
| `field` | 16 | 4x4 grid of lights to indicate activity |
| `l_white_button` | 1 | Light indicating that left white button is active |
| `black_button` | 1 | Light indicating that black button is active |
| `yellow_button` | 1 | Light indicating that yellow button is active |
| `shoulders` | 2 | Lights on the shoulders |
| `nose` | 1 | The "nose" light |
| `eye_bar` | 6 | The lights making up the eye bar |
| `top` | 1 | Light on the top of the head |

## Button functions

There are 7 buttons on the unit.  These are the rough functions.

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

## References

- [Using a Raspberry Pi as a Realtime Voice Changer For Halloween](https://planet-geek.com/2015/10/29/hacks/using-a-raspberry-pi-as-a-realtime-voice-changer-for-halloween/)
- [How to make robot or Dalek voice using SoX library?](https://stackoverflow.com/questions/29957719/how-to-make-robot-or-dalek-voice-using-sox-library)
- [Microphone/speaker system using SoX](https://forums.raspberrypi.com/viewtopic.php?t=322534)