![alt text](https://github.com/fishcode16/python-tk-meetup-photos-downloader/blob/master/images/logo.png "Logo")

# Python/Tk Meetup Photos Downloader / 14-Jun-2020 #

## Description ##
Python/Tk Meetup Photos Downloader was created to help you download your meetup events' photos easily.

I decided to write this program during the COVID-19 lockdown (~March 2020).  Concept/idea is from [Ken Courville](https://github.com/krcourville/meetup-photo-download)'s program, which was no longer functioning. 

## Features ##
  * Quick and easy selection of event and photos
    * Event/photos from the start of the group
    * Highlight events with no photos
  * Intelligent auto-refresh of data
  * High Resolution photos
  * Meetup API version 3

## Developed and tested on ##
  * Python 3.8.0
  * Windows 10 64-bit

## Installation ##
  * Install Python
  * Download zip file and extract to your local hard disk
  * no special permission needed

## Configuration ##
  * Login to your meetup's account
  * Visit https://www.meetup.com/meetup_api/
  * Apply for your 'OAuth Consumers' key 

## Usage ##
  * Run tk-meetup-dl.py
    * first time running, would guide you through to obtain your 'access token'
  * Select the group
  * Select the event
  * Select the photos
  * Click download 

## Notes ##
  * All downloaded content and cache file are located in the application directory
  * Important files:
    * access.json (your meetup's access token json)
    * groups.json (information about your subscribed group)
    * gid-xxxxx (group directory. Events & albums information for the group are stored here)
      * events-YYYY (meetup event json)
      * album-xxxxx (meetup photo album json)

## Future ##
  * Asyncio download
  * IPTC tag on downloaded photo

## Screenshot ##
![alt text](https://github.com/fishcode16/python-tk-meetup-photos-downloader/blob/master/images/screenshot1.png "Screenshot 1")
