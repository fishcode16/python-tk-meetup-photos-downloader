![alt text](https://github.com/fishcode16/python-tk-meetup-photos-downloader/blob/master/images/logo.png "Logo")

# Python/Tk Meetup Photos Downloader / 14-Jun-2020 #

## Description ##
Python/Tk Meetup Photos Downloader was created to help you download your meetup events' photos easily.

## Features ##
  * Quick and easy selection of event and photos
    * Event/photos since group creation
    * Able to filter off events with no photos
    * Quick access to meetup event's web page
  * Intelligent auto-refresh of data
  * High Resolution photos
  * Meetup API version 3

## Developed and tested on ##
  * Python 3.8.0
  * Windows 10 64-bit

*I developed this during the COVID-19 lockdown (~April 2020). Concept/idea was from [Ken Courville](https://github.com/krcourville/meetup-photo-download)'s program, which was no longer functional.* 

## Installation ##
  1. Install Python
  2. Download zip file
  3. Extract zip file

## Configuration ##
  * Login to [Meetup](https://www.meetup.com/)
  * Visit [Meetup API](https://www.meetup.com/meetup_api/) website
  * Apply for your [OAuth Consumers](https://secure.meetup.com/meetup_api/oauth_consumers/) key 
    * __NOTICE:__ Very likely your application will be rejected unless you have a [Meetup PRO account](https://www.meetup.com/lp/meetup-pro)

## Usage ##
  * Run tk-meetup-dl.py
    * first time running would guide you through to obtain your 'access token'
  * Select the group
  * Select the event
  * Select the photos
  * Click download 

## Notes ##
  * All downloaded content and cache file are located in the application directory
  * Important files:
    * access.json (your meetup's access token)
    * user.json (your user information)
    * groups.json (your subscribed group)
    * gid-xxxxxxxxx/ (group directory. group's events & albums information stored here)
      * events-YYYY.json (year's events)
      * events.json (recent events)
      * album-xxxxxxxxx.json (photo album information)

## Future ##
  * asyncio download
  * IPTC tag on downloaded photo

## Screenshot ##
![alt text](https://github.com/fishcode16/python-tk-meetup-photos-downloader/blob/master/images/screenshot1.png "Screenshot 1")
