import tkinter as tk
import tkinter.ttk as ttk
from tkinter import PhotoImage
from datetime import datetime
import os
import sys
import platform
import json
import webbrowser
import asyncio
import async_timeout
import aiohttp
import requests

# ------------------------------------------------------------------------
# Global Variable
Selected_Year = "Recent"
Group_idx = ""
Event_idx = Event_File = ""
Album_File = ""
Download_Folder = ""
R_Click_URL1 = R_Click_URL2 = ""

# Global constant
VERSION = "1.21"
RELEASE_DATE = "12-Dec-2020"
PROGRAM_NAME = "Python/Tk Meetup Photos Downloader"
GITHUB_URL = "https://github.com/fishcode16/python-tk-meetup-photos-downloader"
MEETUP_API = "https://api.meetup.com/"
MEETUP_COM = "https://www.meetup.com/"
CONFIG_FILE = "config.json"
ACCESS_FILE = "access.json"
USER_FILE = "user.json"
GROUP_FILE = "group_data/groups.json"
LOGO_B64 = """
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
fwgGxRawQGTpAAAAAElFTkSuQmCC
"""

# ------------------------------------------------------------------------


def today_str(date_timestamp=0):
    "Return the date/time string format. If no input, use today's"

    if date_timestamp > 0:
        ftime = datetime.fromtimestamp(date_timestamp / 1000)
    else:
        ftime = datetime.today()
    return ftime.strftime("%a, %d %b %Y, %r")


# ------------------------------------------------------------------------


def date_fmt_str(date_timestamp):
    "Return the date only string"

    return datetime.fromtimestamp(date_timestamp / 1000).strftime("%d-%b-%Y")


# ------------------------------------------------------------------------


def last_updated(file):
    "Return the number of hours since the file was last modified."

    if os.path.exists(file):
        # obtain the file modification time (in seconds)
        ftime = datetime.fromtimestamp(os.path.getmtime(file))
        # elapse (in hours)
        hours = round((datetime.now() - ftime).total_seconds() / 3600)
    else:
        hours = -1  # return -1 if file is missing

    return hours


# ------------------------------------------------------------------------


def need_update(file, max_hr):
    """Determine if an update is needed. Update is needed if the last
    modification file time is greater then max_hr or the file is missing,
    else no update is required."""

    # obtain the number of hours since file was last modified
    hours = last_updated(file)
    if hours < 0:  # file is missing, update needed
        update_needed = 1
    elif hours > max_hr:  # >max_hr, update needed
        update_needed = 1
    else:
        update_needed = 0  # else no update needed

    return update_needed


# ------------------------------------------------------------------------


def retrieve_token():
    """Obtain the access token from ACCESS_FILE. ACCESS_FILE is created
    by 'tk-mpd-config.pyw' script."""

    # Set a very high max_hr, so no update is require.
    # (FUTURE) handle access token expiry.
    if need_update(ACCESS_FILE, 999999):
        token = ""  # when ACCESS_FILE is missing
    else:
        data = json.loads((open(ACCESS_FILE).read()))

        # attempt to extract data from json file
        try:
            token = {
                "Authorization":
                data["token_type"] + " " + data["access_token"]
            }
        except:
            token = ""  # invalid json file content

    return token


# ------------------------------------------------------------------------


def load_json(url, params, json_file, max_hr, force_update):
    """Retrieve json data either from online/meetup or extract from local
    file.  If data is upto date (based on max_hr), then is read from file,
    else would http request from online/meetup. Update can be force by
    setting force_update."""

    if need_update(json_file, max_hr) or force_update:

        # Retrieve data from meetup.com
        r = requests.get(url=url, headers=headers, params=params)
        data = r.json()

        if r.status_code == 200:
            # save data/json to file
            text_file = open(json_file, "w", encoding="utf_16")
            text_file.write(json.dumps(data, indent=4))
            text_file.close()
        else:
            # Encountered an error, print for debug
            # (FUTURE) Debug tickbox. output to a file/window
            print("URL: " + url)
            print("PARAMS: " + params)
            print("STATUS: " + str(r.status_code) + ":" + r.reason)
            print("HEADER: " + str(r.headers))
            print("TEXT: " + r.text)

    else:
        # read from file
        data = json.loads((open(json_file, encoding="utf_16").read()))

    return data


# ------------------------------------------------------------------------


def user_profile(force_update=0):
    "Retrieve member's profile. UNUSED at the moment"

    url = MEETUP_API + "members/self"
    max_hr = 720  # auto-refresh user file every month (24*30 hrs)
    user_json = load_json(url, "", USER_FILE, max_hr, force_update)

    member_name = user_json["name"]

    return member_name


# ------------------------------------------------------------------------


def init_app():
    """Retrieve application setting from config file. Create application's folders
    and/or config file (with default setting), if they doesn't exist."""

    # Check if application folders' exist
    for folder in ("group_data", "download"):
        if not os.path.exists(folder):
            os.mkdir(folder)  # Create folder

    default_config = {
        "iptc_tag": False,
        "mtime_tag": True,
        "photo_list_tag": True
    }

    # Create config file (if it doesn't exist)
    if not os.path.exists(CONFIG_FILE):
        # Save data/json to file
        text_file = open(CONFIG_FILE, "w")
        text_file.write(json.dumps(default_config, indent=4))
        text_file.close()

    # Load config json
    config_data = json.loads((open(CONFIG_FILE).read()))

    # check for missing config tag (set it to default if any)
    for config_item in default_config:
        try:  # test if config tag exist
            dummy = config_data[config_item]
        except:  # if missing, set it to default
            config_data[config_item] = default_config[config_item]

    return config_data


# ------------------------------------------------------------------------


def last_updated_msg(file):
    "Return a human friendly last updated message"

    hours = last_updated(file)
    if hours >= 2232:  # event older then 3 months
        msg = "3 months ago"
    elif hours >= 744:  # event older then a month
        msg = "a months ago"
    elif hours >= 336:  # event is between 2-4 weeks
        msg = "2 weeks ago"
    elif hours >= 168:  # event is between 1-2 weeks
        msg = "a weeks ago"
    elif hours >= 48:  # more then 2 days
        msg = "%d days ago" % int(hours / 24)
    elif hours >= 24:  # more then a day
        msg = "a days ago"
    elif hours > 1:  # more then an hour
        msg = "%d hours ago" % hours
    elif hours == 1:  # an hour
        msg = "an hour ago"
    else:
        msg = "within an hour"

    return "Last updated " + msg


# --------------------------------------------------------------------------


def treeview_sort_column(treeview_ref, col_id, reverse, sort_type):
    "Sort the treeview column. sort_type = 0 (text), 1 (int), 2 (date)"

    data_to_sort = []
    for key in treeview_ref.get_children(""):
        column_data = treeview_ref.set(key, col_id)
        data_to_sort.append([column_data, key])

    if sort_type == 1:  # integer
        data_to_sort.sort(key=lambda t: int(t[0]), reverse=reverse)
    elif sort_type == 2:  # date
        data_to_sort.sort(key=lambda t: datetime.strptime(t[0], "%d-%b-%Y"),
                          reverse=reverse)
    else:  # text
        data_to_sort.sort(reverse=reverse)

    # rearrange items in sorted positions
    for index, (val, key) in enumerate(data_to_sort):
        treeview_ref.move(key, "", index)

    # reverse the sort next time
    treeview_ref.heading(col_id,
                         command=lambda _col=col_id: treeview_sort_column(
                             treeview_ref, _col, not reverse, sort_type))


# ------------------------------------------------------------------------


def clear_treeview(treeview_ref):
    "Remove all treeview data"

    for child in treeview_ref.get_children():
        treeview_ref.delete(child)


# ------------------------------------------------------------------------


def display_update_message(frame_ref, msg_ref):
    "display an 'updating' message on the status bar"

    frame_ref.configure(background="pale green")
    msg_ref.set(" Updating....")
    frame_ref.update()  # force update


# ------------------------------------------------------------------------


def clear_group_frame():
    "Clear the content of the group frame"

    global Group_idx

    Group_idx = ""

    clear_treeview(group_tree)

    group_frame_status.configure(background="gainsboro")


# --------------------------------------------------------------------------


def clear_event_frame():
    "clear the content of the event frame"

    global Event_idx, Download_Folder

    Event_idx = Download_Folder = ""

    clear_treeview(event_tree)

    event_frame_buttons("disabled")
    event_frame_status.configure(background="gainsboro")
    event_status.set("")


# --------------------------------------------------------------------------


def clear_album_frame():
    "clear the content of the album frame"

    clear_treeview(photo_tree)

    album_frame_buttons("disabled")
    album_frame_status.configure(background="gainsboro")
    album_status.set("")


# --------------------------------------------------------------------------


def display_group_frame(force_update=0):
    "Retrieve member's subscribed groups and display it (group frame)"

    global Group_List

    # setup variables for API call
    url_api = MEETUP_API + "self/groups"
    params = {"fields": "self"}
    max_hr = 72  # auto-refresh group list every 3 days (24*3 hrs)

    # display the update message
    display_update_message(group_frame_status, group_status)

    # retrieve json data from meetup or cached file
    group_json = load_json(url_api, params, GROUP_FILE, max_hr, force_update)

    # process the json data
    Group_List = []
    for json_idx in range(
            200):  # meetup return max 200, would someone have >200 groups?
        try:
            # extract the needed data
            g_name = group_json[json_idx]["name"]
            g_country = group_json[json_idx]["localized_country_name"]
            g_members = group_json[json_idx]["members"]
            g_id = group_json[json_idx]["id"]
            g_url = group_json[json_idx]["urlname"]
            g_created = group_json[json_idx]["created"]

            g_created_year = datetime.fromtimestamp(g_created / 1000).year

            # populate Group_List
            Group_List.append(
                [g_name, g_country, g_members, g_id, g_url, g_created_year])

            # Create the group's folder (gid),  if it doesn't exist
            g_folder = "group_data/gid-" + str(g_id) + "/"
            if not os.path.exists(g_folder):
                os.makedirs(g_folder)  # create the group folder

            # Create the group's info file (00-group.txt), if it doesn't exist
            g_readme_file = g_folder + "00-group.txt"
            if not os.path.exists(g_readme_file):

                g_created_str = date_fmt_str(
                    group_json[json_idx]["created"])  # group creation date

                g_joined_str = date_fmt_str(
                    group_json[json_idx]["self"]["profile"]["group_profile"]
                    ["created"])  # member joined group date

                # create 00-group.txt (list some of the group's information)
                text_file = open(g_readme_file, "w", encoding="utf_16")
                text_file.writelines([
                    "Group Name: %s\n" % (g_name),
                    " Group URL: %s\n" % (MEETUP_COM + g_url),
                    "   Country: %s\n" % (g_country),
                    "Created on: %s\n" % (g_created_str),
                    " Joined on: %s\n\n" % (g_joined_str),
                    "*this file was auto-created on: %s\n" % (today_str())
                ])
                text_file.close()

        except:
            break

    # display an error message and quit, when user has no joined groups
    if not Group_List:
        mesg_box("error", "You have not join any groups")
        window.destroy()
        sys.exit(1)  # exit!

    Group_List.sort()  # sort by group name (default)

    # clear all frames
    clear_album_frame()
    clear_event_frame()
    clear_group_frame()

    # Display the list of groups (populate treeview)
    for g_idx, (g_name, g_country, g_members, *dummy) in enumerate(Group_List):
        group_tree.insert("",
                          "end",
                          values=(g_idx, g_name, g_country, g_members))

    # status message
    group_status.set(" %d groups | " % len(group_tree.get_children()) +
                     last_updated_msg(GROUP_FILE))


# --------------------------------------------------------------------------


def group_clicked(event):
    "Show which group was selected"

    global Group_idx, R_Click_URL1

    # selected item (treeview)
    item_id = group_tree.identify_row(event.y)
    if item_id:  # only do something, if there is an item selected
        selected_item = group_tree.item(item_id)
        g_idx = selected_item["values"][0]  # retrive the index

        # refresh event frame. if the selected group is different from
        # the current selection
        if Group_idx != g_idx:
            Group_idx = g_idx  # set global variable to the selected group
            display_event_frame()  # update the event frame

        if event.num == 3:  # right click
            group_tree.selection_set(item_id)  # set and focus the selection
            group_tree.focus(item_id)

            # retrieve the selected group information
            (g_name, g_country, g_members, g_id, g_url,
             g_created_year) = Group_List[g_idx]

            # setup the group URL
            R_Click_URL1 = MEETUP_COM + g_url

            # pop up the menu at the mouse pointer
            r_click_popup1.tk_popup(event.x_root, event.y_root, 0)


# --------------------------------------------------------------------------


def display_event_frame(force_update=0):
    "Retrieve group's events and display it (event frame)"

    global Event_List, Event_File, Selected_Year

    # retrieve the selected group information
    (g_name, g_country, g_members, g_id, g_url,
     g_created_year) = Group_List[Group_idx]

    # setup variables for API call
    url_api = MEETUP_API + g_url + "/events"

    # if the current year selection is before the group creation year
    # then set the year selection menu to "Recent"
    if Selected_Year != "Recent" or Selected_Year == "":
        if int(Selected_Year) < g_created_year:
            Selected_Year = "Recent"

    # setup params and max_hr (determine by Selected_Year)
    if Selected_Year == "Recent":
        # retrieve the recent 15 past events
        params = {
            "status": "past",
            "page": "15",
            "desc": "true",
            "fields": "photo_album"
        }
        max_hr = 3  # recent event list (refresh every 6 hrs)
    else:
        # retrieve all the past events for the year
        params = {
            "status": "past",
            "no_earlier_than": str(Selected_Year) + "-01-01T00:00:00.000",
            "no_later_than": str(Selected_Year) + "-12-31T23:59:00.000",
            "fields": "photo_album"
        }
        # yearly event list. Refresh every 2 months (2*30*24) unless
        # is the current year (24 hr)
        if int(Selected_Year) == datetime.today().year:
            max_hr = 24
        else:
            max_hr = 1440

    # setup Event_File
    Event_File = "group_data/gid-" + str(g_id) + "/events-" + str(
        Selected_Year) + ".json"

    # display the update message
    display_update_message(event_frame_status, event_status)

    # retrieve json data from meetup or cached file
    event_json = load_json(url_api, params, Event_File, max_hr, force_update)

    # process the json data
    Event_List = []
    for json_idx in range(500):  # meetup return max 500?
        try:

            e_name = event_json[json_idx]["name"].strip()
            e_id = event_json[json_idx]["id"]
            e_time = event_json[json_idx]["time"]
            e_link = event_json[json_idx]["link"]

            try:  # extract photos count
                e_photo_count = event_json[json_idx]["photo_album"][
                    "photo_count"]
                e_album_id = event_json[json_idx]["photo_album"]["id"]
            except:  # no photo in event
                e_photo_count = 0
                e_album_id = ""

            # populate Event_List
            Event_List.append(
                [e_name, e_id, e_time, e_link, e_photo_count, e_album_id])

        except:
            break

    # display the events in event frame
    update_event_frame()


# --------------------------------------------------------------------------


def update_event_frame():
    "display the events in event frame"

    global Selected_Year

    clear_album_frame()
    clear_event_frame()

    # retrieve the selected group information
    (g_name, g_country, g_members, g_id, g_url,
     g_created_year) = Group_List[Group_idx]

    # populate the year selection menu
    option_year["menu"].delete(0, "end")  # delete the list

    # first entry: Recent
    option_year["menu"].add_command(label="Recent",
                                    command=tk._setit(var_year, "Recent",
                                                      year_clicked))

    # fill from current year till group creation year
    for year in range(datetime.today().year, g_created_year - 1, -1):
        option_year["menu"].add_command(label=year,
                                        command=tk._setit(
                                            var_year, year, year_clicked))

    # if the current year selection is before the group creation year
    # then set the year selection to "Recent"
    if Selected_Year != "Recent" or Selected_Year == "":
        if int(Selected_Year) < g_created_year:
            Selected_Year = "Recent"
    var_year.set(Selected_Year)

    # Set the next sort order for the date field
    if Selected_Year == "Recent":
        sort_order = False  # as it is already reverse sort
    else:
        sort_order = True  # set to reverse sort
    event_tree.heading("Date",
                       command=lambda _col="Date": treeview_sort_column(
                           event_tree, _col, sort_order, 2))

    # obtain checkbox status
    checkbox = event_checkbox.instate(["selected"])

    # Display the list of events (populate treeview)
    for e_idx, (e_name, e_id, e_time, e_link, e_photo_count,
                e_album_id) in enumerate(Event_List):

        # for row highlighting. set tag for events with no photos
        if e_photo_count:
            taggy = ""
        else:
            taggy = "no_photo"  # no photos for the event

        # if checkbox, then display all events, else only events with photos
        if checkbox or e_photo_count:
            event_tree.insert("",
                              "end",
                              tags=taggy,
                              values=(e_idx, e_id, date_fmt_str(e_time),
                                      e_name, e_photo_count))

    event_frame_buttons("!disabled")  # enable all the buttons

    # status message
    event_status.set(" %d events | " % len(event_tree.get_children()) +
                     last_updated_msg(Event_File))


# --------------------------------------------------------------------------


def year_clicked(event):
    "refresh event list after user selected a year"

    global Selected_Year

    # refresh event frame. if the selected year is different from
    # the current selection
    year_selected = var_year.get()
    if Selected_Year != year_selected:
        Selected_Year = year_selected
        display_event_frame()


# --------------------------------------------------------------------------


def event_clicked(event):
    "show which event was selected"

    global Event_idx, R_Click_URL1, R_Click_URL2

    # selected item (treeview)
    item_id = event_tree.identify_row(event.y)
    if item_id:  # only do something, if there is an item selected
        selected_item = event_tree.item(item_id)
        e_idx = selected_item["values"][0]  # retrive the index

        # retrieve the selected event information
        (e_name, e_id, e_time, e_link, e_photo_count,
         e_album_id) = Event_List[e_idx]

        # refresh album frame. if the selected event is different from
        # the current selection
        if Event_idx != e_idx:
            Event_idx = e_idx  # setlected event

            if e_photo_count:
                display_album_frame()
            else:  # if no photos in the event
                clear_album_frame()
                album_status.set("No photos")

        if event.num == 3:  # right click
            event_tree.selection_set(item_id)  # set and focus the selection
            event_tree.focus(item_id)

            # retrieve the selected group information
            (g_name, g_country, g_members, g_id, g_url,
             g_created_year) = Group_List[Group_idx]

            # setup the event URL
            R_Click_URL1 = e_link

            # setup the Album URL
            if e_photo_count:
                R_Click_URL2 = MEETUP_COM + g_url + "/photos/all_photos/?photoAlbumId=" + str(
                    e_album_id)
                r_click_popup2.entryconfig("Album Page", state="normal")
            else:  # disable the album link, as there is no photo in the album
                R_Click_URL2 = ""
                r_click_popup2.entryconfig("Album Page", state="disabled")

            # pop up the menu at the mouse pointer
            r_click_popup2.tk_popup(event.x_root, event.y_root, 0)


# --------------------------------------------------------------------------


def event_frame_buttons(state):
    "Enable/disabled all the buttons of the event_frame"
    # https://stackoverflow.com/questions/4236910/getting-checkbutton-state

    event_refresh_btn.state([state])
    option_year.state([state])
    event_checkbox.state([state])


# --------------------------------------------------------------------------


def display_album_frame(force_update=0):
    "retrieve event photo album"

    global Album_List, Album_File
    global Download_Folder

    # retrieve the selected event information
    (e_name, e_id, e_time, e_link, e_photo_count,
     e_album_id) = Event_List[Event_idx]

    # retrieve the selected group information
    (g_name, g_country, g_members, g_id, g_url,
     g_created_year) = Group_List[Group_idx]

    # setup download folder
    Download_Folder = "download/album-" + str(e_id) + "/"

    # determine refresh, max_hr. based on event date
    dt_object = datetime.fromtimestamp(e_time / 1000)
    hours = round((datetime.today() - dt_object).total_seconds() / 3600)

    if hours > 2232:  # event older then 3 months, auto refresh every 6 months
        max_hr = 4320
    elif hours > 744:  # event older then a month, auto refresh every 2 months
        max_hr = 1488
    elif hours > 336:  # event is between 2-4 weeks, auto refresh every week
        max_hr = 168
    elif hours > 168:  # event is between 1-2 weeks, auto refresh every 2 days
        max_hr = 48
    else:  # event is less then a week, auto refresh every 3 hours
        max_hr = 6

    # setup variables for API call
    url_api = MEETUP_API + g_url + "/events/" + str(e_id) + "/photos"
    params = {"page": 500}  # default is 200
    Album_File = "group_data/gid-" + str(g_id) + "/album-" + str(
        e_album_id) + ".json"

    # display the update message
    display_update_message(album_frame_status, album_status)

    # retrieve json data from meetup or cached file
    album_json = load_json(url_api, params, Album_File, max_hr, force_update)

    # process the json data
    Album_List = []
    album_photo_count = album_json[0]["photo_album"]["photo_count"]
    for json_idx in range(album_photo_count):  # max 500 photos per album

        p_id = album_json[json_idx]["id"]
        p_hires_url = album_json[json_idx]["highres_link"]
        p_upload_time = album_json[json_idx]["updated"]
        p_member = album_json[json_idx]["member"]["name"]

        # populate Album_List
        Album_List.append([p_id, p_hires_url, p_upload_time, p_member])

    # display the event's photos in album frame
    update_album_frame()


# --------------------------------------------------------------------------


def update_album_frame():
    "display the event's photos in album frame"

    # print(album_photo_count)
    # print(e_photo_count)
    # if diff, there is a mis-match, need to update

    clear_album_frame()

    # obtain checkbox status
    checkbox = album_checkbox.instate(["selected"])

    # Display the list of photos (populate treeview)
    need_dl_count = 0
    for p_idx, (p_id, p_hires_url, p_upload_time,
                p_member) in enumerate(Album_List):

        # upload date and time
        p_date = date_fmt_str(p_upload_time)
        p_time = datetime.fromtimestamp(p_upload_time /
                                        1000).strftime("%I:%M %p")

        # highlight downloaded photos (ie. found in download folder)
        photo_file = os.path.basename(p_hires_url)
        local_file = Download_Folder + photo_file
        if os.path.exists(local_file):
            taggy = "no_dl"
        else:
            taggy = "need_dl"
            need_dl_count += 1

        # if checkbox is checked, then display all photos,
        #  else only display the non-downloaded photos
        if checkbox or taggy == "need_dl":
            photo_tree.insert("",
                              "end",
                              tags=taggy,
                              values=(p_idx + 1, photo_file, p_date, p_time,
                                      p_member))

    album_frame_buttons("disabled")  # disabled all the buttons first

    album_refresh_btn.state(["!disabled"])  # enable the refresh button
    album_checkbox.state(["!disabled"])  # enable the checkbox

    # enable the 'select all' button, if there are files to be downloaded
    if need_dl_count:
        album_all_btn.state(["!disabled"])

    # enable "folder button", if download folder exist
    if os.path.exists(Download_Folder):
        album_folder_btn.state(["!disabled"])

    # status message
    album_status.set(" %d photos | " % len(photo_tree.get_children()) +
                     last_updated_msg(Album_File))


# --------------------------------------------------------------------------


def photo_clicked(event):
    "Enable the download button, if there are photo(s) selected for download."

    # If there is selection
    if photo_tree.selection():
        album_none_btn.state(["!disabled"])  # enable 'clear all' button
        # Scan through selection. Enable the 'download' button if there is
        #  at least one photo is eligible for download
        for item_id in photo_tree.selection():
            selected_item = photo_tree.item(item_id)
            tags = selected_item["tags"][0]
            if tags == "need_dl":
                album_download_btn.state(["!disabled"])
                break


# --------------------------------------------------------------------------


def photo_r_clicked(event):
    "right click - open up meetup page. double click - open up local file"

    global R_Click_URL1

    # selected item (treeview)
    item_id = photo_tree.identify_row(event.y)
    if item_id:  # only do something, if there is an item selected
        selected_item = photo_tree.item(item_id)
        p_idx = selected_item["values"][0]  # retrive the index
        photo_file = selected_item["values"][1]
        tags = selected_item["tags"][0]

        # retrieve the selected group information
        (g_name, g_country, g_members, g_id, g_url,
         g_created_year) = Group_List[Group_idx]

        # retrieve the selected event information
        (e_name, e_id, e_time, e_link, e_photo_count,
         e_album_id) = Event_List[Event_idx]

        # retrieve the selected photo information
        (p_id, p_hires_url, p_upload_time, p_member) = Album_List[p_idx - 1]

        if event.num == 3:  # right click
            photo_tree.selection_set(item_id)  # set and focus the selection
            photo_tree.focus(item_id)

            R_Click_URL1 = MEETUP_COM + g_url + "/photos/" + str(
                e_album_id) + "/" + str(p_id)

            # pop up the menu at the mouse pointer
            r_click_popup3.tk_popup(event.x_root, event.y_root, 0)

        # double-click
        # if the file is tag with 'no_dl' (ie. file exist in folder)
        elif tags == "no_dl":
            os.startfile(cwd + "/" + Download_Folder + photo_file)
            # open the image using default system handler


# --------------------------------------------------------------------------


def album_frame_buttons(status):
    "enable/disabled all the buttons of the album_frame"

    album_folder_btn.state([status])
    album_none_btn.state([status])
    album_all_btn.state([status])
    album_download_btn.state([status])
    album_checkbox.state([status])
    album_refresh_btn.state([status])


# --------------------------------------------------------------------------


def album_select_all(yes=0):
    """select all or de-select all the items/photos in the album frame.
    https://youtu.be/zoLOXN_9EH0"""

    if yes:  # select all items
        for item in photo_tree.get_children():
            photo_tree.selection_add(item)
        # enable the 'clear all' and 'download' buttons
        album_none_btn.state(["!disabled"])
        album_download_btn.state(["!disabled"])

    else:  # de-select all items
        for item in photo_tree.get_children():
            photo_tree.selection_remove(item)
        # disable the 'clear all' and 'download' buttons, since nothing was
        #  selected
        album_none_btn.state(["disabled"])
        album_download_btn.state(["disabled"])


# --------------------------------------------------------------------------


def album_download():
    "download the selected photos, called from DL button's command"

    # proceed if there are selections
    if photo_tree.selection():

        # loop through the selections, determine how many photos
        # need to be downloaded
        dl_list_url = []  # list of URLs for download function
        dl_list_idx = []  # list of idx for post-download processing
        for item_id in photo_tree.selection():
            selected_item = photo_tree.item(item_id)
            p_idx = selected_item["values"][0] - 1
            photo_file = selected_item["values"][1]
            tags = selected_item["tags"][0]

            (p_id, p_hires_url, p_upload_time, p_member) = Album_List[p_idx]

            # if the photo was tag "need_dl" (ie. photo is not on system),
            # then add to download list
            if tags == "need_dl":
                dl_list_url.append(p_hires_url)
                dl_list_idx.append([p_idx, photo_file])

        if dl_list_url:  # download only if there are files to download

            if not os.path.exists(Download_Folder):
                os.mkdir(Download_Folder)  # create download folder if missing

            # create 00-event.txt file with the event's information
            e_readme_file = Download_Folder + "00-event.txt"
            if not os.path.exists(e_readme_file):

                # retrieve the selected group information
                (g_name, g_country, g_members, g_id, g_url,
                 g_created_year) = Group_List[Group_idx]

                # retrieve the selected event information
                (e_name, e_id, e_time, e_link, e_photo_count,
                 e_album_id) = Event_List[Event_idx]

                text_file = open(e_readme_file, "w", encoding="utf_16")
                text_file.writelines([
                    "    Group: %s\n" % (g_name),
                    "    Event: %s\n" % (e_name),
                    "Event URL: %s\n" % (e_link),
                    "     Date: %s\n\n" % (today_str(e_time)),
                    "*this file was auto-created on: %s\n" % (today_str())
                ])
                text_file.close()

            download_photos(dl_list_url)  # download the photos!!

            # Post-download processing.
            #  IPTC tag (future), modify access date/time, photo index

            # IPTCinfo when ready (failed with images from meetup)
            # -group, event name, event date/time
            # -caption, uploaded by, datetime
            # -comments, tag on image?
            if iptc_tag.get():
                pass

            # modify the file's access date/time to upload date/time
            #  unable to find a way to modify the file's creation date/time
            if mtime_tag.get():
                for (p_idx, photo_file) in dl_list_idx:
                    (p_id, p_hires_url, p_upload_time,
                     p_member) = Album_List[p_idx]

                    photo_date = int(p_upload_time / 1000)
                    os.utime(Download_Folder + photo_file,
                             (photo_date, photo_date))

            # create a text file (with the event's photo information
            if photo_list_tag.get():

                text_file = open(Download_Folder + "00-photos.txt",
                                 "w",
                                 encoding="utf_16")
                text_file.writelines([
                    "Photo filename", "\t\t", "|  Upload Date", "\t\t",
                    "|  Upload Time", "\t\t", "|  Uploaded by", "\n",
                    "------------------------+", "-----------------------+",
                    "-----------------------+", "-----------------------", "\n"
                ])

                # loop through all the event's photo (irregardless if it
                # was downloaded)
                for (p_id, p_hires_url, p_upload_time, p_member) in Album_List:

                    photo_file = os.path.basename(p_hires_url)
                    p_dt_str = datetime.fromtimestamp(
                        p_upload_time /
                        1000).strftime("%d-%b-%Y \t|\t%I:%M %p")

                    text_file.writelines([
                        photo_file, "\t|\t", p_dt_str, "\t|\t", p_member, "\n"
                    ])

                text_file.write("\n*this file was auto-created on: %s\n" %
                                (today_str()))
                text_file.close()


# --------------------------------------------------------------------------


def download_photos(dl_list_url):
    "Initiate the download of photos in the dl_list_url"

    # create a window/frame with a border
    (download_win, frame) = border_frame()

    download_msg = tk.StringVar()
    label0 = ttk.Label(frame,
                       style="msgbox.TLabel",
                       textvariable=download_msg,
                       anchor="center",
                       width=30)
    label0.grid(row=0, column=0, padx=20, pady=5, sticky="nsew")
    msg = "Downloading %d files" % (len(dl_list_url))
    download_msg.set(msg)

    download_photos.progress_bar = ttk.Progressbar(frame,
                                                   orient="horizontal",
                                                   mode="determinate",
                                                   value=0)
    download_photos.progress_bar.grid(row=1, column=0, sticky="nsew", padx=10)

    ok_btn = ttk.Button(frame, text="OK", command=download_win.destroy)
    ok_btn.grid(row=2, column=0, sticky="nsew", padx=60, pady=10)
    ok_btn.state(["disabled"])

    position_window(download_win)

    # ---

    # download!
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(async_dl(loop, dl_list_url))

    # ---

    msg = "%d file(s) downloaded!" % (len(dl_list_url))
    download_msg.set(msg)
    ok_btn.state(["!disabled"])

    download_win.wait_window()  # wait for user to close the window
    window.attributes("-disabled", 0)  # enable the main window

    display_album_frame()


# --------------------------------------------------------------------------


async def async_dl(loop, dl_list_url):

    async_dl.count = 0
    async_dl.total = len(dl_list_url)

    async with aiohttp.ClientSession(loop=loop) as session:
        for url in dl_list_url:
            await download_coroutine(session, url)


# --------------------------------------------------------------------------


async def download_coroutine(session, url):

    file = os.path.basename(url)
    local_file = Download_Folder + file

    async with async_timeout.timeout(120):
        async with session.get(url) as response:
            with open(local_file, "wb") as fd:
                async for data in response.content.iter_chunked(1024):
                    fd.write(data)

    # update the progress bar
    async_dl.count += 1
    download_photos.progress_bar["value"] = int(async_dl.count /
                                                async_dl.total * 100)
    window.update()  # force update
    # BUG - progress bar, no colour


# --------------------------------------------------------------------------


def position_window(win_ref):
    "position a window at the centre of the main application window"

    # handle the "x" button on the 'window'
    win_ref.protocol("WM_DELETE_WINDOW", win_ref.destroy)

    # obtain the application window's cooridinates (x & y)
    app_x = window.winfo_x()
    app_y = window.winfo_y()

    # remove the window
    # (reduce window flashing due to repositioning, most of the time)
    win_ref.withdraw()

    # retrive the window's width & height
    win_ref.update()  # force an update; to update the window's width & height
    win_width = win_ref.winfo_width()  # width of application window
    win_height = win_ref.winfo_height()  # height of application window

    # calculate the value of x & y, so the window will be in the centre of
    # the application window. app_width & app_height (are global)
    win_x = app_x + (app_width / 2) - (win_width / 2)
    win_y = app_y + (app_height / 2) - (win_height / 2)

    win_x += 22  # manual offset

    # position the window at the centre of the app
    win_ref.geometry("+%d+%d" % (win_x, win_y))  # position it!
    win_ref.deiconify()  # bring the window back
    win_ref.attributes("-topmost", 1)  # ensure window is at the top

    window.attributes("-disabled", 1)  # disabled the main window

    win_ref.update()  # force update


# --------------------------------------------------------------------------


def border_frame():
    "Create a frame with a border"

    # Setup the about window
    temp_win = tk.Toplevel()
    temp_win.resizable(False, False)
    temp_win.overrideredirect(True)

    # create a frame, with a background colour (via style)
    outer_frame = ttk.Frame(temp_win, style="outer.TFrame")
    outer_frame.grid(row=0, column=0)

    # create 2nd frame within the outer frame, smaller (due to padding)
    inner_frame = ttk.Frame(outer_frame, style="inner.TFrame")
    inner_frame.grid(row=0, column=0, padx=3, pady=3)
    # thus has a 3 pixel border

    return (temp_win, inner_frame)


# --------------------------------------------------------------------------


def mesg_box(msg_typ, mesg):
    """Display a message box
    msg_typ is question, warning, error or information (set the icon type)
    mesg is the message to display"""

    # create a window/frame with a border
    (mesgbox_win, frame) = border_frame()

    label0 = ttk.Label(frame,
                       image="::tk::icons::" + msg_typ,
                       style="msgbox.TLabel")
    label0.grid(row=0, column=0, sticky="nw", padx=10, pady=(10, 0))

    label1 = ttk.Label(frame, text=mesg, justify="left", style="msgbox.TLabel")
    label1.grid(row=0, column=1, padx=(0, 20), pady=(10, 0))

    ok_btn = ttk.Button(frame, text="OK", command=mesgbox_win.destroy)
    ok_btn.grid(row=1, column=1, padx=(0, 10), pady=10, sticky="e")

    # pop up the window
    position_window(mesgbox_win)
    mesgbox_win.wait_window()  # Wait for user to close the window
    window.attributes("-disabled", 0)  # Enable the main window


# --------------------------------------------------------------------------


def check_for_update():
    "Compare the application's version with github"

    url = GITHUB_URL + "/raw/master/version.txt"
    r = requests.get(url)

    if r.status_code == 200:
        (github_prog_ver, github_config_ver) = r.text.split(",")

        if github_prog_ver > VERSION:
            msg = "Version " + str(
                github_prog_ver
            ) + " available!\n\nDo update to the latest version."
        elif github_prog_ver < VERSION:
            msg = "You are running a higher version!!"
        else:
            msg = "Program is up to date"

        mesg_box("information", msg)
    else:
        msg = str(r.status_code) + " : " + r.reason
        mesg_box("error", msg)


# --------------------------------------------------------------------------


def about_window():
    "Display an about window"

    # create a window/frame with a border
    (about_win, frame) = border_frame()

    # ---

    logo_img = PhotoImage(data=LOGO_B64)
    label_logo = ttk.Label(frame, image=logo_img, style="msgbox.TLabel")
    label_logo.grid(row=0, column=0, sticky="nw")

    frame1 = ttk.Frame(frame, style="inner.TFrame")
    frame1.grid(row=0, column=1, padx=(0, 10), pady=(15, 5), sticky="n")

    # ---

    label00 = ttk.Label(frame1,
                        style="msgbox.TLabel",
                        text=PROGRAM_NAME,
                        anchor="center")
    label00.grid(row=0, column=0, columnspan=2, padx=10)
    label00.configure(font=("", 12, "bold"))

    # ---

    label10 = ttk.Label(frame1,
                        style="msgbox.TLabel",
                        justify="right",
                        text="Version:\nRelease Date:")
    label10.grid(row=1, column=0, sticky="nsew", padx=(20, 0))

    label11 = ttk.Label(frame1,
                        style="msgbox.TLabel",
                        justify="left",
                        text="%s\n%s" % (VERSION, RELEASE_DATE))
    label11.grid(row=1, column=1, sticky="nsew")

    # ---

    divider = ttk.Separator(frame1, orient="horizontal")
    divider.grid(row=2, column=0, columnspan=2, sticky="ew", pady=10, padx=10)

    # ---

    label20 = ttk.Label(frame1,
                        style="msgbox.TLabel",
                        anchor="w",
                        text="Your system information:")
    label20.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=10)

    # ---

    label30 = ttk.Label(frame1,
                        style="msgbox.TLabel",
                        justify="right",
                        text="Platform:\nPython:\ntkinter:")
    label30.grid(row=4, column=0, sticky="nsew", padx=(20, 0))

    label31 = ttk.Label(frame1,
                        style="msgbox.TLabel",
                        justify="left",
                        text="%s (%s)\n%s (%s)\n%s" %
                        (platform.platform(), platform.machine().lower(),
                         platform.python_version(), platform.python_build()[1],
                         window.tk.call("info", "patchlevel")))
    label31.grid(row=4, column=1, sticky="nsew")

    # ---

    ok_btn = ttk.Button(frame1, text="OK", command=about_win.destroy)
    ok_btn.grid(row=8, column=1, pady=(0, 5), sticky="e")

    # ---

    position_window(about_win)
    about_win.wait_window()  # wait for 'close' of window
    window.attributes("-disabled", 0)  # enable the main window


# --------------------------------------------------------------------------


def app_close():
    "Save configuration before application shutdown/close"

    config_json["iptc_tag"] = iptc_tag.get()
    config_json["mtime_tag"] = mtime_tag.get()
    config_json["photo_list_tag"] = photo_list_tag.get()

    # Save data/json to file
    text_file = open(CONFIG_FILE, "w")
    text_file.write(json.dumps(config_json, indent=4))
    text_file.close()

    window.destroy()  # close the application window


# --------------------------------------------------------------------------


def fixed_map(option):
    """Fixed treeview background's tag issue
    https://stackoverflow.com/questions/56329342/tkinter-treeview-background-tag-not-working

    Returns the style map for 'option' with any styles starting with
    ('!disabled', '!selected', ...) filtered out."

    style.map() returns an empty list for missing options, so this
    should be future-safe."""
    return [
        elm for elm in style.map("Treeview", query_opt=option)
        if elm[:2] != ("!disabled", "!selected")
    ]


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

# initialize the application, load in configuration
config_json = init_app()

# --------------------------------------------------------------------------
# application's window layout

window = tk.Tk()
window.title(PROGRAM_NAME)
window.resizable(False, False)
window.iconphoto(True, PhotoImage(data=LOGO_B64))
window.protocol("WM_DELETE_WINDOW", app_close)

# --------------------------------------------------------------------------

style = ttk.Style()
style.theme_use("clam")
style.map("Treeview",
          foreground=fixed_map("foreground"),
          background=fixed_map("background"))
style.configure("Treeview.Heading", font=("", 9, "bold"), background="bisque")

style.configure("outer.TFrame", background="sandy brown")
style.configure("inner.TFrame", background="alice blue")
style.configure("msgbox.TLabel", background="alice blue")

style.configure("TProgressbar", background="lawn green")

# --------------------------------------------------------------------------
# menu layout
menu = tk.Menu(window)

# file menu
file_item = tk.Menu(menu, tearoff=0)
file_item.add_command(label="Check for update", command=check_for_update)
file_item.add_separator()
file_item.add_command(label="Exit", command=app_close)
menu.add_cascade(label="File", menu=file_item)

# config menu
iptc_tag = tk.BooleanVar()
config_item = tk.Menu(menu, tearoff=0)
config_item.add_checkbutton(label="IPTC tag",
                            onvalue=1,
                            offvalue=0,
                            variable=iptc_tag,
                            state="disabled")
iptc_tag.set(config_json["iptc_tag"])

# photo list
photo_list_tag = tk.BooleanVar()
config_item.add_checkbutton(label="Generate photo list",
                            onvalue=1,
                            offvalue=0,
                            variable=photo_list_tag)
photo_list_tag.set(config_json["photo_list_tag"])

# modify file access time
mtime_tag = tk.BooleanVar()
config_item.add_checkbutton(label="Modify file access time",
                            onvalue=1,
                            offvalue=0,
                            variable=mtime_tag)
mtime_tag.set(config_json["mtime_tag"])
menu.add_cascade(label="Config", menu=config_item)

# help menu
help_item = tk.Menu(menu, tearoff=0)
help_item.add_command(label="Github",
                      command=lambda: webbrowser.open(GITHUB_URL, 1))
help_item.add_command(label="Meetup.com",
                      command=lambda: webbrowser.open(MEETUP_COM, 1))
help_item.add_command(
    label="Meetup API",
    command=lambda: webbrowser.open("https://www.meetup.com/meetup_api/", 1))
help_item.add_separator()
help_item.add_command(label="About", command=about_window)
menu.add_cascade(label="Help", menu=help_item)

# display current working directory
cwd = os.getcwd()
menu.add_cascade(label="[" + cwd + "]", command=lambda: os.startfile(cwd))

# configure it!
window.configure(menu=menu)

# --------------------------------------------------------------------------
# Define right click/pop up menu

# right click @ Group page
r_click_popup1 = tk.Menu(window, tearoff=0, fg="blue")
r_click_popup1.add_command(label="Group page",
                           command=lambda: webbrowser.open(R_Click_URL1, 1))

# right click @ Event page
r_click_popup2 = tk.Menu(window, tearoff=0, fg="blue")
r_click_popup2.add_command(label="Event page",
                           command=lambda: webbrowser.open(R_Click_URL1, 1))
r_click_popup2.add_command(label="Album Page",
                           command=lambda: webbrowser.open(R_Click_URL2, 1))

# right click @ Photo page
r_click_popup3 = tk.Menu(window, tearoff=0, fg="blue")
r_click_popup3.add_command(label="Photo page",
                           command=lambda: webbrowser.open(R_Click_URL1, 1))

# --------------------------------------------------------------------------
# Define Group frame

group_frame = ttk.Frame(window)
group_frame.grid(row=0, column=0, padx=(10, 5), pady=(5, 0), stick="nw")

# treeview
lb_header = ["g_index", "Group", "Country", "Members"]
group_tree = ttk.Treeview(group_frame,
                          columns=lb_header,
                          show="headings",
                          selectmode="browse",
                          height=6)
group_tree.heading("g_index", text="g_index")
group_tree.heading("Group",
                   text="Group",
                   anchor="w",
                   command=lambda _col="Group": treeview_sort_column(
                       group_tree, _col, True, 0))
group_tree.heading("Country",
                   text="Country",
                   anchor="w",
                   command=lambda _col="Country": treeview_sort_column(
                       group_tree, _col, False, 0))
group_tree.heading("Members",
                   text="Members",
                   command=lambda _col="Members": treeview_sort_column(
                       group_tree, _col, False, 1))

group_tree.column("Group", width=320, anchor="w")
group_tree.column("Country", width=140, anchor="w")
group_tree.column("Members", width=70, anchor="e")
group_tree["displaycolumns"] = ("Group", "Country", "Members")

group_tree.bind("<ButtonRelease-1>", group_clicked)  # left click
group_tree.bind("<ButtonRelease-3>", group_clicked)  # right click

group_tree.grid(row=0, column=0, columnspan=2)

# ---

# scrollbar
group_scroll = ttk.Scrollbar(group_frame,
                             orient="vertical",
                             command=group_tree.yview)
group_scroll.grid(row=0, column=2, rowspan=2, sticky="ns")
group_tree.config(yscrollcommand=group_scroll.set)

# ---

group_status = tk.StringVar()
group_frame_status = ttk.Label(group_frame,
                               textvariable=group_status,
                               anchor="w",
                               width=74)
group_frame_status.grid(row=1, column=0, sticky="nsew")

group_refresh_btn = ttk.Button(group_frame,
                               text="Refresh",
                               command=lambda: display_group_frame(1))
group_refresh_btn.grid(row=1, column=1, sticky="nse")

# --------------------------------------------------------------------------
# Define Event frame

event_frame = ttk.Frame(window)
event_frame.grid(row=1, column=0, padx=(10, 5), pady=(11, 10), stick="nw")

# ---

# treeview
lb_header = ["e_index", "e_id", "Date", "Event", "Photos"]
event_tree = ttk.Treeview(
    event_frame,
    columns=lb_header,
    show="headings",
    selectmode="browse",
    height=18,
)
event_tree.heading("e_index", text="e_index")
event_tree.heading("e_id", text="e_id")
event_tree.heading("Date",
                   text="Date",
                   anchor="w",
                   command=lambda _col="Date": treeview_sort_column(
                       event_tree, _col, True, 2))
event_tree.heading("Event",
                   text="Event",
                   anchor="w",
                   command=lambda _col="Event": treeview_sort_column(
                       event_tree, _col, False, 0))
event_tree.heading("Photos",
                   text="Photos",
                   command=lambda _col="Photos": treeview_sort_column(
                       event_tree, _col, True, 1))

event_tree.column("Date", width=80, anchor="center")
event_tree.column("Event", width=400, anchor="w")
event_tree.column("Photos", width=50, anchor="e")
event_tree["displaycolumns"] = ("Date", "Event", "Photos")

event_tree.tag_configure("no_photo",
                         background="lavender",
                         foreground="steel blue")

event_tree.bind("<ButtonRelease-1>", event_clicked)  # left click
event_tree.bind("<ButtonRelease-3>", event_clicked)  # right click

event_tree.grid(row=0, column=0, columnspan=4)

# ---

# scrollbar
event_scroll = ttk.Scrollbar(event_frame,
                             orient="vertical",
                             command=event_tree.yview)
event_scroll.grid(row=0, column=4, rowspan=2, sticky="ns")
event_tree.config(yscrollcommand=event_scroll.set)

# ---

event_status = tk.StringVar()
event_frame_status = ttk.Label(event_frame,
                               textvariable=event_status,
                               anchor="w",
                               width=45)
event_frame_status.grid(row=1, column=0, sticky="nsew")

event_checkbox = ttk.Checkbutton(event_frame,
                                 text="All Events",
                                 command=lambda: update_event_frame())
event_checkbox.state(["!alternate"])
event_checkbox.state(["disabled", "selected"])
event_checkbox.grid(row=1, column=1, sticky="nse")

var_year = tk.StringVar()
var_year.set("Recent")  # default value
option_year = ttk.OptionMenu(event_frame,
                             var_year,
                             "Recent",
                             command=year_clicked)
option_year.grid(row=1, column=2, sticky="nse")
option_year.state(["disabled"])

event_refresh_btn = ttk.Button(event_frame,
                               text="Refresh",
                               command=lambda: display_event_frame(1))
event_refresh_btn.grid(row=1, column=3, sticky="nse")
event_refresh_btn.state(["disabled"])

# --------------------------------------------------------------------------
# Define photo album frame

album_frame = ttk.Frame(window)
album_frame.grid(row=0,
                 column=1,
                 rowspan=3,
                 padx=(5, 10),
                 pady=(5, 10),
                 sticky="nw")

# ---

album_folder_btn = ttk.Button(
    album_frame,
    text="DL folder",
    command=lambda: os.startfile(os.path.realpath(Download_Folder)))
album_folder_btn.grid(row=0, column=0, sticky="nsew")
album_folder_btn.state(["disabled"])

album_none_btn = ttk.Button(album_frame,
                            text="Clear all",
                            command=lambda: album_select_all())
album_none_btn.grid(row=0, column=1, sticky="nsew")
album_none_btn.state(["disabled"])

album_all_btn = ttk.Button(album_frame,
                           text="Select all",
                           command=lambda: album_select_all(1))
album_all_btn.grid(row=0, column=2, sticky="nsew")
album_all_btn.state(["disabled"])

album_download_btn = ttk.Button(album_frame,
                                text="Download",
                                width=6,
                                command=album_download)
album_download_btn.grid(row=0, column=3, sticky="nsew")
album_download_btn.state(["disabled"])

# treeview
lb_header = ["No", "Photo", "Date", "Time", "Uploaded by"]
photo_tree = ttk.Treeview(
    album_frame,
    columns=lb_header,
    show="headings",
    selectmode="extended",
    height=26,
)
photo_tree.heading(
    "No",
    text="No",
    command=lambda _col="No": treeview_sort_column(photo_tree, _col, True, 1))
photo_tree.heading("Photo",
                   text="Photo",
                   command=lambda _col="Photo": treeview_sort_column(
                       photo_tree, _col, True, 0))
photo_tree.heading("Date", text="Date")
photo_tree.heading("Time", text="Time")
photo_tree.heading("Photo",
                   text="Photo",
                   command=lambda _col="Photo": treeview_sort_column(
                       photo_tree, _col, True, 0))
photo_tree.heading("Uploaded by",
                   text="Uploaded by",
                   command=lambda _col="Uploaded by": treeview_sort_column(
                       photo_tree, _col, True, 0))
photo_tree.heading("Uploaded by",
                   text="Uploaded by",
                   command=lambda _col="Uploaded by": treeview_sort_column(
                       photo_tree, _col, True, 0))

photo_tree.column("No", width=40, anchor="e")
photo_tree.column("Photo", width=160, anchor="center")
photo_tree.column("Date", width=90, anchor="center")
photo_tree.column("Time", width=90, anchor="center")
photo_tree.column("Uploaded by", width=100, anchor="center")

photo_tree.grid(row=1, column=0, columnspan=4)
photo_tree.bind("<ButtonRelease-1>", photo_clicked)  # left click
photo_tree.bind("<Double-Button-1>", photo_r_clicked)  # double left click
photo_tree.bind("<ButtonRelease-3>", photo_r_clicked)  # right click

photo_tree.tag_configure("no_dl", background="lavender", foreground="blue")

# ---

# scrollbar
photo_scroll = ttk.Scrollbar(album_frame,
                             orient="vertical",
                             command=photo_tree.yview)
photo_scroll.grid(row=1, column=4, rowspan=3, sticky="ns")
photo_tree.config(yscrollcommand=photo_scroll.set)

# ---

album_status = tk.StringVar()
album_frame_status = ttk.Label(album_frame,
                               textvariable=album_status,
                               width=52,
                               anchor="w")
album_frame_status.grid(row=2, column=0, columnspan=2, sticky="nsew")

album_checkbox = ttk.Checkbutton(album_frame,
                                 text="All Photos",
                                 command=lambda: update_album_frame())
album_checkbox.grid(row=2, column=2, sticky="nse")
album_checkbox.state(["!alternate"])
album_checkbox.state(["disabled", "selected"])

album_refresh_btn = ttk.Button(album_frame,
                               text="Refresh",
                               command=lambda: display_album_frame(1))
album_refresh_btn.grid(row=2, column=3, sticky="nse")
album_refresh_btn.state(["disabled"])

# --------------------------------------------------------------------------

# ---
# Display the application window (centre of the screen)

# obtain current window size, width and height
screen_width = window.winfo_screenwidth()  # width of the screen
screen_height = window.winfo_screenheight()  # height of the screen

# Remove the application window
# (reduce window flashing due to repositioning, most of the time)
window.withdraw()

# Obtain the application window size, width and height
window.update()  # force update; to update window w & h
app_width = window.winfo_width()  # width of application window
app_height = window.winfo_height()  # height of application window

# Calculate the value of x & y, so the window will be in the centre
app_x = (screen_width / 2) - (app_width / 2)  # calculate the x, y
app_y = (screen_height / 2) - (app_height / 2)

# Postion the application window at the middle of the screen
window.geometry("+%d+%d" % (app_x, app_y))  # position it!
window.deiconify()  # bring up the window

# --------------------------------------------------------------------------
# main()

# Retrieve the access token and assign it to http headers variable
headers = retrieve_token()

# Display an error message if there isn't a access token
if headers == "":
    mesg_box(
        "error",
        "Unable to retrieve access token.\n\nplease run 'tk-mpd-config.py'")
    window.destroy()
    sys.exit(1)  # exit!

# member_name = user_profile()
display_group_frame()

window.mainloop()
