# HOWTO obtain your Meetup's access token #

1. Login to your Meetup account.

2. Visit Meetup API to access your [OAuth Consumers](https://secure.meetup.com/meetup_api/oauth_consumers/).

3. Run tk-mpd-config.py

4. Enter your Key, Secret and Redirect URI information.
![alt text](https://github.com/fishcode16/python-tk-meetup-photos-downloader/blob/master/images/screenshot2-1.png "Screenshot 2-1")

5. Click on "Create Authorization URL" button
A "Authorization URL" will be generated. You can either click on the "Open URL" button to send the URL to your web browser or you can paste the URL into your browser address bar.
__NOTICE__ You might be prompt to login to your Meetup account, if the browser is unable to.
![alt text](https://github.com/fishcode16/python-tk-meetup-photos-downloader/blob/master/images/screenshot2-2.png "Screenshot 2-2")

6. If there is no error, you will be redirected to your "Redirect URI" website.

7. Look at your web browser address bar. Copy the "Code" key
![alt text](https://github.com/fishcode16/python-tk-meetup-photos-downloader/blob/master/images/screenshot2-3.jpg "Screenshot 2-3")

8. Enter the "Code" key and click on "Request for Access Token" button.
![alt text](https://github.com/fishcode16/python-tk-meetup-photos-downloader/blob/master/images/screenshot2-4.png "Screenshot 2-4")

9. You should receive your "access token" and it will be saved onto "access.json" file.
![alt text](https://github.com/fishcode16/python-tk-meetup-photos-downloader/blob/master/images/screenshot2-5.png "Screenshot 2-4")

10. That it! Now you can run tk-mpd.py to download your Meetup's photos.

For more information, visit [Meetup API](https://www.meetup.com/meetup_api/)