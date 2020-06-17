# HOWTO obtain your Meetup's access token #

__NOTICE:__ Please note that there are slight difference between the screenshots and the application. I made some changes, but lazy to redo the screenshots. FYI.

___

1. Login to your Meetup account.

2. Visit Meetup API to access your [OAuth Consumers](https://secure.meetup.com/meetup_api/oauth_consumers/).

3. Run tk-mpd-config.py

4. Enter your Key, Secret and Redirect URI information.

![alt text](https://github.com/fishcode16/python-tk-meetup-photos-downloader/blob/master/images/screenshot2-1.png "Screenshot 2-1")

5. Click on "Create Authorization URL" button
   * A "Authorization URL" will be generated. You can either click on the "Open URL" button to send the URL to your web browser or you can paste the URL into your browser address bar.
   * __NOTICE:__ You might be prompt to login to your Meetup account.

![alt text](https://github.com/fishcode16/python-tk-meetup-photos-downloader/blob/master/images/screenshot2-2.png "Screenshot 2-2")

6. If there is no error, you will be redirected to your "Redirect URI" website. Look at your web browser address bar. Copy the "Code" key

![alt text](https://github.com/fishcode16/python-tk-meetup-photos-downloader/blob/master/images/screenshot2-3.png "Screenshot 2-3")

7. Enter the "Code" key and click on "Request for Access Token" button.

![alt text](https://github.com/fishcode16/python-tk-meetup-photos-downloader/blob/master/images/screenshot2-4.png "Screenshot 2-4")

8. You should receive your "access token" and it will be saved onto "access.json" file.

![alt text](https://github.com/fishcode16/python-tk-meetup-photos-downloader/blob/master/images/screenshot2-5.png "Screenshot 2-4")

9. That it! Now you can run tk-mpd.py to download your Meetup's photos.

For more information, visit [Meetup API](https://www.meetup.com/meetup_api/)
