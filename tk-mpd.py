import tkinter as tk
import tkinter.ttk as ttk
from tkinter import font
from tkinter import PhotoImage
from tkinter import messagebox

import datetime
import os
import sys
import json
import requests
import webbrowser
from urllib.parse import urlparse


#-------------------------------------------------------------------------
#global variables
version = '1.01'
release_date = '16-Jun-2020'
script_name = 'Python/Tk Meetup Photos Downloader'
github_url = 'https://github.com/fishcode16/python-tk-meetup-photos-downloader'

meetup_api = 'https://api.meetup.com'
grp_id = grp_name = grp_url = ''
selected_year = 'Recent'
event_id = event_name = event_time = ''


#-------------------------------------------------------------------------

def last_updated(filename):
    "return number of hours since last file access time"

    if os.path.exists(filename):
        ftime = datetime.datetime.fromtimestamp(os.path.getmtime(filename))
        hours = round((datetime.datetime.now() - ftime).total_seconds() / 3600)
    else:
        hours = -1

    return hours

#-------------------------------------------------------------------------

def need_update(filename, max_hr):
    "determine if UPDATE is needed"

    hours = last_updated(filename)

    if hours < 0:  #file missing
        UPDATE = 1
    elif hours > max_hr:  #>max_hr
        UPDATE = 1
    else:
        UPDATE = 0

    return UPDATE

#-------------------------------------------------------------------------

def retrieve_token():
    "obtain access token from json file"

    access_json = 'access.json'
    UPDATE = need_update(access_json, 999999)

    if UPDATE:
        headers = ''
        
    else:
        data = json.loads((open(access_json).read()))
        access_token = data['token_type'] + ' ' + data['access_token']
        headers = {'Authorization': access_token}

    return headers

#-------------------------------------------------------------------------

def load_json(meetup_url, params, json_file, max_hr, force_update):
    "retrieve data either from meetup or from local file"

    UPDATE = need_update(json_file, max_hr)

    if UPDATE or force_update:
        #print('Refreshed from Meetup')
        r = requests.get(url=meetup_url, headers=headers, params=params)
        data = r.json()

        if r.status_code == 200:
            #save json output to file
            text_file = open(json_file, 'w')
            text_file.write(json.dumps(data, indent=4))
            text_file.close()
        else:
            print('Staus Code: ' + str(r.status_code))
            print('Reason: ' + r.reason)
            #print('Header: ' + str(r.headers))
            #print('Text: ' + r.text)

        #print('Completed')

    else:
        #print('Read from file')     #debug
        data = json.loads((open(json_file).read()))

    return data

#-------------------------------------------------------------------------

def user_profile(force_update):
    "retrieve member's profile"

    meetup_url = meetup_api + '/members/self'
    user_json_file = 'user.json'
    data = load_json(meetup_url, '', user_json_file, 4320, force_update)
    user_json_data = data

    member_name = data['name']

    return member_name

#-------------------------------------------------------------------------

def retrieve_group(force_update):
    "retrieve member's subscribed groups"

    global group_json_data
    global grp_id, grp_name, grp_url

    grp_id = grp_name = grp_url = ''

    meetup_url = meetup_api + '/self/groups'
    group_json_file = 'groups.json'
    data = load_json(meetup_url, '', group_json_file, 72, force_update)
    group_json_data = data

    #delete the group/treeview data
    for x in group_list.get_children():
        group_list.delete(x)

    clear_events_frame()
    clear_photo_frame()

    #display groups
    for x in range(200):  #meetup return 200?
        try:
            #populate the group list / treeview
            g_name = data[x]['name']
            g_country = data[x]['localized_country_name']
            g_members = data[x]['members']
            group_list.insert('', 'end', values=(x, g_name, g_country, g_members))

            #create group directory (gid)
            g_id = data[x]['id']
            g_path = 'gid-' + str(g_id)

            if not (os.path.exists(g_path)):
                os.mkdir(g_path)

                g_readme_file = g_path + '/00-group-name.txt'
                #create a text file with the group name
                text_file = open(g_readme_file, 'w')
                text_file.write(g_name)
                text_file.close()

        except:
            break

    #status message
    y = last_updated(group_json_file)
    msg = str(x) + ' groups | Last updated ' + str(y) + ' hours ago'
    group_status.set(msg)
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
        g_index = selected_data['values'][0]
        selected_group = selected_data['values'][1]

        #only do something if the selected is different from current
        if selected_group != grp_name:

            #set global variable for selected group
            grp_id = group_json_data[g_index]['id']
            grp_name = group_json_data[g_index]['name']
            grp_url = group_json_data[g_index]['urlname']

            #delete the list
            option_year['menu'].delete(0, 'end')

            #re-populate it. first entry: Recent
            option_year['menu'].add_command(label='Recent', command=tk._setit(var_year, 'Recent', year_clicked))

            #populate, from current year till group creation year
            g_created = group_json_data[g_index]['created']
            g_created_year = datetime.datetime.fromtimestamp(g_created / 1000).year
            current_year = datetime.datetime.now().year

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
        r_click_url = group_json_data[g_index]['link']

        #mouse pointer over item
        r_click_popup.tk_popup(event.x_root, event.y_root, 0)

    return

#---------------------------------------------------------------------------

def retrieve_events(year, force_update):
    "retrive events listing"

    global event_json_data

    #multi photo albums should be detected in this json data?
    #how to handle?

    meetup_url = meetup_api + '/' + grp_url + '/events'
    event_path = 'gid-' + str(grp_id) + '/'

    if year == 'Recent':
        events_json_file = event_path + 'events.json'
        params = {
            'status': 'past',
            'page': '15',
            'desc': 'true',
            'fields': 'photo_album'}
        max_hr = 744  #31 days. recent event list
    else:
        events_json_file = event_path + 'events-' + str(year) + '.json'
        params = {
            'status': 'past',
            'no_earlier_than': str(year) + '-01-01T00:00:00.000',
            'no_later_than': str(year) + '-12-31T23:59:00.000',
            'fields': 'photo_album'}
        max_hr = 4320  #6 months. yearly event list

    data = load_json(meetup_url, params, events_json_file, max_hr, force_update)  #744 hrs = 31 days
    event_json_data = data

    clear_photo_frame()
    clear_events_frame()

    chkbox = all_event.get()  #checkbox status

    event_count = 0
    #populate the event listing / treeview
    for x in range(500):  #max 500 per request?
        try:
            e_name = event_json_data[x]['name'].strip()
            e_id = event_json_data[x]['id']

            e_time = event_json_data[x]['time']
            dt_object = datetime.datetime.fromtimestamp(int(e_time) / 1000).strftime('%d-%b-%Y')

            try:
                photo_count = event_json_data[x]['photo_album']['photo_count']
                taggy = 'dummy'
                event_count += 1
            except:
                photo_count = 0
                taggy = 'nophoto'

            if chkbox or photo_count > 0:
                event_list.insert('', 'end', tags=taggy, values=(x, e_id, dt_object, e_name, photo_count))

        except:
            break

    if chkbox == 0:  #if checkbox, then return the count of events with photos
        x = event_count

    events_buttons('normal')

    #status message
    y = last_updated(events_json_file)
    msg = str(x) + ' events | Last updated ' + str(y) + ' hours ago'
    event_status.set(msg)

    return

#---------------------------------------------------------------------------

def clear_events_frame():
    "clear event window"

    global event_id, event_name, event_time

    event_id = event_name = event_time = ''

    #delete the event/treeview data
    for x in event_list.get_children():
        event_list.delete(x)

    events_buttons('disabled')
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
        e_index = selected_data['values'][0]
        e_id = selected_data['values'][1]
        photo_count = selected_data['values'][4]

        #only do something if the selected is different from current
        if e_id != event_id:

            event_id = event_json_data[e_index]['id']
            event_name = event_json_data[e_index]['name'].strip()
            event_time = event_json_data[e_index]['time']

            #if no photos in the event
            if photo_count == 0:
                #delete the treeview data
                for x in photo_list.get_children():
                    photo_list.delete(x)

                album_status.set('No photos')
                album_buttons('disabled')

            else:
                retrieve_album(0)

    except:
        pass

    return

#---------------------------------------------------------------------------

def event_r_clicked(event):
    "right click, open meetup page"

    global r_click_url

    x = event_list.identify_row(event.y)
    if x:
        selected_data = event_list.item(x)
        g_index = selected_data['values'][0]
        r_click_url = event_json_data[g_index]['link']

        #mouse pointer over item
        r_click_popup.tk_popup(event.x_root, event.y_root, 0)

    return

#---------------------------------------------------------------------------

def events_buttons(status):
    "enable/disabled all buttons at event_frame"

    event_refresh_btn['state'] = status
    option_year.configure(state=status)
    event_checkbox.configure(state=status)

    return

#---------------------------------------------------------------------------

def retrieve_album(force_update):
    "retrieve event photo album"

    global album_json_data

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
    album_json_file = 'gid-' + str(grp_id) + '/album-' + str(event_id) + '.json'
    data = load_json(meetup_url, '', album_json_file, max_hr, force_update)
    album_json_data = data

    #delete the treeview data
    for x in photo_list.get_children():
        photo_list.delete(x)

    nodl = 0
    for x in range(500):  #max 500 photos per album
        try:
            photo = album_json_data[x]['id']
            photo_filename = 'highres_' + str(photo) + '.jpeg'

            member = album_json_data[x]['member']['name']

            upload_time = album_json_data[x]['updated']
            ftime = datetime.datetime.fromtimestamp(upload_time / 1000)
            p_date = ftime.strftime('%d-%b-%Y')
            p_time = ftime.strftime('%I:%M %p').replace('PM', 'pm', 1).replace('AM', 'am', 1)

            #highlight photos found in folder
            p_path = str(event_id) + '/' + photo_filename
            if os.path.exists(p_path):
                taggy = 'nodl'
                nodl += 1
            else:
                taggy = 'dummy'

            photo_list.insert('', 'end', tags=taggy, values=(x + 1, photo_filename, p_date, p_time, member))

        except:
            break

    #disabled the buttons
    album_buttons('disabled')

    #enable the refresh button
    album_refresh_btn["state"] = 'normal'

    #enable some buttons, if not all files are downloaded
    if x != nodl:
        album_btn3['state'] = 'normal'
        album_btn2['state'] = 'normal'

    #enable "folder button", if folder exist
    if os.path.exists(str(event_id)):
        album_btn4['state'] = 'normal'

    #status message
    y = last_updated(album_json_file)
    msg = str(x) + ' photos | Last updated ' + str(y) + ' hours ago'
    album_status.set(msg)

    return

#---------------------------------------------------------------------------

def clear_photo_frame():
    "clear the photo list"

    global event_id, event_name, event_time

    event_id = event_name = event_time = ''

    #delete the treeview data
    for x in photo_list.get_children():
        photo_list.delete(x)

    album_buttons('disabled')
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

        #pop up menu, only if the file is tag with 'nodl' (ie. file exist in folder)
        if tag == 'nodl':
            req_file_to_delete = selected_data['values'][1]
            r_click_popup2.tk_popup(event.x_root, event.y_root, 0)
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
        album_btn1['state'] = 'normal'
    else:
        album_btn1['state'] = 'disabled'

    #report number of photos downloaded

    return

#---------------------------------------------------------------------------

def album_buttons(status):
    "enable/disabled all buttons at photo_frame"

    album_btn4['state'] = status
    album_btn3['state'] = status
    album_btn2['state'] = status
    album_btn1['state'] = status
    album_refresh_btn["state"] = status

    return

#---------------------------------------------------------------------------

def album_select_all():
    "select all in the photo album"

    for x in photo_list.get_children():
        photo_list.selection_add(x)
        #https://youtu.be/zoLOXN_9EH0

    album_btn1['state'] = 'normal'  #enable download button

    return

#---------------------------------------------------------------------------

def album_select_none():
    "unselect all in the photo album"

    for x in photo_list.get_children():
        photo_list.selection_remove(x)
        #https://youtu.be/zoLOXN_9EH0

    album_btn1['state'] = 'disabled'  #disable download button, since nothing was selected

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
    msg_box.tag_config('err', background='red', foreground='white')
    msg_box.tag_config('ok', foreground='green')
    msg_box.tag_config("sum", foreground="blue")

    progress_bar = ttk.Progressbar(download_win, orient='horizontal', mode='determinate', value=0)
    progress_bar.grid(row=1, column=0, sticky='nsew', padx=20)

    ok_btn = ttk.Button(download_win, text='OK', command=download_win.destroy)
    ok_btn.grid(row=2, column=0, sticky='nsew', padx=10, pady=10)
    ok_btn['state'] = 'disabled'

    position_window(download_win)

    #create download folder if needed
    dl_folder = str(event_id) + '/'
    if not (os.path.exists(dl_folder)):
        os.mkdir(dl_folder)

    photo_count = album_json_data[0]['photo_album']['photo_count']
    total = len(dl_list)
    count = 0
    dl_count = 0

    for x in dl_list:  #max 500 photos per album

        photo = album_json_data[x]['id']
        photo_filename = 'highres_' + str(photo) + '.jpeg'

        msg_box.insert('end', '[{:3d}] '.format(x + 1) + photo_filename + ' - ')

        local_file = dl_folder + photo_filename
        if not (os.path.exists(local_file)):

            #download the photo
            hires_link = album_json_data[x]['highres_link']
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
                #unable to find a way to modify the file create date/time
                photo_date = album_json_data[x]['created']
                photo_date = int(photo_date / 1000)
                os.utime(local_file, (photo_date, photo_date))

                dl_count += 1

            else:
                msg_text = 'ERROR\n' + \
                           'Staus Code: ' + str(r.status_code) + '\n' \
                                                                 'Reason: ' + r.reason + '\n'
                msg_box.insert('end', msg_text, 'err')

        else:
            pass
            msg_box.insert('end', 'skipped\n')

        count += 1

        msg_box.see('end')  #auto scroll text up

        #update progress bar
        progress_bar['value'] = int(count / total * 100)
        window.update()  #force update?

    msg_box.insert('end', 'Download completed\n', 'ok')

    #display summary
    msg_text = '---Summary---\n' + \
               'Download folder: ' + dl_folder + '\n' + \
               str(photo_count) + ' photos in event album\n' + \
               str(total) + ' photos was selected\n' + \
               str(dl_count) + ' photos downloaded'
    msg_box.insert('end', msg_text, 'sum')
    msg_box.see('end')  #auto scroll text up
    msg_box.config(state='disabled')

    #---

    ok_btn['state'] = 'normal'

    download_win.wait_window()  #wait for 'close' of window
    window.attributes('-disabled', 0)  #enable the main window

    retrieve_album(0)

    return

#---------------------------------------------------------------------------

def about_window():
    about_win = tk.Toplevel()
    about_win.title('About')
    about_win.resizable(False, False)

    #---

    frame0 = ttk.Frame(about_win)
    frame0.grid(row=0, column=0, padx=10, pady=5)

    logo_b64 = "\
iVBORw0KGgoAAAANSUhEUgAAANoAAADACAIAAADtMupxAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMA\
AA7DAcdvqGQAAC21SURBVHhe7Z0JfBvlnfc1mtF9W5Z833Z8xya2EyfOHUgIR7i3UCiUcvTtFtru9n23+7IttOxLd9u9uiVttxQo\
bYGFlFASYCGEMwECOZzLseP7vmTrvo+Zef+jmSg+ZFuyJWvkzPejj/LMMzOyIv30P54T+fGPf8zj4GAHfOZfDg4WwMmRg0VwcuRg\
EZwcOVgEJ0cOFsHJkYNFcHLkYBGcHDlYBCdHDhbByZGDRXBy5GARnBw5WAQnRw4WwcmRg0VwcuRgEZwcOVgEJ0cOFsHJkYNFcHLk\
YBGcHDlYBCdHDhbByZGDRXBy5GARnBw5WAQnRw4WwcmRg0VwcuRgEZwcwyAQCMQSCYIgzDGbePzxxzdv3swcrDg4OV5GKBQVFRdv\
3b7jlttuv/mWW7ft2CESiZhziaOysnLVqlXMAY83OjoqFouZgxXHFS1HPooKhUKlSrW6pubmW2978Jvf3H39DVXV1fq0tFSdrqKy\
Cg4TbiO3bNmSlZXFHARhw48kTqBbt25lilcGIC+ZXK7X6XPzcisqK+sa1q5rXF9QWAiinK08qBzo73c4HMxxLNiwYQOfz9doNHV1\
dVqt1mQyBQKB/Pz8qqqqgYEB5iIer6mpCepramqKiorgN0NjsVjgLr/fD4X6+vr09HQwliRJMvfweBUVFatXr6bla7Va6cqNGzca\
DIaCgoKGhgb4uyMjI3Q9C7lS5AhS02hSiktKamqvqq6pKauogHJ6eoZMJgNx0Ne4vP6z/aYegz1FLhJiKF3psDuGh4fockzYvXt3\
Tk4OfOx9fX3V1dXr1q07f/48SOorX/nK4OCg2WyGa8A733jjjYcPHwbx6XQ6FEUhnHW73SA+qFGpVFdddRWoEy4DvZ48eRJukUql\
999/f2ZmJihVr9fv3LkT5Dg2Ngan7r77bhAoOH2j0bh9+3YQ8YULF6i3wj5WshxBguCO4esECW7Zuq1h3TqwgqmpqXK5HL5LOAtm\
BSdIu8f/Qcvw3kOtT+4//cbJgf85M7TvWE9dYWqaispmQCgd7e1TLdASAT3Bq+3du7enp+fs2bOgD9BNd3c3WK+UlJS2tja4BuwZ\
SKelpQUO169f39zc/NZbb4EW6dtxHP/DH/5w/PhxUBvY2o6ODrDf4NPhf/rMM8/09va2trbC/xHMLa3UTZs2wav9/ve/h78CV8It\
n3/+OUEQ1LthGSstdgRDolKrs3NyVtfUXrPr2nvuvfeOO+9aU1+v1mhoX0wQpMnhvTBoPnx++JfvXnjwmaM7n3rnH145daRtLEAw\
mnN4A0+/22q0e6EM5hNekK6PFSALcMRQgGdwnRkZGVAG8YGAgud5tbW1tC4BcM0AXaYB/dntdij09/fDM9hFeAaLC0KkTgfp7OwE\
GxmKMsEA0wUwwPBM38JCVogcQYWZWVl1DQ07r7121+7r4LFpy5ZVpaVKJRMRghUcMjrePj3ws4Nnf/Dy8R+8fOKHr5564ZPOM30m\
byCMneifcPROUF+5RCoFL09Xxgr6LdGAC6YzZdqBgi0sKyvzer1g4YLnKcnShRAhUw0WDsr0qykUCp/PR9cDdFkikdCHoVvAssLz\
1DfAKpJbjhD2FRYV7dq9+4GHvwmpceP6DYVFxWAV4GugP3H4GnoN9mc/vPjVpz+65d8++NGrp1491nuie3LI5PSFU2GISbtnYNIB\
t4OBAR8av+8PXhyiPSiALkGCjY2NV199dUiLwDxypKHfGwSdkKbQNQDElyBW+pWTiCSTo1AoAluVk5tb37B2z823PPS/vnXdDTeW\
rCqFWBCkCV8MONwxi7tl0PR288A/7j99878evu3f3997qK19xOrHwZgwr7MgcOG5ARO8GrymTq/HBALmRCyAeB1SECjQmUrIk4K/\
ViqVkG5PlaPL5aIzZbB/dE1YwLhCWk23UIJ9hbz7008/pU8lEcmRysjk8uzsnNKysqrqqqrq6qrVq/Py8yGkAx9NXwBSuzhs+ejC\
6OvH+14/0bfvi963Tg+2DlusLn/ECpyJL4Df0pAvQPkYhnVcbJsRwC0akCCkIEVFRddeey08v/32211dXfSpyclJSLTBU0MlXQPA\
X29qaoKvCeohWITb4bJQkxDUg5pNJhMkOvCD3LVrF+RGoEuILyExp6/ZsWMHiBXugjJEjWvXrv3yyy89Hg99llWweiMPMBWQCxcU\
FoHBAPsE4gNbBTCnwZHhxMmeSciLj7aN2T0B8L+gS+bckoG/s/9vdhSmKcE5vvH6/uGh2DT3PPzww+3t7Z988gkkv7NbNL/zne/A\
2UOHDjHHQSC4hPCDbgNakLAvmyywyDqCzuBTVyiU6RnpldXVTZs2r21szC+gGqgFQS3CNW4fPhGM6j5uHX32o/an/nLmLyf6W4cs\
kAsHffGiTWF4UhXiusJUeGNej2dggEpjlw6YN4PBAOZtauZBU1BQALHjO++8QyfOISB8jNyYzX7ZJCLxcoQvG4xfbl7eqrJy8MU1\
tVeBFjMzs8Ct0A3UYJxMTu+5ftOHLaMHTvbvO9bzp6NdH14Y7ZtwxNAWhsXm8t2+roD6nYjF586eZWqXxvXXX9/b2zu1AyYE3RNz\
9OhR5vjKI5HOOiMzs6CgMCcvVyKRQi4CJnCqIwYVGmzuYx2GoxfH20csdo/f5cXjrb8Z8BHem3+3MytFBm/mv1/8E4RozAmO+JAA\
OYLbLa+oWNe4XjK9MRZ8rcsXcHj8kBp/0WX4tG384qglgMfY/0bLj2+/6uaGfCh8dvTI6eZmupIjTiTAWecXFGzasjWkRQj4Bo3O\
5t7JD1tGIBD8w5HOF492He+eNNg8kbfLhKUgVVqok4GFgyyHqYoeqRDbVplJm+2O9na6kiNOJECOFZVVOTk59BdstHt+fvDc8x93\
HDoz9FnHeNe43eLyLVGFgE4hfHhLwdc35m0v120p1YGJbR9fZLKJ8pGtlZkyEQZBbm9Pt9dL9RxyxIkENIOTlzrvfQH8dx+2Hzw1\
MDDptLr9S1chIBGgW0tTn7679pa6rEy1RCsX5Wql395RtDpbxVwRJSaHty/YWygSibSpOrqSI04kQI4TEwa65xTcccugOVaNMxIB\
v6lY+/ie8iduqgAhXs6JeDyxgH9rXaZCjDHH0WB2+noNdkhlINlKTU1lajniQwLkaLNanXQ7LTmz+3XR5KdK/2536Q+uW7WhOAXc\
K9RYvMiAA/VQsqfakhoKNDU5izGQkMt3jFq9AQJeRJuqFQpjPBK7sbHxhz/8IXMwhdDoniuKBMjRbrfbbDYoqGTCzBQZXblo5CLs\
/o15L3yjbkeFXi0VgvYcfmRfr/x7J9L+vln/2Cldp5XqblaIBXeug4CVvik62oYtbm8A5Jii1YrFS5VjZWVlRUUFcxDE6XQypUus\
WrXqtttuy8vLY47nACSbkhLj0UaJJQFydLvdZpMJ7CIoqThNQRuzRZAiE+ys1P/bV6rv25DH5/PBzpq8/CPjkp+e074xqPAR8F9D\
xjyC/+pQm73Uf7M6Swkum743KrrH7UYH1SmiUqoUCiVduWhUKtU111zDHASBMIApXaKjo+N3v/sdPZxxHq6//vri4mLmYEWQmF4Z\
kVhUUFgIGnJ58SNto/OP9ZoNKHhDkfahLQW31WWlQ5iIIODyT06K9/Up3h+Rm3wQI16WuCOA2gNIndbLR5DKTOWX3SazK7rBEAGC\
LExTVOWkwBsGw76UuQp33nlneno6KDIQCGRlZQ0PD2dnZ5eUlBw5cgTOFhYWguEcHByEC6AwPj4Ol1199dVr1qyhB08UFRX5/X5w\
LwKBYMOGDfT4HYlEArE43U9dUFCwevVqMKvwmYRGl23cuHFgYACiAviuz507R1eykwRYR2BsdJQeHF+RrZYIo8swVBLsRzeW/b9b\
K9YWaEQCqiN70sP/2fmUX7RpWiwiPxnG1n45ITlvpiwQuOy71uVg0dvjj1upSSdAbv4CDnR+IBlSKBSgFbBqOTk5dCXdHZ+ZmXnX\
XXfR/aJKpXLbtm30iDLQHwj3u9/9blpaGmj3oYce0uv1YFDhEM5qtVoQsTo4Xh2M7r333gsKhle+7777ysrKoFImk+3YseOee+4B\
KcOV8KehkrUkRo4QO1qC41O0ctGqjEgzjAyV+M612S880LC9XI9SXxsy7kYPDsgeP516ziwiKYsY/rP2Ecj7IzK7nzq7Jk8ND7o+\
ck73Ttpc1NAEnU4/ozMpKvbu3dva2gqKeemll/bv38/UBlUFOjt58mTYDmtQG1x84MABuAtMY3l5OYSb9O2ff/75K6+8cvHixfz8\
fLCXTz/9NNTAZX19fevXr6dvByBAgsonn3wyVrljnEiMHIGurk54hh/r1op0umYe5CL0ljWZP9pT9tDmAq2csnOgrUMj0r0XNfv6\
lRb/NO8cDqTVKjpvprIQuP3GmgwhFt1/HDLr490TUABLll9QQFcumtlDJx955JHm5uYZ48pCjI6Otl/qEDIYDKGZLiBruskM0Ol0\
4HDAIjYFAdmBEaVPAZ999hlTYjeJk2NHB13YWkFNXJqH0nT5z+6oemR7UVWWShCUUbcN+5cW7Us9qm67kAjnnWfjxpE3B+VgGuAH\
sHFV6tqCqA3kpxfH6UJR0ZKyB9DibDl6PB6IIGlPPZupJg0kGHK4UKYLADhleM7NzQXPDn4cAkfQN30KYLlRDJEwOVqtVrOZGiCj\
U0rKs8KIAyK8PK300R1Fe++urc5WgxAh4el3YM93Kp84o+uyC/HIhHgJpN8pPDgoJ0gqE/ruNSVqaXTzDc4NmBxuSkY6vV58aUrU\
IgANzZ5U+utf/xoixT179jDH05khprBypAfnguPet2/f66+/fvDgwdBo8CQiYXIEhgaoSZbApjIqKp+KVia8e33OU7dW3l6fRecr\
Ex7+Xwbk/9mm+WBURoRxzRH9+g8MynvtlArTlOK7G3OiamOyunydY9S6DgIM0+tnvuHIcblcYL0gWKTzDwCSYogIQUM1NTWQPtOV\
U5lLjvBSkABBgZo+0dEBKgc3TZ/SaDSQYtPlJCKhchwapD/o9SX6kDDAKF5bpf/VPbX3rs/L1Urho/fhvI9GJU+dSz04qBhzC4Ip\
y2X0EuKRGt8zO7z/1OT9ZpV/Z16gQhPIk7lkaJjWHA/Of3tI5g2GW1tLdZWZ802GmoHD4+8Yo1rvMYGAzmoXB0SBRqMRgsWvfe1r\
dI1cLofn8+fPQ+x4ww03hDLuBYFbGhoannjiidraWkhWwC6CoOHw+9//PiRGa9euZa5LHhI5/DY1VXf9nj3gpIZNzm8/9/moxZWb\
Ir1/U15jYQqGUs3aPoI36sb+3Ks4YxbPUCGNCCUfa/DXpc1qtiQJHuHptqInJyQ9Vv6QA/HgIGsEhChGiW8UW65K8cJFb54dffr9\
7rDzrMNye2PB/7mhGqx1V2fHB4cPzw4BIwes1/xzX4RCYSTTDCQSiUgkmjqBFSylWCxO0ukyiZQjZIhX79yVm5dnd/tePNIhRIhr\
KumOPnBPvB4HdnRMetQgdeNzmvByDf6zTf4FXS5O8Ewe3qQbMXoQeE4X+6rVbpCs1el74o2WE70RTYkCrsrX/uyrDXqVZMwy9Prx\
500OKtdeOvDbwXwikUMtdFNm8komkXNlIBLXA2lpZMBXqBVVZSmlwSZxhx95fUDx5z5lK9WsPV84sSUbX6O/FFfhbtTTifpGeKSf\
RAQ8hBqhSJ8BvcoEPJ2Ul6skSzVklhIRCgSYUCiTiteWpDWW6EszVZBRYSjiCk4Bo++aDZzdWZOtVYiFmKhztMXqis1cBXibJIb7\
pU6Chwu8S+3ET2oSaR1RFF1dU1NZUUE3cIBF9OJIi0X4co9yzBNR2vuDeu+mrKAcA3ap6RUUZ/QBVSRfTmD6gEBPCNIITMfji0kE\
UiI+j3kOb1EDOAGRQ/uorX3E0j5i7R63efzUBJ0ATsIzTpBP3rFmTz3VMfPWqZc/br08G3qJoHxMJACVCyUTepEnioh2hZEYOYL+\
IBsoKiqCsF0QXOABhHjRKvhkTNpsEgdHP0QC+ezV3nSwJiQpNr0q8M054CCoThmBKklURT3zoSAj+FKohAIPEc2jToPNM2p2UQ+L\
a9zqrshW37qWagZvGz7z3If/Ql8WK0SYWE6oFZORpjIrjwTIEXKXqqqqrKys0Eo6Y270jQH5WZPY6qfadCJEhpEvX+dF4QVwl9zw\
K4QXaUZCZUWIgEREJCIk+SKSLyEwLYGmEALqmceXhFUnSZJgHcFG0p3sXr/n4shZg3WEethGJu3jXr+bvnIpSIUK/RjV13xlsqxy\
BKMIFnHNmjX0Qm+UdyZ4H43KXu2jx4NFxyo1/u9bqNyW7xuWGl+CAIyuXwq0l8cFabggnRCk41gaDxXDp3T5MYcdBU8Omc2QsXfY\
1Dto7B21DPgCXlAwSVKLjJERvzfw2jmTVzEHVx7LJEcMw8AclpaWpqczPdTOAHLWJDo8IuuwCcM24izI9uzA39ZR3RKYq0VsfXsx\
L7EQl7y8msTU8EygKpJy8RL6mYcI51ZnwOI0mRwGo91gdBjMzkmbyzxk6gWNMlfMTb6pgSldeSyHHEGC5eXlOp0OjCJ4Z8hcL1iE\
7w6DEEWuuRtxFuS+cv8dq6gWbaH9qNDxeTzkOAP42YB/p7IiUCRCPRNYCiVTTEOCZPnSubw8QeIOj61nvH3/l897/C7mxBxcyXKM\
b0MPGMX6+vq6ujq1Wk0vMuHHeS90q/67VzXixuZvxFmQGwrwHAU13UbgOscPTCyDHOFPIDwcIb18wsHHLfzAJOobxLydAvc5ofME\
5joLh0jAAikQyRdDeMrchSB8hC8WSNLV2d6Au9ewwGRttXvaPglXFPGSo1QqzcvLa2pqys7ODrbjIEYv/9NxyX+2adqs4mCn85L0\
I8XI6wrwVAkYH6/A3YLiCVhXk/4/hB580ofiJsw3IHRfEDq/FLjOYt5uBHeAo+fxqVgZdAkJ0Jn+L+jb5+JKlmNcnHVBQUFxMbUK\
LT3O2Ufwjhkkn4xLu23CsKO1F0GWjPiHtf5cJYkEzBLzATTAjP5iGxB9BoSFHs1NPD7V23Si+8irn/+WPjUXahlLZ2MtQ+/Rktzl\
bMAp79q1a8OGDRAvghYhpex3YP90PuW5TvVFa8y0CKhFpASj0lWEcCMkG1fOpIH/MObrR/3MVi4TNmr3gyQF4fNwsdeVOu5SxqZ3\
dDaxtI45OTnr1q2jxyoTJM/gQcE7HxqROwMxFj2wMRN/tNYvE/BQT7fE8ibEc8wJ9kHy+G7Nzbi4BMp/+OQX5wdO0PXJSLx7j2Ip\
lOrqalqLYBTPm4S/bNW8PqCMhxbhL2hEpBgCAZJECCePZPkCmwjBZ6bDJrV1BHAi4PI63F6nTxGXYD2WWgmt3G/38w+Pyvqc0Q23\
jhwM4aVKyOBAHpIfsMakATxacLfbMzbqMYzjPqq5m6kNB9U8BNlMsKl8wsbMSExqvAGvG525VEFMiKUcQ6PunAHE4FlwOtXiEfB5\
eikZbOMj+Xikw8NiAuH3OQf6h15/tee3Tw+89MLAn57v+c0vRw6+7hoeJPz+sLokUSazNliHwbrQlcmONxCDHtHZxDJ2LCkpqa+v\
FwgEZi//1+3qC5Z47XOrEJJPrPOVpZA8MiAxvoz5l8kDBpwO08kvrWeayVl7vaASiXpNg6ZuLX/Wlh8+cZVXcz0UAn5/wJc06/H5\
cd+wuf/zrvdbR84wVdOJR3N9LNsd3W43veOfCOW5cKTNGuk0v/khCSLgtnnMY27joGui32noxZwjX63XSoUoyFFk/xThLYfJIQIB\
86nj5lMneJfmkk4FBOoZG0GlUkn6zHVX/JLVhJCqxAP+0GKC7Aflo2qptjq7QYiJugzMjnRTiUf7aCydNcixs7MTx3GI6jbp3RmS\
xauE6ljDAz6n2dJ/Zuz0m+Nn/sfcdcw+1OIydHtMg0KPMUUaXLuCcPHJ+bxGsIOODBCkn3oQ8Bwc0bCYWNNnNlnPng6rRRrS75/4\
+AP/pW17Q+BCqpueeifJo8WpbCzZWZFZyxzEmRj3ythsNq1Wq1KpwHLpxIHjk+JFGEhQosc6bh+6YBs457OOk/jMKSlri3Q7V2dD\
AfX2CTxh+txAf0ZfYNDt63Z42uzu8zZ3i83davd0ONwDbt+EN+DCCQxBRNQ+XZG+Pcvpk66+HuZgLiDTxzBZHrWWOA3J43uV24Nj\
fnmBpN1iQyFWN/d/zhxcIh7WMcZyBBswMTFRWFiIYZhejEMQ2euYuTzX/OA+j3XwPGjR7zBS/QDhuK42Z00BtfKnwN2C+YfpSppJ\
r/8Lk+OQwXrUaD9hdp62ukCFPS5vv9sHQuxz+TqCAr1g84BADd6AToTJLm1dPT+TRz8ORDIfiiCUlatDKidQtV9OzeiDTwacNV2Z\
dMiEik/a32EOLsF2Z03jdDpbWlrg0weXfWOOM1UELjsi50h9YT63uetL52gH4Z+vo6U0k1nWB/VTfYPgf30E0eXw/KZn/Mdtw6+N\
mEFqox6/LYBDrktfOZUAyYNToM4PJmw/aRs+MGJyBHD468zpOfBP33poLgifj5wiOwJjevySKGqcjQCLzqYsmni0UVP7LE9OTsIX\
nCLCt6U7sQj8IVzsd1qM7Z95LEx/2jyUZARblUkC8Y8bvP5Pjfa93eP/0TUGTjna7xyuf89g+1X3eLPFCcElUxsOyJ2Z0ryAs0bQ\
YFwbhMC0dAFCR7rAMQ9xkaPL5aJ3EMf4vCa9J0OysJPyuyyWnhM++8KdoRqZUKeglOEL2A+Njj7bN/HasKnL6V1MehIEbgRX/sqQ\
CV7H5p8zUxFnRuSbRPo0ZMpSO5flmMzWcdmIixzB1IEc6RWX9RL8uuwFWvBxv5fKWiBYjICiNAU/2CEzYBl4a8wy5PaB8106Tpw4\
anQ8328w+8I3CKgqqnlzLOk0FVV1bWgQLuQxJErFFfCBAHRlkmIctBqHrNZxhzfKxVqjIi5yBHAcP3nyJL1OQ5PeXaWeMxYEs2Ef\
afOYF/bRNMXpTOBocBroQgzpcHh/12fodXogHmWqLiFM1SkrquZTJJ+vqq2TZFxudwzOYQiuJZ78cqQgeQEf7jC6nJa4dMkA8Z2c\
UFdXV1FRAWlmrx37eYs27ERBx3iPpfckj5jTS87gh7fW3r6Omlr6RsuLxwbjsmxhigDdk6Gp08jQKc1AoCe/xWz4+H1XTzdTNRU+\
qiiv0G3ejk1ZjBTH0tyam0hMY3QMfdj2rMWd3B3WOE44Hf6REbvJ6JFrpaWeDcyJ2BEv60hz8eJFa7BZOEcW2JLuon5f0/G7rLbB\
c5FrEShOo/IYgsQnXPEadWfy438eNp0wO6faSPhRCdSajBtuSWnaxJ+xuDyGpW7elrZj54x0h5nEzeN5/A5vIC5jDpYTFOUrVaKy\
8tS8fJXHEZfezvjOlaGyGQxLS0vDUL5CQFy0iuxTDCSBB+xDF3y2KHyuWiq8s6lQLRM5fbYTQ8fsXio8jQd+krxoc8swvl4kEARD\
VQAUyUdRSVaOqrJalJYu0umleQXqmjVpV18ry8lFgru/01cCIGRcmB2QrCJ5yISjv9twIvLprSxHqRQ57D51IJc5jh3xtY7g4Pr6\
+uilurJlgY36aTEH5C5uU3S7EOhVYnFwuUe71+4NxHcQuJck9w2Z3hw1Q3IzVUegOUyuUJZXatdv1K7boFhVhganjc8CIfly+MHD\
x+D0msGcM9UrgoyMuMxPiK8cAafTeeHCBSigCG9nliNNfDkvc451zt/cPZs0lYSWo8NrjdMYp6kQPN6RSfuLg5OWOdLteUEJTAni\
BaNoc8crrkgUsuAK7TEn7nIE+vv7BweplUUlKO+bpVYhn2qB89om3UZm9dvI0QflCC8FbtobwRT6pQPvtc3u+deO0fNWpxunBmAw\
J+YAztO9RD6ST/DpVh7C7pmkz64YIDBhSjFlOeQINDc301udrVL6mvRukghY+8OPopsHCMzAOgpBjmBvvFYfEccGsBmYA/hzfZOv\
Dhkv2Ny+OVbc8xPkiNt30uJ4e8xCefkxm4tHrY4HCl551jFOxDeVCeHz+QQCgV6vh8BLKSSa+y1jAx3wTTGnIwPs4q6arPIsTYAI\
tIydHrQusEdabIHQb8Tjb7W7z1icRl/AixMBknThxKQ30O30fGFyvDtuPWK0n7a42h2eQbfPjGMbC3ehfMyPe070H4j2P8t+8LHY\
71+7TNYRLAS4bIvFAhauUO6vFIwg0ffhSoSoTkmNMAc/gfHDNGHGGxCUEycGPf73DLbf9k38tH30yYsjP+8cfa5/8v0JW4/Lawbp\
XWocSpWkCKjlpngm5wjXYR0hyyRHwGq1dndTDcgon7dndWqqIuqpCxIhplNSDXtgckpSy5Sipe5WGVcylMwyjZOOZbXiSc3yyRHo\
7OycnKSC+twU8QObC+nKyAHrqKetI4IUppTdUXV3ha5CJVLGJaheMplKZsjFpGOALnAsyDLFjjQEQRgMBnp7qZI02bkhx2g0vZ9F\
aYo7GplNHvl8VCtLq81ctzH/6qbcTaWp5enydJlAihM+nBpqyecHL0tgy/M1xdcpxGqIUk70HVgBXTKziUfsuBwL6s2goaGhtLQU\
FHmyz/LkwTZLcOvJBVGIBfdvLfnGtlLmeG5cPpvZNWlyG02uSbPbaPPaXT670+90+hwuv2t55Ikh6E+u+VcMFfsCnj9+/jeL+FW8\
8m/HmNJ07vz+5Y0vE4v3dOxX6V1W60jj8XjS09PFYrFaKhi1ersMC4yyRvlIfYH2r7cV7qjKlIgWbn0VoCKlWJOmyMpPKSnVVZXr\
q4OP1RVpNRX61Tmq7BSJVoQJCAL34fFqudTL9U35V0PB7BxpGztKV0ZFy7Hw/VVVG9iycng8rGMC5Oh2u6VSqU6nE2IoJDRH2ifm\
2WgIQ9G/2bXqW1sLcrUSuUzKDy6JFjlUhx5fIBZI5SKlRqLVyzPyNMXlaTV12U2Ul8/bVKot08t0Ekzk87s8eMymVhWnlFRn1ENh\
xNreN3marowKTo7Lh81my8nJEYlEWpnA4SPPDYZZ8AWylmur05+8pWJNrorePFAkofaEo88uHXgpASpOkenzU1atzly7qXDnxrzN\
VWm1hSnFGYpMtUgtFymkAgmoGULQaFePqM1YU5BCxRU9E6fGrNRWydHCyXH58PshlHPm5eUFcxr5yT6rccqAJbCaO6syHtyUf211\
mlLMzDsB9YjEzE4LcQK8vEqSkqHMKdSWVqbVVqbVlOuqyvTVZbqKktTyLGWWWqwRoyJqhtm8dlTAx7YW7UqR6iCPaRs9YnEtZpEM\
To7LChhIlUql0WhEGH9VhuJEn8XhoSxQkV7xxE3lN9WmZ6hEGHq5HQrFBMLwA2fiAuXlUYFEKFeJNamytAxFNhhRCECvylq3IW9b\
Y25TiXaVXqaXYEJIVqZ6eYSH1Getq89uArPqx70gR6d3MasIXZlyTEBmHSI1NRV+DBBHkiTP6PS3jNgEKL82WykThQkQhSKxeMpA\
a1bh9lknnAaDY8zutehlGSX6KmGwP8bmnnjvwm/MrkjnXUzlysysl7UZfAZms7mvr48gCPDAqXLB1lXapiJNWC0CaGST8xOCRKjK\
1ZTU52zaVnxjZUY9rUXA5bP6cfauzMtCEilHHMc7Ojo8noi+sPA59egE78e/Ysrsw+23++I/KHMlkUg5AhBBtra2LriWEkRyCBLm\
rSI7H0L2H0aqb2aO2QTkMeDEOesYFQmWI9De3m4wLDBdhurzY4ox4uZHQcSkIaKZ3YuD2trIa1kx82OWh8TLEVz2mTNn5t/Zns9H\
wUIyB1Mg9/4DWVtGnn+DOY4MECLSTQ1E5+94gPeTX9OVMYcgAw5PHOW+Ikm8HAGTydTf3w/ejTmeRXCjpHBsaeD96Z+ZcoQ0fpUp\
BEFee48pxRqcAOsYm/3XrxxYIcdAINDV1eVyzblZ35xyjB7EucCWgLGCIDjrGDWskCMwOTnZ19fHHMwE0hhqYVDmaGmQD93OlOKM\
D3e7fDNXwuWYH7bIETz12bNnwxpI0GGstEjxnXvIKbY22rgzcsyuUS6PiZZE9srMJjc3t6mpSTB98wHQokQmx2btSMByTva9eXrg\
beZgbr54t6vvwlLnGeZX6hqvLWYOlouV1iszm5GRkeHh4Rk5DRwGAuG3bJkNtYxi41ep3HnWg/eT3zAXLQtGR0SzyOt3FCi1ES1k\
OhdwO7wIc5DksEuOdE4zu5/G5/H43G5Q5AyY00HIzn7QHL/m1rmSFeS1Q7QuSQ8zeojEcV5LF++fn+Xte5fXGcsJVvDeTM7wYyBm\
gAnQphtWodgivwi4EW6HF2GOkxx2OWsARdF169YVF89yPYGAavvDpFzqPPxbaioMikK6DX4c4rNAAJeuvYu5LBYQZ/YjUY7znYHX\
7/zjse8zBxHQ02I4fijcOn0LsXZXUWGVnjlYXla+swZwHG9pafF6Z04bAC3CM+Jwydd/ze/zet0ut9Nht1rOfXYstloE+LW3Uc59\
CUAew5QiAyQF8R9zEDFwS6K0GCdYJ0fAZrM1NzczB0GQyZlDBsEbjo+Pv/2XN+of/Q+mKtZQbt20yJYakzPqQWXRBpErKWQMwUY5\
At3d3WNjY6HokExl9oKlMRqNX3755QcffPC1Xy6cui4F/pb7eB1ztYbOh9k1bbebSIgqiFxhIWMIlsqRIIiLFy9Oddm2A7+gCx/+\
x7ePHDnS0dHxrf96n66JK8ht32NKEUOShNm5mAkJqlRpXWQGDy6Di5mDFQRL5QiMBAkZSEKtOPX8Y7//3g2tra12u333e+fp+mUg\
2jjSG3C7fYtcljeSIHLlhYwhEjZXZkHAQI6OUjYG0mfwzsePH29rawsN/Nn9UZg9ROPHZOepsTptgPD5cU+A8IP9C3Zchvkxw+/H\
6BjoNHwRWOwk7vQ81VCXyesOP3cRQsZNN5Xyp8wiShQrba7Morn3lWOq+CyVPg/P/CodRTCJUCkVqqQi9TV/9Q4PITvff0wmUstE\
GqjE+EL45djckyf6/tI7cZqkVipdJNZJ13svncdnTT+HkHHn3dUscdPxaOhJJjk++uzHTCkRvPiUzqWmUgcEJx/6DrUXIs0fnylG\
+QIBKpaLNKBIo3PQ4TUvfQW9sC2RCWxlnM0V0e4YFqnLm1gtAnc9zvQs3/d308aue/wOp9dscY0OmVv7jGfsHmNMVnOcHUSu4JAx\
RBLIUW1xPfBy+Fme0SJ54q9TBj+CB08c9Urr6KWdDyz6ZWpemdoSuSJbGWeTBHL82mvHmdJCyJ/5Ca02eAhvvYapvQRUSh68gyl3\
HhLecS1dRvQpkr9/CB6Cbevomvl54weXQ3hrahw/wFBL5EptZZwN22PHCH00olZozh9kDqbg+dMB12O/4MkkKRf/h6maAmTBs0dS\
eg9+6Pz2PzIH04FshiktIxBEwjML3fSVmMpEJEc+P6X/A6YcC8zVN5GWMA2HsZLjXCtMxIrlWaniiktlHnrhCFOal9hqEdCcP8CU\
pvPwt8fgwRxwxAFWy1E897qPCYRTZPxIglRmfjSxNo2RMI8i7/vfY02vcDO2FknSyxGJ3ZzXqNj8YpglUnc/bRS5eZVHuXV5FgmL\
5IgQEc2GiS2mnG3wYA4uYV59E1Oam7JjYRbfeedRLVPiWBSskKPM4YEM+pHnP4Hnbz1/OX1ZUJ6agQ+Z0hzQapstOBpzXfg516R5\
8dtkQ/adkPaglQEr5PiNV75gSjweRhD6CUYN+/asoQtzMbvVMCrCLhmFd3GbZCUMVrQ7zmhcxBHk1w9socvztTtiaErvfCNwzVV7\
SCuzSwjVMTgdc+0tpJGK/2acmsuUzuYKt4JXSrvjyZpcpsTjjeipLaHDoml/hynNQUiLqs9epgtTobXIwSpYIUeXeNoKE8frmbEC\
q1sGMw1zNpogwvnWpSBtDqbE46G5GUzpEuY1t9EFTfe0FcxMeTuY0kK0rY96i0+OBWGFHJ+7p+n3dzaa1NIjjUVPP3h5dPqWLxYz\
9ZjGXHkjXUB0KXRhKuQEs9TdTE0vtA5viKP3qJkSR+xgi7N2yMUv3b72bNXlXSrm761WHXuFKS2Epnk/U7qEue6Saew6RBdorFff\
z5QW4pm9aUwpCN15eM/fXx6Ty7E42Bg7RgKaPU0QM7DuptYImAvScMk0Tt/hEG+PeA7rlIz+wUeYHhqpPQHtpisMlsrx1oPTpv1H\
C97C7Lum6TlMF0KETKP67LSl9PyfRbFzoNB52acffoDz2jGDpXLMMszXEC37+f9mSuEg8ctaQQTMHnIhQqaRnzItZ7ff+bdMKQK+\
PmV+Qv9V4n2PaR1q/hXV7oNHt0djpCSlsxbddT1TCoc5/1J2LJ65aZyp7Dq6ILp34W7AyLFkCV5+aoXPYpmBud/PlGJKssaOkZDS\
+S5TCuFkBjfInpq2tgQZuDQRhiMyJi7GZabESpOj/eHHmdIsTKW7mdIsAidbmFLESGxXroK7j3pV4vlSyUWz0uTofyf81voEhIyu\
OTfAQosv9wNFSMWRZdqBgT1AvDjR7Wt7C+fbdHKZjKmNKSydK9N4srfhzJxDGWZ3QNMQoxOWtX/FHAQRff1m4a5Nzv/770TftCXF\
NH0fINPXFXF896e+12em4fPwu7VZPalx+UrYj0IhVyiUzEFMYe/UrXmawdWnXuPrw4wsjHz0AzCXpgHH937q27+ANB/bXULGcD+H\
ZABBEIFAIJfLxeJ4dZCyV44PvPipNLjhelg0PYdnNOI4/vZnvj/Pyl3mRtN1aEYz+FRMudt58y6OP7UzkyNWsDd2fO6ejUwpHObC\
a8AW+g59CuVAazeoJyotAubiXaRj7vhvVoMlxzLA6lRmQQvkePBHIErbrgfnt2RzYS6/Hm4nJmfuHEg6XTzffO1q46kKpsQRU9g+\
7R+YfyxFQuA8dZxIgoYe+O69i912JR6crshiShyxhr2r307lVG3e8TX5aIDIHE/8FObXbqpjShyxJgmsY4hjawsT7iU5Nx1XkkmO\
CYfTYrxJAjnueecsZDOhhMYhiXql0KXz3uYyTovLQBLIMW942pZbL9y1HKvFhTi4sxqE2L6Km8m/HCRBQw9Qd7qvuSaP5DOdcnFt\
+tm3Z824Pi4dshwLkhyx46mr8kNaBJ65p4kpxQFOiwkkKVMZr1jgxeIy/HMgc9rEl289f+TBP4YfscYRD5I1s37m65uYUkw5cF0t\
XXjgj0chJMAIQuLDWdgttFJJVjkCkGEEIl7c0aJYeEzU1NxZ6ps22JtT5PKQxHIEfvONzXu/sZk5mBvQ2Z++0jhPS824Vj7PWY5l\
Izky60i4Z98XGtu06QdjWvmfb6lnDqZw4ztnc0YsKEmCyXx3e+WELszwnNnmkNPrMrBy5BhbSjvHd35yeVNYTovLwxUgR5J89LlP\
4F+zUvziXzXSdRGy5syAWSPtzYv9TrkcYUnu2DESaC0CM1x5JDTX5nJaXE5WvhxHuGbt5GHly3H/njWTGmoG6q/uXzgH50gsXCrD\
wSJWvnXkSCI4OXKwCE6OHCyCkyMHi+DkyMEiODlysAhOjhwsgpMjB4vg5MjBIjg5crAITo4cLIKTIweL4OTIwSI4OXKwCE6OHCyC\
kyMHi+DkyMEaeLz/D2sOoz1TsPKvAAAAAElFTkSuQmCC"

    logo_img = PhotoImage(data=logo_b64)
    label_logo = ttk.Label(frame0, image=logo_img)
    label_logo.grid(row=0, column=0, pady=8)

    #---

    frame1 = ttk.Frame(about_win)
    frame1.grid(row=0, column=1, padx=10, pady=5)

    about0_1 = ttk.Label(frame1, text=script_name, anchor='center')
    about0_1.grid(row=0, column=0, columnspan=2)
    about0_1.config(font=('', 12, 'bold'))

    div1 = ttk.Separator(frame1, orient='horizontal')
    div1.grid(row=1, column=0, columnspan=2, sticky='ew', pady=4)

    about1_0 = ttk.Label(frame1, text='Version: ')
    about1_0.grid(row=2, column=0, sticky='e', pady=1)
    about1_1 = ttk.Label(frame1, text=version + ' | ' + release_date)
    about1_1.grid(row=2, column=1, sticky='w')

    about3_0 = ttk.Label(frame1, text='Author: ')
    about3_0.grid(row=3, column=0, sticky='e', pady=1)
    about3_1 = ttk.Label(frame1, text='KWAN')
    about3_1.grid(row=3, column=1, sticky='w')

    about4_0 = ttk.Label(frame1, text='Website: ')
    about4_0.grid(row=4, column=0, sticky='e', pady=1)
    about4_1 = ttk.Label(frame1, text=github_url[:35] + '...', cursor='hand2', foreground='blue')
    about4_1.grid(row=4, column=1, sticky='w')
    about4_1.bind('<Button-1>', lambda e: webbrowser.open(github_url, 1))

    div2 = ttk.Separator(frame1, orient='horizontal')
    div2.grid(row=5, column=0, columnspan=2, sticky='ew', pady=4)

    sys5_0 = ttk.Label(frame1, text='Platform: ')
    sys5_0.grid(row=6, column=0, sticky='e', pady=1)
    sys5_1 = ttk.Label(frame1, text=sys.platform)
    sys5_1.grid(row=6, column=1, sticky='w')

    systext = sys.version.replace(' (', '\n(', 1).replace(r') [', ')\n[')
    sys6_0 = ttk.Label(frame1, text='Python: ')
    sys6_0.grid(row=7, column=0, sticky='ne', pady=1)
    sys6_1 = ttk.Label(frame1, text=systext, justify='left')
    sys6_1.grid(row=7, column=1, sticky='nw')

    sys7_0 = ttk.Label(frame1, text='TK: ')
    sys7_0.grid(row=8, column=0, sticky='e', pady=1)
    sys7_1 = ttk.Label(frame1, text=tk.TkVersion)
    sys7_1.grid(row=8, column=1, sticky='w')

    ok_btn = ttk.Button(about_win, text='OK', command=about_win.destroy)
    ok_btn.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky='nsew')

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

    win_ref.update_idletasks()  #force to update w & h
    ab_w = win_ref.winfo_width()  #retreive the 'window' w & h
    ab_h = win_ref.winfo_height()

    x = x + (app_w / 2) - (ab_w / 2)  #calculate the x, y
    y = y + (app_h / 2) - (ab_h / 2)

    win_ref.geometry('+%d+%d' % (x, y))  #position it!
    win_ref.deiconify()  #bring it back

    window.attributes('-disabled', 1)  #disabled the main window

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
window.title(script_name)
window.resizable(False, False)

#---------------------------------------------------------------------------
#window menu

menu = tk.Menu(window)

file_item = tk.Menu(menu, tearoff=0)
file_item.add_command(label='About', command=about_window)
file_item.add_separator()
file_item.add_command(label='Exit', command=lambda: window.destroy())
menu.add_cascade(label='File', menu=file_item)
menu.add_command(label='Help', command=lambda: webbrowser.open(github_url, 1))


window.config(menu=menu)

#---

r_click_popup = tk.Menu(window, tearoff=0, fg='blue')
r_click_popup.add_command(label="Open meetup", command=lambda: webbrowser.open(r_click_url, 1))

r_click_popup2 = tk.Menu(window, tearoff=0, fg='blue')
r_click_popup2.add_command(label="Delete local file", command=delete_local_file)

#------------------------------------------------------------------
#group area

group_frame = ttk.Frame(window)
group_frame.grid(row=0, column=0, padx=5, pady=5, stick='nw')

#---

lb_header = ['g_index', 'Group', 'Country', 'Members']
group_list = ttk.Treeview(columns=lb_header, show='headings', selectmode='browse', height=6, padding='6 6 6 6')
group_list.grid(row=0, column=0, columnspan=2, in_=group_frame)
group_list.bind('<ButtonRelease-1>', group_clicked)
group_list.bind("<Button-3>", group_r_clicked)

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

div = ttk.Separator(window, orient='horizontal')
div.grid(row=1, column=0, sticky='ew')

#------------------------------------------------------------------
#event area

event_frame = ttk.Frame(window)
event_frame.grid(row=2, column=0, padx=5, pady=5, stick='nw')

#---

lb_header = ['e_index', 'e_id', 'Date', 'Event', 'Photos']
event_list = ttk.Treeview(columns=lb_header, show='headings', selectmode='browse', height=18, padding='6 6 6 6')
event_list.grid(row=0, column=0, columnspan=4, in_=event_frame)
event_list.bind('<ButtonRelease-1>', event_clicked)
event_list.bind("<Button-3>", event_r_clicked)

event_list.column('Date', width=80, anchor='center')
event_list.column('Event', width=390, anchor='w')
event_list.column('Photos', width=50, anchor='e')
event_list['displaycolumns'] = ('Date', 'Event', 'Photos')

for col in lb_header:
    event_list.heading(col, text=col, anchor='w')

event_list.heading('Photos', anchor='e')

event_list.tag_configure('nophoto', background='#F4F0FE', foreground='grey')

#---

event_status = tk.StringVar()
event_frame_status = ttk.Label(event_frame, textvariable=event_status, anchor='w', width=46)
event_frame_status.grid(row=1, column=0, sticky='nsew')

all_event = tk.IntVar()
all_event.set(1)
event_checkbox = ttk.Checkbutton(event_frame, text="All Events", variable=all_event, onvalue=1, offvalue=0,
                                 command=lambda: retrieve_events(selected_year, 0))
event_checkbox.grid(row=1, column=1, sticky='e')
event_checkbox.configure(state='disabled')

var_year = tk.StringVar()
var_year.set('Recent')  #default value
option_year = ttk.OptionMenu(event_frame, var_year, 'Recent', command=year_clicked)
option_year.grid(row=1, column=2, sticky='e')
option_year.configure(state='disabled')

event_refresh_btn = ttk.Button(event_frame, text='Refresh', command=lambda: retrieve_events(selected_year, 1),
                               state='disabled')
event_refresh_btn.grid(row=1, column=3, sticky="e")

#------------------------------------------------------------------

div = ttk.Separator(window, orient='vertical')
div.grid(row=0, column=1, rowspan=3, sticky='ns')

#------------------------------------------------------------------
#photo album area

album_frame = ttk.Frame(window)
album_frame.grid(row=0, column=2, rowspan=3, padx=5, pady=5, sticky='nw')

#---

album_btn4 = ttk.Button(album_frame, text='DL folder', command=lambda: os.startfile(os.path.realpath(str(event_id))), state='disabled')
album_btn4.grid(row=0, column=0, sticky='nsew')

album_btn3 = ttk.Button(album_frame, text='Clear all', command=album_select_none, state='disabled')
album_btn3.grid(row=0, column=1, sticky='nsew')

album_btn2 = ttk.Button(album_frame, text='Select all', command=album_select_all, state='disabled')
album_btn2.grid(row=0, column=2, sticky='nsew')

album_btn1 = ttk.Button(album_frame, text='Download', command=album_download, state='disabled')
album_btn1.grid(row=0, column=3, sticky='nsew')

#---

lb_header = ['No', 'Photo', 'Date', 'Time', 'Uploaded by']
photo_list = ttk.Treeview(columns=lb_header, show='headings', selectmode='extended', height=27, padding='6 6 6 6')
photo_list.grid(row=1, column=0, columnspan=4, in_=album_frame, sticky='w')
photo_list.bind("<ButtonRelease-1>", photo_clicked)
photo_list.bind("<Button-3>", photo_r_clicked)

photo_list.column('No', width=40, anchor='e')
photo_list.column('Photo', width=160, anchor='center')
photo_list.column('Date', width=90, anchor='center')
photo_list.column('Time', width=90, anchor='center')
photo_list.column('Uploaded by', width=100, anchor='center')

for col in lb_header:
    photo_list.heading(col, text=col)

photo_list.tag_configure('nodl', background='#F4F0FE', foreground='grey')

#---

album_status = tk.StringVar()
album_frame_status = ttk.Label(album_frame, textvariable=album_status, anchor='w')
album_frame_status.grid(row=2, column=0, columnspan=3, sticky='w')

album_refresh_btn = ttk.Button(album_frame, text='Refresh', command=lambda: retrieve_album(1), state='disabled')
album_refresh_btn.grid(row=2, column=3, sticky='e')

#------------------------------------------------------------------

#https://stackoverflow.com/questions/56329342/tkinter-treeview-background-tag-not-working
style = ttk.Style()
style.map('Treeview', foreground=fixed_map('foreground'), background=fixed_map('background'))
#end-copy

style.configure("Treeview.Heading", foreground='blue')

#---

#postion main window in the middle of the screen
ws = window.winfo_screenwidth()  #width of the screen
hs = window.winfo_screenheight()  #height of the screen

window.withdraw()  #remove window, to reduce window flashing due reposition most of the time

window.update_idletasks()  #force update, to update window w & h
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
    messagebox.showerror('Error', 'access token is missing, please run tk-mpd-config.py')
    window.destroy()
    sys.exit(1)
    
#member_name = user_profile(0)

retrieve_group(0)

window.mainloop()
