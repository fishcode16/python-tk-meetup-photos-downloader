import tkinter as tk
import tkinter.ttk as ttk
from tkinter import font
from tkinter import PhotoImage

from datetime import datetime
import os
import platform
import json
import requests
import webbrowser
from urllib.parse import urlparse

import aiohttp
import asyncio
import async_timeout

#-------------------------------------------------------------------------
#global variables
version = '1.1'
release_date = '29-Jun-2020'
program_name = 'Python/Tk Meetup Photos Downloader'
github_url = 'https://github.com/fishcode16/python-tk-meetup-photos-downloader'

meetup_api = 'https://api.meetup.com'
selected_year = 'Recent'

logo_b64 = "\
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"
    
#-------------------------------------------------------------------------

def last_updated(file):
    "return the number of hours since the file was last accessed"

    if os.path.exists(file):
        ftime = datetime.fromtimestamp(os.path.getmtime(file))
        hours = round((datetime.now() - ftime).total_seconds() / 3600)
    else:
        hours = -1      #file is missing

    return hours

#-------------------------------------------------------------------------

def need_update(file, max_hr):
    "determine if an update is needed"

    hours = last_updated(file)

    if hours < 0:         #file is missing
        update = 1
    elif hours > max_hr:  #>max_hr
        update = 1
    else:
        update = 0

    return update

#-------------------------------------------------------------------------

def retrieve_token():
    "obtain access token from json file"

    access_file = 'access.json'

    if need_update(access_file, 999999):
        headers = ''

    else:
        data = json.loads((open(access_file).read()))

        #attempt to extract data from json file 
        try:
            headers = {'Authorization': data['token_type'] + ' ' + data['access_token']}
        except:
            headers = ''      #invalid json file content

    return headers

#-------------------------------------------------------------------------

def load_json(meetup_url, params, json_file, max_hr, force_update):
    "retrieve data either from meetup or extract from local file"

    if need_update(json_file, max_hr) or force_update:

        win_ref = popup_status_window('Retrieving...')

        #retrieve data from meetup.com
        r = requests.get(url=meetup_url, headers=headers, params=params)
        data = r.json()

        if r.status_code == 200:
            #save data/json to file
            text_file = open(json_file, 'w')
            text_file.write(json.dumps(data, indent=4))
            text_file.close()
        else:
            print(meetup_url)
            print(params)
            print(str(r.status_code) + ':' + r.reason)
            #print('Header: ' + str(r.headers))
            #print('Text: ' + r.text)

        win_ref.destroy()     #close the popup window

    else:
        data = json.loads((open(json_file).read()))

    return data

#-------------------------------------------------------------------------

def user_profile(force_update):
    "retrieve member's profile, unused"

    meetup_url = meetup_api + '/members/self'
    user_file = 'user.json'
    user_json = load_json(meetup_url, '', user_file, 4320, force_update)

    member_name = user_json['name']

    return member_name

#-------------------------------------------------------------------------

def retrieve_group(force_update):
    "retrieve member's subscribed groups"

    global group_json

    meetup_url = meetup_api + '/self/groups'
    group_file = 'groups.json'
    group_json = load_json(meetup_url, '', group_file, 72, force_update)

    clear_group_frame()
    clear_event_frame()
    clear_album_frame()

    g_list = []
    for x in range(200):  #meetup return 200?
        try:
            #populate the group list / treeview
            g_name    = group_json[x]['name']
            g_country = group_json[x]['localized_country_name']
            g_members = group_json[x]['members']

            g_list.append([g_name, g_country, g_members, x])

            #create group directory (gid)
            g_id     = group_json[x]['id']
            g_folder = 'gid-' + str(g_id)

            if not(os.path.exists(g_folder)):
                os.mkdir(g_folder)

            #create 00-group.txt
            g_readme_file = g_folder + '/00-group.txt'
            if not(os.path.exists(g_folder)):

                #create a text file with the group's information
                text_file = open(g_readme_file, 'w')
                text_file.write('  Group: ' + g_name + '\n')
                text_file.write('Country: ' + g_country + '\n')

                g_created = group_json[x]['created']
                g_created_str = datetime.fromtimestamp(g_created / 1000).strftime('%d-%b-%Y')
                text_file.write('Created: ' + g_created_str + '\n\n')

                today_str = datetime.today().strftime('%H:%M, %d-%b-%Y')
                text_file.write('*this file was created on: ' + today_str)
                text_file.close()

        except:
            break

    g_list.sort()   #sort the group list

    #display list of groups
    for (g_name, g_country, g_members, y) in g_list:
        group_list.insert('', 'end', values=(y, g_name, g_country, g_members))

    #status message
    y = last_updated(group_file)
    msg = str(x) + ' groups | Last updated ' + str(y) + ' hours ago'
    group_status.set(msg)

    return

#---------------------------------------------------------------------------

def clear_group_frame():
    "clear group window"

    global grp_id, grp_name, grp_url

    grp_id = grp_name = grp_url = ''

    #delete the group/treeview data
    for x in group_list.get_children():
        group_list.delete(x)

    return

#---------------------------------------------------------------------------

def group_clicked(event):
    "show which group was selected"

    global grp_id, grp_name, grp_url
    global selected_year

    try:
        #selected item (treeview)
        x = group_list.focus()
        selected_data = group_list.item(x)

        #retrive the needed from array
        g_index        = selected_data['values'][0]
        selected_group = selected_data['values'][1]

        #only do something if the selected is different from current
        if selected_group != grp_name:

            #set global variable for selected group
            grp_id   = group_json[g_index]['id']
            grp_name = group_json[g_index]['name']
            grp_url  = group_json[g_index]['urlname']

            #delete the list
            option_year['menu'].delete(0, 'end')

            #re-populate it. first entry: Recent
            option_year['menu'].add_command(label='Recent', command=tk._setit(var_year, 'Recent', year_clicked))

            #populate, from current year till group creation year
            g_created = group_json[g_index]['created']
            g_created_year = datetime.fromtimestamp(g_created / 1000).year
            current_year = datetime.today().year

            for x in range(current_year, g_created_year - 1, -1):
                option_year['menu'].add_command(label=x, command=tk._setit(var_year, x, year_clicked))

            #if selected_year is before g_created_year, set to 'Recent'
            if selected_year != 'Recent' or selected_year == '':
                if int(selected_year) < g_created_year:
                    selected_year = 'Recent'

            var_year.set(selected_year)

            #update event frame (reset back to "recent")
            retrieve_events(selected_year, 0)

    except:
        pass

    return

#---------------------------------------------------------------------------

def group_r_clicked(event):
    "right click, open meetup page"

    global r_click_url

    x = group_list.identify_row(event.y)
    if x:
        selected_data = group_list.item(x)
        g_index = selected_data['values'][0]
        r_click_url = group_json[g_index]['link']

        #mouse pointer over item
        r_click_popup2.tk_popup(event.x_root, event.y_root, 0)

    return

#---------------------------------------------------------------------------

def retrieve_events(year, force_update):
    "retrive events listing"

    global events_json

    meetup_url = meetup_api + '/' + grp_url + '/events'
    g_folder = 'gid-' + str(grp_id) + '/'

    if year == 'Recent':
        events_file = g_folder + 'events.json'
        params = {
            'status': 'past',
            'page': '15',
            'desc': 'true',
            'fields': 'photo_album'}
        max_hr = 24  #recent event list
    else:
        events_file = g_folder + 'events-' + str(year) + '.json'
        params = {
            'status': 'past',
            'no_earlier_than': str(year) + '-01-01T00:00:00.000',
            'no_later_than': str(year) + '-12-31T23:59:00.000',
            'fields': 'photo_album'}
        max_hr = 4320  #6 months. yearly event list

    events_json = load_json(meetup_url, params, events_file, max_hr, force_update)  #744 hrs = 31 days

    clear_event_frame()
    clear_album_frame()

    chkbox = all_event.get()  #checkbox status

    events_with_photo = 0
    #populate the event listing / treeview
    for x in range(500):  #max 500 per request?
        try:
            e_name = events_json[x]['name'].strip()
            e_id   = events_json[x]['id']

            e_time = events_json[x]['time']
            dt_object = datetime.fromtimestamp(int(e_time) / 1000).strftime('%d-%b-%Y')

            try:
                photo_count = events_json[x]['photo_album']['photo_count']
                taggy = 'have_photo'
                events_with_photo += 1
            except:
                photo_count = 0
                taggy = 'no_photo'

            # if checkbox, then display all events, else only events with photos
            if chkbox or photo_count:
                event_list.insert('', 'end', tags=taggy, values=(x, e_id, dt_object, e_name, photo_count))

        except:
            break

    if not(chkbox):  #if checkbox, then return the count of events with photos
        x = events_with_photo

    event_frame_buttons('normal')

    #status message
    y = last_updated(events_file)
    msg = str(x) + ' events | Last updated ' + str(y) + ' hours ago'
    event_status.set(msg)

    return

#---------------------------------------------------------------------------

def clear_event_frame():
    "clear event window"

    global event_id, event_name, event_time
    global dl_folder

    event_id = event_name = event_time = ''
    dl_folder = ''

    #delete the event/treeview data
    for x in event_list.get_children():
        event_list.delete(x)

    event_frame_buttons('disabled')
    event_status.set('')

    return

#---------------------------------------------------------------------------

def year_clicked(event):
    "refresh event list after user selected a year"

    global selected_year

    x = var_year.get()
    if x != selected_year:
        #update only if selected and current is different
        selected_year = x
        retrieve_events(selected_year, 0)

    return

#---------------------------------------------------------------------------

def event_clicked(event):
    "show which event was selected"

    global event_id, event_name, event_time
    global dl_folder

    try:
        #selected item (treeview)
        x = event_list.focus()
        selected_data = event_list.item(x)

        #retrive the needed from array
        e_index     = selected_data['values'][0]
        e_id        = selected_data['values'][1]
        photo_count = selected_data['values'][4]

        #only do something if the selected is different from current
        if e_id != event_id:

            #set it, global variables
            event_id   = events_json[e_index]['id']
            event_name = events_json[e_index]['name'].strip()
            event_time = events_json[e_index]['time']

            dl_folder = 'photos-' + str(event_id) + '/'

            #if no photos in the event
            if photo_count:
                retrieve_album(0)
            else:
                clear_album_frame()
                album_status.set('No photos')
    except:
        pass

    return

#---------------------------------------------------------------------------

def event_r_clicked(event):
    "right click, open meetup page"

    global r_click_url, r_click_album_url

    x = event_list.identify_row(event.y)
    if x:
        selected_data = event_list.item(x)
        g_index = selected_data['values'][0]
        r_click_url = events_json[g_index]['link']

        try:
            id = events_json[g_index]['photo_album']['id']
            r_click_album_url = 'https://www.meetup.com/' + grp_url + '/photos/all_photos/?photoAlbumId=' + str(id)
            r_click_popup1.entryconfig('Album Page', state='normal')

        except:
            r_click_album_url = ''
            r_click_popup1.entryconfig('Album Page', state='disabled')

        #mouse pointer over item
        r_click_popup1.tk_popup(event.x_root, event.y_root, 0)

    return

#---------------------------------------------------------------------------

def event_frame_buttons(status):
    "enable/disabled all buttons at event_frame"

    event_refresh_btn.configure(state=status)
    option_year.configure(state=status)
    event_checkbox.configure(state=status)

    return

#---------------------------------------------------------------------------

def retrieve_album(force_update):
    "retrieve event photo album"

    global album_json

    #determine refresh, max_hr. based on event date
    #< 1 weeks, 6 hrs
    #1-2 weeks, 3 days (48 hrs)
    #2-4 weeks, 1 week (168 hrs)
    #> 1 month - 2 months (1488 hrs)
    #> 3 months - 6 months (4320 hrs)
    dt_object = datetime.fromtimestamp(event_time / 1000)
    hours = round((datetime.now() - dt_object).total_seconds() / 3600)

    if hours > 2232:  #>3 mths, 6 mths
        #print('Event is older then 3 months')
        max_hr = 4320
    elif hours > 744:  #>1 mth, 2 mths
        #print('Event is older then a month')
        max_hr = 1488
    elif hours > 336:  #>2 wks, 1 wk
        #print('Event is older then 2 weeks')
        max_hr = 168
    elif hours > 168:  #>1 wk, 3 days
        #print('Event is older then a week')
        max_hr = 48
    else:  #<1 wk, 6 hrs
        #print('event is less then a week')
        max_hr = 6

    #retrieve event's photo album
    meetup_url = meetup_api + '/' + grp_url + '/events/' + str(event_id) + '/photos'
    album_file = 'gid-' + str(grp_id) + '/album-' + str(event_id) + '.json'
    album_json = load_json(meetup_url, '', album_file, max_hr, force_update)
   
    clear_album_frame()

    chkbox = all_photo.get()  #checkbox status

    need_dl_count = 0
    for x in range(500):  #max 500 photos per album
        try:
            hires_url = album_json[x]['highres_link']
            photo_file = os.path.basename(hires_url)

            member = album_json[x]['member']['name']

            upload_time = album_json[x]['updated']
            ftime = datetime.fromtimestamp(upload_time / 1000)
            p_date = ftime.strftime('%d-%b-%Y')
            p_time = ftime.strftime('%I:%M %p').lower()

            #highlight photos found in folder
            local_file = dl_folder + photo_file
            if os.path.exists(local_file):
                taggy = 'no_dl'
            else:
                taggy = 'need_dl'
                need_dl_count += 1

            # if checkbox, then display all photos, else only display non-downloaded
            if chkbox or taggy == 'need_dl':
                photo_list.insert('', 'end', tags=taggy, values=(x + 1, photo_file, p_date, p_time, member))

        except:
            break
   
    #disabled the buttons
    album_frame_buttons('disabled')

    #enable the refresh button
    album_refresh_btn.configure(state='normal')
    album_checkbox.configure(state='normal')

    #enable some buttons, if not all files are downloaded
    if need_dl_count:
        album_none_btn.configure(state='normal')
        album_all_btn.configure(state='normal')

    #enable "folder button", if download folder exist
    if os.path.exists(dl_folder):
        album_folder_btn.configure(state='normal')

    #if checkbox is unchecked, display the number of photos that need download
    if not(chkbox):
        x = need_dl_count

    #use "no photos" instead of "0 photos"
    msg = 'No photos'
    if x:
        msg = str(x) + ' photos'
        
    #status message
    y = last_updated(album_file)
    msg = msg + ' | Last updated ' + str(y) + ' hours ago'
    album_status.set(msg)

    return

#---------------------------------------------------------------------------

def clear_album_frame():
    "clear the album/photo list"

    #delete the treeview data
    for x in photo_list.get_children():
        photo_list.delete(x)

    album_frame_buttons('disabled')
    album_status.set('')

    return

#---------------------------------------------------------------------------

def photo_r_clicked(event):
    "right click - open up meetup page. double click - open up local file"

    global r_click_url

    try:
        x = photo_list.identify_row(event.y)
        selected_data = photo_list.item(x)
        index = selected_data['values'][0]
        tags  = selected_data['tags'][0]
        
        if event.num == 3:      #1 = double clicked; 3 = right clicked
            photo_id = album_json[index-1]['id']
            photo_album_id = album_json[index-1]['photo_album']['id']
            r_click_url = 'https://www.meetup.com/' + grp_url + '/photos/' + str(photo_album_id) + '/' + str(photo_id)
            r_click_popup3.tk_popup(event.x_root, event.y_root, 0)

        #proceed only if the file is tag with 'no_dl' (ie. file exist in folder)
        #double click
        elif tags == 'no_dl':
            file = selected_data['values'][1] 
            local_file = cwd + '/' + dl_folder + file
            os.startfile(local_file)    #open the image using default system handler
            
    except:
        pass

    return

#---------------------------------------------------------------------------

def photo_clicked(event):
    "update photo frame, when a photo(s) are selected/unselected"

    x = len(photo_list.selection())

    if x:
        album_download_btn.configure(state='normal')
    else:
        album_download_btn.configure(state='disabled')

    return

#---------------------------------------------------------------------------

def album_frame_buttons(status):
    "enable/disabled all buttons at album_frame"

    album_folder_btn.configure(state=status)
    album_none_btn.configure(state=status)
    album_all_btn.configure(state=status)
    album_download_btn.configure(state=status)
    album_checkbox.configure(state=status)
    album_refresh_btn.configure(state=status)
    
    return

#---------------------------------------------------------------------------

def album_select_all():
    "select all in the photo album"

    for x in photo_list.get_children():
        photo_list.selection_add(x)
        #https://youtu.be/zoLOXN_9EH0

    album_download_btn.configure(state='normal')  #enable download button

    return

#---------------------------------------------------------------------------

def album_select_none():
    "unselect all in the photo album"

    for x in photo_list.get_children():
        photo_list.selection_remove(x)
        #https://youtu.be/zoLOXN_9EH0

    #disable download button, since nothing was selected
    album_download_btn.configure(state='disabled')

    return

#---------------------------------------------------------------------------

def album_download():
    "download the selected photos, called from DL button's command"

    #proceed if there are selections
    if len(photo_list.selection()) > 0:

        #create download folder if needed
        if not(os.path.exists(dl_folder)):
            os.mkdir(dl_folder)

        #create 00-event.txt
        e_readme_file = dl_folder + '00-event.txt'
        if not(os.path.exists(e_readme_file)):        

            #create a text file with the event's information
            text_file = open(e_readme_file, 'w')
            text_file.write('Group: ' + grp_name + '\n')
            text_file.write('Event: ' + event_name + '\n')

            e_dt_str = datetime.fromtimestamp(event_time / 1000).strftime('%H:%M %d-%b-%Y')
            text_file.write(' Date: ' + e_dt_str + '\n\n')

            today_str = datetime.today().strftime('%H:%M, %d-%b-%Y')
            text_file.write('*this file was created on: ' + today_str)
            text_file.close()
                
        #loop through the selections
        dl_list = []
        for idx in photo_list.selection():
            x = photo_list.item(idx)['values'][0] - 1

            hires_url = album_json[x]['highres_link']

            #if image is not found, add to download list
            file = os.path.basename(hires_url)
            local_file = dl_folder + file
            if not(os.path.exists(local_file)):
                dl_list.append(hires_url)

        #download only if there are files to download
        if len(dl_list):
            download_photos(dl_list)  #download the photos

    return

#---------------------------------------------------------------------------

def download_photos(dl_list):
    "download photos in the dl_list"

    #setup download window
    download_win = tk.Toplevel(window)
    download_win.resizable(False, False)
    download_win.overrideredirect(True)

    frame = tk.Frame(download_win, highlightbackground='blue', highlightcolor='blue', highlightthickness=1)
    frame.grid(row=0, column=0)

    download_msg = tk.StringVar()
    label0 = ttk.Label(frame, textvariable=download_msg, anchor='center', width=30)
    label0.grid(row=0, column=0, padx=20, pady=5, sticky='nsew')
    msg = 'Downloading ' + str(len(dl_list)) + ' files'
    download_msg.set(msg)

    download_photos.progress_bar = ttk.Progressbar(frame, orient='horizontal', mode='determinate', value=0)
    download_photos.progress_bar.grid(row=1, column=0, sticky='nsew', padx=10)

    ok_btn = ttk.Button(frame, text='OK', command=download_win.destroy)
    ok_btn.grid(row=2, column=0, sticky='nsew', padx=60, pady=10)
    ok_btn.configure(state='disabled')

    position_window(download_win)

    #---

    #download!
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete( async_dl(loop, dl_list) )

    #---

##    #IPTCinfo when ready
##    #-group, event name, event date/time
##    #-caption, uploaded by, datetime
##    #-comments, tag on image?
##
##    #modify file access/modify time to upload date/time
##    #unable to find a way to modify the file creation date/time
##    photo_date = album_json[x]['created']
##    photo_date = int(photo_date / 1000)
##    os.utime(local_file, (photo_date, photo_date))
    
    #---
    
    download_msg.set('Download completed')
    ok_btn.configure(state='normal')

    download_win.wait_window()          #wait for 'close' of window
    
    window.attributes('-disabled', 0)   #enable the main window
    
    retrieve_album(0)

    return

#---------------------------------------------------------------------------

async def async_dl(loop, dl_list):

    async_dl.count = 0
    async_dl.total = len(dl_list)
    
    async with aiohttp.ClientSession(loop=loop) as session:
        for url in dl_list:
            await download_coroutine(session, url)
            
    return

#---------------------------------------------------------------------------

async def download_coroutine(session, url):

    file = os.path.basename(url)
    local_file = dl_folder + file

    async with async_timeout.timeout(120):
        async with session.get(url) as response:
            with open(local_file, 'wb') as fd:
                async for data in response.content.iter_chunked(1024):
                    fd.write(data)

    #update progress bar
    async_dl.count += 1
    download_photos.progress_bar['value'] = int(async_dl.count / async_dl.total * 100)
    window.update()  #force update?
        
    return

#---------------------------------------------------------------------------

def position_window(win_ref):
    "position toplevel window at the centre of the main window"

    #handle the "x" button on 'window'
    win_ref.protocol('WM_DELETE_WINDOW', win_ref.destroy)

    #position the window at the centre of the app
    x = window.winfo_x()  #current main window x, y
    y = window.winfo_y()

    win_ref.withdraw()  #remove the window, thus removed the flashing most of the time

    win_ref.update()  #force to update w & h
    ab_w = win_ref.winfo_width()  #retrive the 'window' w & h
    ab_h = win_ref.winfo_height()

    x = x + (app_w / 2) - (ab_w / 2)  #calculate the x, y
    y = y + (app_h / 2) - (ab_h / 2)

    win_ref.geometry('+%d+%d' % (x, y))  #position it!
    win_ref.deiconify()  #bring it back
    win_ref.attributes('-topmost', 1)

    window.attributes('-disabled', 1)  #disabled the main window

    win_ref.update()  #force update

    return

#---------------------------------------------------------------------------

def mesg_box(msg_typ, mesg):

    mesgbox_win = tk.Toplevel()
    mesgbox_win.resizable(False, False)
    mesgbox_win.overrideredirect(True)

    #---

    frame = tk.Frame(mesgbox_win, highlightbackground='blue', highlightcolor='blue', highlightthickness=1)
    frame.grid(row=0, column=0)

    #---

    #question,warning,error,information
    label0 = ttk.Label(frame, image='::tk::icons::' + msg_typ)
    label0.grid(row=0, column=0, sticky="nw", padx=10, pady=(10,0))

    label1 = ttk.Label(frame, text=mesg, justify='left')
    label1.grid(row=0, column=1, padx=(0,20), pady=(10,0))
    
    ok_btn = ttk.Button(frame, text='OK', command=mesgbox_win.destroy)
    ok_btn.grid(row=1, column=1, padx=(0,10), pady=10, sticky='e')
    
    position_window(mesgbox_win)

    mesgbox_win.wait_window()  #wait for 'close' of window
    
    window.attributes('-disabled', 0)  #enable the main window
    
    return

#---------------------------------------------------------------------------
def popup_status_window(mesg):
    "display a pop up 'status message' window"
    
    popup_win = tk.Toplevel()
    popup_win.resizable(False, False)
    popup_win.overrideredirect(True)

    frame = tk.Frame(popup_win, highlightbackground="blue", highlightcolor="blue", highlightthickness=1)
    frame.grid(row=0, column=0)
    
    label = tk.Label(frame, text=mesg, padx=25, pady=10)
    label.grid(row=0, column=0, sticky='nsew')

    position_window(popup_win)
    window.attributes('-disabled', 0)  #enable the main window

    window.update()     #force update

    return popup_win

#---------------------------------------------------------------------------

def check_for_update():

    #url = github_url + '/raw/dev/version.txt'
    url = github_url + '/raw/master/version.txt'

    r = requests.get(url)
    data = r.text

    if r.status_code == 200:
        (prog_ver, config_ver) = r.text.split(',')

        if prog_ver > version:
            msg = 'New version available!\n\nVersion ' + str(prog_ver)
        else:
            msg = 'Current version ' + version + '\n\nNo new update available'

        mesg_box('information', msg)
    else:
        msg = str(r.status_code) + ' : ' + r.reason
        mesg_box('error', msg)
        
    return

#---------------------------------------------------------------------------

def debug_info():

    msg = 'Date: ' + \
          '\n> ' + datetime.today().strftime('%d-%b-%Y') + \
          '\n\nPlatform: ' + \
          '\n> ' + platform.machine().lower() + \
          '\n> ' + platform.platform() + \
          '\n\nPython: ' + \
          '\n> ' + platform.python_version() + ' / Tk: ' + str(tk.TkVersion) + \
          '\n> ' + platform.python_build()[0] + \
          '\n> ' + platform.python_build()[1]

    mesg_box('information', msg)
    
    return

#---------------------------------------------------------------------------

def about_window():

    about_win = tk.Toplevel()
    about_win.resizable(False, False)
    about_win.overrideredirect(True)

    #---

    frame = tk.Frame(about_win, highlightbackground='green', highlightcolor='green', highlightthickness=2)
    frame.grid(row=0, column=0)

    #---

    frame0 = ttk.Frame(frame)
    frame0.grid(row=0, column=0)

    logo_img = PhotoImage(data=logo_b64)
    label_logo = ttk.Label(frame0, image=logo_img)
    label_logo.grid(row=0, column=0)

    #---
    
    frame1 = ttk.Frame(frame)
    frame1.grid(row=0, column=1, padx=(0,10), pady=(15,5), sticky='n')

    y = 0
    prog1 = ttk.Label(frame1, text=program_name, anchor='center')
    prog1.grid(row=y, column=0)
    prog1.configure(font=('', 12, 'bold'))

    y += 1
    div1 = ttk.Separator(frame1, orient='horizontal')
    div1.grid(row=y, column=0, sticky='ew', pady=(0,6))

    y += 1
    prog2_0 = ttk.Label(frame1, text='Version: ' + version)
    prog2_0.grid(row=y, column=0, sticky='w', padx=(10,0))

    y += 1
    prog2_1 = ttk.Label(frame1, text='Release Date: ' + release_date)
    prog2_1.grid(row=y, column=0, sticky='w', padx=(10,0))

    y += 1
    ok_btn = ttk.Button(frame1, text='OK', command=about_win.destroy)
    ok_btn.grid(row=y, column=0, pady=(0,5), sticky='e')

    #---

    position_window(about_win)

    about_win.wait_window()             #wait for 'close' of window

    window.attributes('-disabled', 0)   #enable the main window

    return
        
#---------------------------------------------------------------------------

#https://stackoverflow.com/questions/56329342/tkinter-treeview-background-tag-not-working
def fixed_map(option):
    #Fix for setting text colour for Tkinter 8.6.9
    #From: https://core.tcl.tk/tk/info/509cafafae
    #
    #Returns the style map for 'option' with any styles starting with
    #('!disabled', '!selected', ...) filtered out.

    #style.map() returns an empty list for missing options, so this
    #should be future-safe.
    return [elm for elm in style.map('Treeview', query_opt=option) if
            elm[:2] != ('!disabled', '!selected')]
#end-copy







#---------------------------------------------------------------------------
#window layout

window = tk.Tk()
window.title(program_name)
window.resizable(False, False)
window.iconphoto(True, PhotoImage(data=logo_b64))

#---------------------------------------------------------------------------
#window menu

menu = tk.Menu(window)

file_item = tk.Menu(menu, tearoff=0)
file_item.add_command(label='Exit', command=lambda: window.destroy())
menu.add_cascade(label='File', menu=file_item)

help_item = tk.Menu(menu, tearoff=0)
help_item.add_command(label='Website', command=lambda: webbrowser.open(github_url, 1))
help_item.add_command(label='Debug Info', command=debug_info)
help_item.add_command(label='Check for update', command=check_for_update)
help_item.add_separator()
help_item.add_command(label='About', command=about_window)
menu.add_cascade(label='Help', menu=help_item)

cwd = os.getcwd()
menu.add_cascade(label='[' + cwd + ']', command=lambda: os.startfile(cwd))

window.configure(menu=menu)

#---

r_click_popup1 = tk.Menu(window, tearoff=0, fg='blue')
r_click_popup1.add_command(label='Event page', command=lambda: webbrowser.open(r_click_url, 1))
r_click_popup1.add_command(label='Album Page', command=lambda: webbrowser.open(r_click_album_url, 1))

r_click_popup2 = tk.Menu(window, tearoff=0, fg='blue')
r_click_popup2.add_command(label='Group page', command=lambda: webbrowser.open(r_click_url, 1))

r_click_popup3 = tk.Menu(window, tearoff=0, fg='blue')
r_click_popup3.add_command(label='Photo page', command=lambda: webbrowser.open(r_click_url, 1))

#------------------------------------------------------------------
#group area

group_frame = ttk.Frame(window)
group_frame.grid(row=0, column=0, padx=5, pady=5, stick='nw')

#---

lb_header = ['g_index', 'Group', 'Country', 'Members']
group_list = ttk.Treeview(columns=lb_header, show='headings', selectmode='browse', height=6, padding='6 6 6 6')
group_list.grid(row=0, column=0, columnspan=2, in_=group_frame)
group_list.bind('<ButtonRelease-1>', group_clicked)
group_list.bind('<Button-3>', group_r_clicked)

group_list.column('Group', width=310, anchor='w')
group_list.column('Country', width=150, anchor='w')
group_list.column('Members', width=60, anchor='e')
group_list['displaycolumns'] = ('Group', 'Country', 'Members')

for col in lb_header:
    group_list.heading(col, text=col, anchor='w')

group_list.heading('Members', anchor='e')

#---

group_status = tk.StringVar()
group_frame_status = ttk.Label(group_frame, textvariable=group_status, anchor='w')
group_frame_status.grid(row=1, column=0, sticky='nsew')

group_refresh_btn = ttk.Button(group_frame, text='Refresh', command=lambda: retrieve_group(1))
group_refresh_btn.grid(row=1, column=1, sticky='e')

#------------------------------------------------------------------

div1 = ttk.Separator(window, orient='horizontal')
div1.grid(row=1, column=0, sticky='ew', pady=(6,3))

#------------------------------------------------------------------
#event area

event_frame = ttk.Frame(window)
event_frame.grid(row=2, column=0, padx=5, pady=5, stick='nw')

#---

lb_header = ['e_index', 'e_id', 'Date', 'Event', 'Photos']
event_list = ttk.Treeview(columns=lb_header, show='headings', selectmode='browse', height=18, padding='6 6 6 6')
event_list.grid(row=0, column=0, columnspan=4, in_=event_frame)
event_list.bind('<ButtonRelease-1>', event_clicked)
event_list.bind('<Button-3>', event_r_clicked)

event_list.column('Date', width=80, anchor='center')
event_list.column('Event', width=390, anchor='w')
event_list.column('Photos', width=50, anchor='e')
event_list['displaycolumns'] = ('Date', 'Event', 'Photos')

for col in lb_header:
    event_list.heading(col, text=col, anchor='w')

event_list.heading('Photos', anchor='e')

event_list.tag_configure('no_photo', background='#F4F0FE', foreground='grey')

#---

event_status = tk.StringVar()
event_frame_status = ttk.Label(event_frame, textvariable=event_status, anchor='w', width=46)
event_frame_status.grid(row=1, column=0, sticky='nsew')

all_event = tk.IntVar()
all_event.set(1)
event_checkbox = ttk.Checkbutton(event_frame, text='All Events',
                    variable=all_event, onvalue=1, offvalue=0,
                    command=lambda: retrieve_events(selected_year, 0))
event_checkbox.grid(row=1, column=1, sticky='e')
event_checkbox.configure(state='disabled')

var_year = tk.StringVar()
var_year.set('Recent')  #default value
option_year = ttk.OptionMenu(event_frame, var_year, 'Recent', command=year_clicked)
option_year.grid(row=1, column=2, sticky='e')
option_year.configure(state='disabled')

event_refresh_btn = ttk.Button(event_frame, text='Refresh',
                        command=lambda: retrieve_events(selected_year, 1))
event_refresh_btn.grid(row=1, column=3, sticky='e')
event_refresh_btn.configure(state='disabled')

#------------------------------------------------------------------
#photo album area

album_frame = ttk.Frame(window)
album_frame.grid(row=0, column=1, rowspan=3, padx=5, pady=4, sticky='nw')

#---

y=0
album_folder_btn = ttk.Button(album_frame, text='DL folder',
                        command=lambda: os.startfile(os.path.realpath(dl_folder)))
album_folder_btn.grid(row=y, column=0, sticky='nsew')
album_folder_btn.configure(state='disabled')

album_none_btn = ttk.Button(album_frame, text='Clear all', command=album_select_none)
album_none_btn.grid(row=y, column=1, sticky='nsew')
album_none_btn.configure(state='disabled')

album_all_btn = ttk.Button(album_frame, text='Select all', command=album_select_all)
album_all_btn.grid(row=y, column=2, sticky='nsew')
album_all_btn.configure(state='disabled')

album_download_btn = ttk.Button(album_frame, text='Download', command=album_download)
album_download_btn.grid(row=y, column=3, sticky='nsew')
album_download_btn.configure(state='disabled')

#---

y += 1
lb_header = ['No', 'Photo', 'Date', 'Time', 'Uploaded by']
photo_list = ttk.Treeview(columns=lb_header, show='headings',
                        selectmode='extended', height=27, padding='6 6 6 6')
photo_list.grid(row=y, column=0, columnspan=4, in_=album_frame)
photo_list.bind('<ButtonRelease-1>', photo_clicked)
photo_list.bind('<Button-3>', photo_r_clicked)
photo_list.bind('<Double-Button-1>', photo_r_clicked)

photo_list.column('No', width=40, anchor='e')
photo_list.column('Photo', width=160, anchor='center')
photo_list.column('Date', width=90, anchor='center')
photo_list.column('Time', width=90, anchor='center')
photo_list.column('Uploaded by', width=100, anchor='center')

for col in lb_header:
    photo_list.heading(col, text=col)

photo_list.tag_configure('no_dl', background='#F4F0FE', foreground='grey')

#---

y += 1
album_status = tk.StringVar()
album_frame_status = ttk.Label(album_frame, textvariable=album_status, anchor='w')
album_frame_status.grid(row=y, column=0, columnspan=2, sticky='nsew')

all_photo = tk.IntVar()
all_photo.set(1)
album_checkbox = ttk.Checkbutton(album_frame, text='All Photos',
                        variable=all_photo, onvalue=1, offvalue=0,
                        command=lambda: retrieve_album(0))
album_checkbox.grid(row=y, column=2, sticky='e')
album_checkbox.configure(state='disabled')

album_refresh_btn = ttk.Button(album_frame, text='Refresh',
                        command=lambda: retrieve_album(1))
album_refresh_btn.grid(row=y, column=3, sticky='e')
album_refresh_btn.configure(state='disabled')

#------------------------------------------------------------------

#https://stackoverflow.com/questions/56329342/tkinter-treeview-background-tag-not-working
style = ttk.Style()
style.map('Treeview', foreground=fixed_map('foreground'), background=fixed_map('background'))
#end-copy

style.configure('Treeview.Heading', foreground='blue')

#---

#postion main window in the middle of the screen
ws = window.winfo_screenwidth()     #width of the screen
hs = window.winfo_screenheight()    #height of the screen

#remove window; to reduce window flashing due to reposition (most of the time)
window.withdraw()

window.update()  #force update, to update window w & h
app_w = window.winfo_width()    #retrieve window w & h
app_h = window.winfo_height()

x = (ws / 2) - (app_w / 2)      #calculate the x, y
y = (hs / 2) - (app_h / 2)

window.geometry('+%d+%d' % (x, y))  #position it!
window.deiconify()          #bring up the window



#------------------------------------------------------------------
#main

headers = retrieve_token()  #set header (access token)
if headers == '':
    msg = 'Unable to retrieve access token.\n\nplease run "tk-mpd-config.py"'
    mesg_box('error', msg)
    window.destroy()
else:
    #member_name = user_profile(0)
    retrieve_group(0)

    window.mainloop()
