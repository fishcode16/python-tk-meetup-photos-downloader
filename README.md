![alt text](https://github.com/fishcode16/python-tk-meetup-photos-downloader/blob/master/images/logo.png "Logo")

# Python/Tk Meetup Photos Downloader / Version 1.2 / (In development) #

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

## Developed on ##
  * Python 3.8.0 (32-bit)
  * Windows 10 (64-bit)

## Tested on ##
  * Python 3.8.0 (32-bit)
  * Python 3.8.5 (32-bit)
  * Python 3.8.6 (32-bit)
  * Python 3.9.0 (32-bit)

## Installation ##
  1. Install [Python](https://www.python.org/)
  2. Install Python module
     * $ pip install urllib3
     * $ pip install aiohttp[speedups]
  3. Download the application zip file
  4. Unzip
     * __IMPORTANT:__ ensure the folder is only accessible by the user

## Configuration ##
  1. Login to [Meetup](https://www.meetup.com/)
  2. Visit [Meetup API](https://www.meetup.com/meetup_api/) website
  3. Apply for your [OAuth Consumers](https://secure.meetup.com/meetup_api/oauth_consumers/) key 
     * __FYI:__ Very likely your application will be rejected unless you have a [Meetup PRO account](https://www.meetup.com/lp/meetup-pro)
  4. Setup your OAuth Consumers
  5. Run *tk-mpd-config.pyw*
  6. Read the [HOWTO-CONFIG](https://github.com/fishcode16/python-tk-meetup-photos-downloader/blob/master/HOWTO-CONFIG.md)

## Usage ##
  * Run *tk-mpd.pyw*
  * Select the group
  * Select the event
  * Select the photos
  * Click download

### Directories and data files
    .
    ├── config.json                      # application configuration
    ├── access.json                      # your meetup's access token
    ├── download/                        # download folder
    │   └── album-xxxxxxxxx/             # photos for event (xxxxxxxxx event ID)
    │       ├── 00-event.txt             # event information (human readable format)
    │       ├── 00-photos.txt            # photos index of the album (uploader, date/time)
    │       ├── hires_.....jpeg          # downlaoded photo
    │       └── ...
    ├── group_data/                      # your group information
    │   ├── groups.json                  # your subscribed groups (json downloaded from meetup)
    │   └── gid-xxxxxxxxx/               # group's events & albums information (xxxxxxxxx group's ID)
    │       ├── 00-group.txt             # group information (human readable format)
    │       ├── events-YYYY.json         # yearly events data (YYYY year)
    │       ├── events-Recent.json       # recent events data
    │       ├── album-xxxxxxxxx.json     # photo album information (xxxxxxxxx event's ID)
    │       └── ...

    
## Future ##
  * IPTC tag on downloaded photo

___

## Screenshots ##

![alt text](https://github.com/fishcode16/python-tk-meetup-photos-downloader/blob/master/images/screenshot1-1.png "Screenshot 1")

![alt text](https://github.com/fishcode16/python-tk-meetup-photos-downloader/blob/master/images/screenshot1-2.jpg "Screenshot 2")

___

