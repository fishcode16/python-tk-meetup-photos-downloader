import tkinter as tk
import tkinter.ttk as ttk
from tkinter import font
from tkinter import PhotoImage

import datetime
import os
import platform
import json
import requests
import webbrowser
from urllib.parse import urlparse


#-------------------------------------------------------------------------
#global variables
version = '1.1'
release_date = '22-Jun-2020'
program_name = 'Python/Tk Meetup Photos Downloader'
github_url = 'https://github.com/fishcode16/python-tk-meetup-photos-downloader'

meetup_api = 'https://api.meetup.com'
selected_year = 'Recent'


#-------------------------------------------------------------------------

def last_updated(file):
    "return the number of hours since the file was last accessed"

    if os.path.exists(file):
        ftime = datetime.datetime.fromtimestamp(os.path.getmtime(file))
        hours = round((datetime.datetime.now() - ftime).total_seconds() / 3600)
    else:
        hours = -1

    return hours

#-------------------------------------------------------------------------

def need_update(file, max_hr):
    "determine if an update is needed"

    hours = last_updated(file)

    if hours < 0:  #file is missing
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

        try:
            headers = {'Authorization': data['token_type'] + ' ' + data['access_token']}
        except:
            headers = ''

    return headers

#-------------------------------------------------------------------------

def load_json(meetup_url, params, json_file, max_hr, force_update):
    "retrieve data either from meetup or from local file"

    if need_update(json_file, max_hr) or force_update:
        r = requests.get(url=meetup_url, headers=headers, params=params)
        data = r.json()

        if r.status_code == 200:
            #save data/json to file
            text_file = open(json_file, 'w')
            text_file.write(json.dumps(data, indent=4))
            text_file.close()
        else:
            print('Staus Code: ' + str(r.status_code))
            print('Reason: ' + r.reason)
            #print('Header: ' + str(r.headers))
            #print('Text: ' + r.text)

    else:
        data = json.loads((open(json_file).read()))

    return data

#-------------------------------------------------------------------------

def user_profile(force_update):
    "retrieve member's profile"

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
            g_id   = group_json[x]['id']
            g_path = 'gid-' + str(g_id)

            if not (os.path.exists(g_path)):
                os.mkdir(g_path)

                g_created = group_json[x]['created']
                g_created_str = datetime.datetime.fromtimestamp(g_created / 1000).strftime('%d-%b-%Y')
                today_str = datetime.datetime.today().strftime('%H:%M, %d-%b-%Y')

                g_readme_file = g_path + '/00-group-name.txt'
                #create a text file with the group's information
                text_file = open(g_readme_file, 'w')
                text_file.write('  Group: ' + g_name + '\n')
                text_file.write('Country: ' + g_country + '\n')
                text_file.write('Created: ' + g_created_str + '\n')
                text_file.write('\n')
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
            g_created_year = datetime.datetime.fromtimestamp(g_created / 1000).year
            current_year = datetime.datetime.today().year

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
    event_path = 'gid-' + str(grp_id) + '/'

    if year == 'Recent':
        events_file = event_path + 'events.json'
        params = {
            'status': 'past',
            'page': '15',
            'desc': 'true',
            'fields': 'photo_album'}
        max_hr = 24  #recent event list
    else:
        events_file = event_path + 'events-' + str(year) + '.json'
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
            dt_object = datetime.datetime.fromtimestamp(int(e_time) / 1000).strftime('%d-%b-%Y')

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

    event_id = event_name = event_time = ''

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

            event_id   = events_json[e_index]['id']
            event_name = events_json[e_index]['name'].strip()
            event_time = events_json[e_index]['time']

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
    dt_object = datetime.datetime.fromtimestamp(event_time / 1000)
    hours = round((datetime.datetime.now() - dt_object).total_seconds() / 3600)

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
            photo = album_json[x]['id']
            photo_filename = 'highres_' + str(photo) + '.jpeg'

            member = album_json[x]['member']['name']

            upload_time = album_json[x]['updated']
            ftime = datetime.datetime.fromtimestamp(upload_time / 1000)
            p_date = ftime.strftime('%d-%b-%Y')
            p_time = ftime.strftime('%I:%M %p').lower()

            #highlight photos found in folder
            p_path = str(event_id) + '/' + photo_filename
            if os.path.exists(p_path):
                taggy = 'no_dl'
            else:
                taggy = 'need_dl'
                need_dl_count += 1

            # if checkbox, then display all photos, else only display non-downloaded
            if chkbox or taggy == 'need_dl':
                photo_list.insert('', 'end', tags=taggy, values=(x + 1, photo_filename, p_date, p_time, member))

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

    #enable "folder button", if folder exist
    if os.path.exists(str(event_id)):
        album_folder_btn.configure(state='normal')

    #if checkbox is unchecked, display the number of photos that need download
    if not(chkbox):
        x = need_dl_count

    #use "no photos" instead of "0 photos"
    if x:
        msg = str(x) + ' photos'
    else:
        msg = 'No photos'
        
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
    "right click, open allow user to delete the photo from local folder"

    global req_file_to_delete

    try:
        x = photo_list.identify_row(event.y)
        selected_data = photo_list.item(x)
        tag = selected_data['tags'][0]

        #pop up menu, only if the file is tag with 'no_dl' (ie. file exist in folder)
        if tag == 'no_dl':
            req_file_to_delete = selected_data['values'][1]
            r_click_popup3.tk_popup(event.x_root, event.y_root, 0)
            #popup button will call delete_local_file
    except:
        pass

    return

#---------------------------------------------------------------------------

def delete_local_file():
    "delete the photo from the folder"

    local_file = str(event_id) + '/' + req_file_to_delete
    #if file exist, delete (should exist, else won't end up here)
    if os.path.exists(local_file):
        os.remove(local_file)
        retrieve_album(0)

    return

#---------------------------------------------------------------------------

def photo_clicked(event):
    "update photo frame, when a photo(s) are selected/unselected"

    x = len(photo_list.selection())

    if x:
        album_download_btn.configure(state='normal')
    else:
        album_download_btn.configure(state='disabled')

    #report number of photos downloaded, future

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
    "download the selected photos, called from button's command"

    dl_list = []
    if len(photo_list.selection()) > 0:
        for x in photo_list.selection():
            dl_list.append(photo_list.item(x)['values'][0] - 1)

        download_photos(dl_list)  #download the photos

    return

#---------------------------------------------------------------------------

def download_photos(dl_list):
    "download photos in the dl_list"

    #setup download window
    download_win = tk.Toplevel(window)
    download_win.title('Download Status')
    download_win.resizable(False, False)

    msg_box = tk.Text(download_win, height=16, width=42)
    msg_box.grid(row=0, column=0, padx=10, pady=10)
    msg_box.tag_configure('err', background='red', foreground='white')
    msg_box.tag_configure('ok', foreground='green')
    msg_box.tag_configure('sum', foreground='blue')

    progress_bar = ttk.Progressbar(download_win, orient='horizontal', mode='determinate', value=0)
    progress_bar.grid(row=1, column=0, sticky='nsew', padx=20)

    ok_btn = ttk.Button(download_win, text='OK', command=download_win.destroy)
    ok_btn.grid(row=2, column=0, sticky='nsew', padx=10, pady=10)
    ok_btn.configure(state='disabled')

    position_window(download_win)

    #---
    
    #display number of files to download
    total = len(dl_list)
    photo_count = album_json[0]['photo_album']['photo_count']
                                
    msg_text = str(photo_count) + ' photos in event\'s photo album\n' + \
               str(total) + ' photos was selected for download\n\n' + \
               '---Downloading---\n'
    msg_box.insert('end', msg_text, 'sum')
    
    window.update()     #force update

    #---

    #create download folder if needed
    dl_folder = str(event_id) + '/'
    if not (os.path.exists(dl_folder)):
        os.mkdir(dl_folder)

    #---
        
    count = 0
    dl_count = 0
    for x in dl_list:  #max 500 photos per album

        photo = album_json[x]['id']
        photo_filename = 'highres_' + str(photo) + '.jpeg'

        msg_box.insert('end', '[{:3d}] '.format(x + 1) + photo_filename + ' - ')
        window.update()

        local_file = dl_folder + photo_filename
        if not(os.path.exists(local_file)):

            #download the photo
            hires_link = album_json[x]['highres_link']
            r = requests.get(url=hires_link)
            if r.status_code == 200:

                msg_box.insert('end', 'done\n', 'ok')

                #write content/image to disk
                with open(local_file, 'wb') as fd:
                    for chunk in r.iter_content(chunk_size=128):
                        fd.write(chunk)
                fd.close()

                #IPTCinfo when ready

                #modify file access/modify time to upload date/time
                #unable to find a way to modify the file creation date/time
                photo_date = album_json[x]['created']
                photo_date = int(photo_date / 1000)
                os.utime(local_file, (photo_date, photo_date))

                dl_count += 1

            else:
                msg_text = 'err: ' + str(r.status_code) + ':' + r.reason + '\n'
                msg_box.insert('end', msg_text, 'err')

        else:
            pass
            msg_box.insert('end', 'skipped\n')

        msg_box.see('end')  #auto scroll text up

        #update progress bar
        count += 1
        progress_bar['value'] = int(count / total * 100)
        window.update()  #force update?

    msg_box.insert('end', 'Download completed\n\n', 'ok')

    #---
    
    #display summary
    msg_text = '---Summary---\n' + \
               'Download folder: ' + dl_folder + '\n' + \
               str(dl_count) + ' photos downloaded'
    msg_box.insert('end', msg_text, 'sum')
    msg_box.see('end')  #auto scroll text up
    msg_box.configure(state='disabled')

    #---

    ok_btn.configure(state='normal')

    download_win.wait_window()  #wait for 'close' of window
    window.attributes('-disabled', 0)  #enable the main window

    retrieve_album(0)

    return

#---------------------------------------------------------------------------

def about_window():

    logo_b64 = "\
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\
tiViwvjbAAAAAElFTkSuQmCC" 

    about_win = tk.Toplevel()
    about_win.title('About')
    about_win.resizable(False, False)

    #---

    frame0 = ttk.Frame(about_win)
    frame0.grid(row=0, column=0, padx=10, pady=5)

    logo_img = PhotoImage(data=logo_b64)
    label_logo = ttk.Label(frame0, image=logo_img)
    label_logo.grid(row=0, column=0, pady=8)

    #---
    
    frame1 = ttk.Frame(about_win)
    frame1.grid(row=0, column=1, padx=(0,10), pady=(15,5), sticky='n')

    y = 0
    prog1 = ttk.Label(frame1, text=program_name, anchor='center')
    prog1.grid(row=y, column=0, columnspan=2)
    prog1.configure(font=('', 12, 'bold'))

    y += 1
    div1 = ttk.Separator(frame1, orient='horizontal')
    div1.grid(row=y, column=0, columnspan=2, sticky='ew', pady=6)

    y += 1
    prog2_0 = ttk.Label(frame1, text='Version: ' + version, foreground='blue')
    prog2_0.grid(row=y, column=0, sticky='w')
    prog2_0.configure(font=('', 11))
    prog2_1 = ttk.Label(frame1, text='Release Date: ' + release_date, foreground='blue')
    prog2_1.grid(row=y, column=1, sticky='e')
    prog2_1.configure(font=('', 11))

    y += 1
    ok_btn = ttk.Button(frame1, text='OK', command=about_win.destroy)
    ok_btn.grid(row=y, column=0, columnspan=2, pady=(14,0), sticky='nsew')

    #---

    position_window(about_win)

    about_win.wait_window()  #wait for 'close' of window
    window.attributes('-disabled', 0)  #enable the main window

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
    ab_w = win_ref.winfo_width()  #retreive the 'window' w & h
    ab_h = win_ref.winfo_height()

    x = x + (app_w / 2) - (ab_w / 2)  #calculate the x, y
    y = y + (app_h / 2) - (ab_h / 2)

    win_ref.geometry('+%d+%d' % (x, y))  #position it!
    win_ref.deiconify()  #bring it back

    window.attributes('-disabled', 1)  #disabled the main window

    return

#---------------------------------------------------------------------------

def check_for_update():

    url = github_url + '/raw/master/version.txt'
    url = github_url + '/raw/dev/version.txt'

    r = requests.get(url)
    data = r.text

    if r.status_code == 200:
        (prog_ver, config_ver) = r.text.split(',')

        if prog_ver > version:
            msg = 'New version available!\n\nVersion ' + str(prog_ver)
            mesg_box('information', 'Status', msg)

        else:
            mesg_box('information', 'Status', 'No new update available')
    else:
        msg = str(r.status_code) + ' : ' + r.reason
        mesg_box('error', 'http error', msg)
        
    return

#---------------------------------------------------------------------------

def debug_info():

    msg = 'Platform: ' + platform.machine().lower() + \
          '\n: ' + platform.platform() + \
          '\n\nPython: ' + platform.python_version() + \
          ' / Tk: ' + str(tk.TkVersion) + \
          '\n: ' + platform.python_build()[0] + \
          '\n: ' + platform.python_build()[1]

    mesg_box('information', 'Debug Info', msg)
    
    return

#---------------------------------------------------------------------------

def mesg_box(msg_typ, title, mesg):

    mesgbox_win = tk.Toplevel()
    mesgbox_win.title(title)
    mesgbox_win.resizable(False, False)
    
    #---

    frame = ttk.Frame(mesgbox_win)
    frame.grid(row=0, column=0, padx=20, pady=10)

#    ttk.Label(frame, image="::tk::icons::question")
#    ttk.Label(frame, image="::tk::icons::warning")
#    ttk.Label(frame, image="::tk::icons::error")
#    ttk.Label(frame, image="::tk::icons::information")

    icon = '::tk::icons::' + msg_typ
    
    label0 = ttk.Label(frame, image=icon)
    label0.grid(row=0, column=0, sticky="nw")

    label1 = ttk.Label(frame, text=mesg, justify='left')
    label1.grid(row=0, column=1, padx=10)
    
    ok_btn = ttk.Button(frame, text='OK', command=mesgbox_win.destroy)
    ok_btn.grid(row=1, column=0, columnspan=2, pady=(10,5), sticky='ew')
    
    position_window(mesgbox_win)

    mesgbox_win.wait_window()  #wait for 'close' of window
    
    window.attributes('-disabled', 0)  #enable the main window
    
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

#menu.add_cascade(label=30*' ')   #spacer

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
r_click_popup3.add_command(label='Delete local file', command=delete_local_file)


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

event_refresh_btn = ttk.Button(event_frame, text='Refresh', command=lambda: retrieve_events(selected_year, 1))
event_refresh_btn.grid(row=1, column=3, sticky='e')
event_refresh_btn.configure(state='disabled')

#------------------------------------------------------------------
#photo album area

album_frame = ttk.Frame(window)
album_frame.grid(row=0, column=1, rowspan=3, padx=5, pady=4, sticky='nw')

#---

y=0
album_folder_btn = ttk.Button(album_frame, text='DL folder', command=lambda: os.startfile(os.path.realpath(str(event_id))))
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
photo_list = ttk.Treeview(columns=lb_header, show='headings', selectmode='extended', height=27, padding='6 6 6 6')
photo_list.grid(row=y, column=0, columnspan=4, in_=album_frame)
photo_list.bind('<ButtonRelease-1>', photo_clicked)
photo_list.bind('<Button-3>', photo_r_clicked)

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

album_refresh_btn = ttk.Button(album_frame, text='Refresh', command=lambda: retrieve_album(1))
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
ws = window.winfo_screenwidth()  #width of the screen
hs = window.winfo_screenheight()  #height of the screen

window.withdraw()  #remove window, to reduce window flashing due reposition most of the time

window.update()  #force update, to update window w & h
app_w = window.winfo_width()  #retreive window w & h
app_h = window.winfo_height()

x = (ws / 2) - (app_w / 2)  #calculate the x, y
y = (hs / 2) - (app_h / 2)

window.geometry('+%d+%d' % (x, y))  #position it!
window.deiconify()  #bring up the window


#------------------------------------------------------------------
#main

headers = retrieve_token()  #set header (access token)
if headers == '':
    msg = 'Unable to retreive access token!!\n\nplease run "tk-mpd-config.py"'
    mesg_box('error', 'Error', msg)
    window.destroy()
else:

    #member_name = user_profile(0)

    retrieve_group(0)

    window.mainloop()
