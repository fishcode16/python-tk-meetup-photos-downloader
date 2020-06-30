![alt text](https://github.com/fishcode16/python-tk-meetup-photos-downloader/blob/master/images/logo.png "Logo")

# Python/Tk Meetup Photos Downloader / Version 1.1 / xx-xxx-2020 #

## Description ##
Python/Tk Meetup Photos Downloader was created to help you download your meetup events' photos easily.

*Concept/idea was from [Ken Courville](https://github.com/krcourville/meetup-photo-download)'s program, which was no longer functional.*

## Features ##
  * Quick and easy selection of event and photos
    * Event/photos since group creation
    * Able to filter off events with no photos
    * Quick access to event & photo album web page at Meetup
  * Intelligent auto-refresh of cached data
  * High Resolution photos
  * Meetup API version 3

## Developed and tested on ##
  * Python 3.8.0
  * Windows 10 64-bit

## Installation ##
  1. Install Python
  2. Install Python module ($ pip install aiohttp)
  3. Download the application zip file
  4. Unzip
     * __IMPORTANT:__ ensure the folder is not accessible by others

## Configuration ##
  1. Login to [Meetup](https://www.meetup.com/)
  2. Visit [Meetup API](https://www.meetup.com/meetup_api/) website
  3. Apply for your [OAuth Consumers](https://secure.meetup.com/meetup_api/oauth_consumers/) key 
     * __FYI:__ Very likely your application will be rejected unless you have a [Meetup PRO account](https://www.meetup.com/lp/meetup-pro)
  4. Setup your OAuth Consumers
  5. Run *tk-mpd-config.py*
  6. Read the [HOWTO-CONFIG](https://github.com/fishcode16/python-tk-meetup-photos-downloader/blob/master/HOWTO-CONFIG.md)

## Usage ##
  * Run *tk-mpd.py*
  * Select the group
  * Select the event
  * Select the photos
  * Click download

__FYI:__ No scrollbar, use the mouse's scroll wheel :/


### Directories and data files
    .
    ├── config.json                      # application configuration
    ├── access.json                      # your meetup's access token
    ├── download/                        # download folder
    │   └── album-xxxxxxxxx/             # photos for event (xxxxxxxxx event ID)
    │       ├── 00-event.txt             # event information (human readable format)
    │       ├── hires_.....jpeg          # downlaoded photo
    │       └── ...
    ├── group_data/                      # your group information
    │   ├── groups.json                  # your subscribed groups (json downloaded from meetup)
    │   └── gid-xxxxxxxxx/               # group's events & albums information (xxxxxxxxx group's ID)
    │       ├── 00-group.txt             # group information (human readable format)
    │       ├── events-YYYY.json         # yearly events data (YYYY year)
    │       ├── events.json              # recent events data
    │       ├── album-xxxxxxxxx.json     # photo album information (xxxxxxxxx event's ID)
    │       └── ...

    
## Future ##
  * IPTC tag on downloaded photo

___

## Screenshots ##

![alt text](https://github.com/fishcode16/python-tk-meetup-photos-downloader/blob/master/images/screenshot1-1.png "Screenshot 1")

![alt text](https://github.com/fishcode16/python-tk-meetup-photos-downloader/blob/master/images/screenshot1-2.jpg "Screenshot 2")

___

