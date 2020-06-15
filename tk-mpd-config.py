import tkinter as tk
import tkinter.ttk as ttk
from tkinter import font

import requests
import webbrowser
from urllib.parse import urlparse

#-------------------------------------------------------------------------
#global variables
version = '1.01'
release_date = '16-Jun-2020'
github_url = 'https://github.com/fishcode16/python-tk-meetup-photos-downloader/blob/master/HOWTO-CONFIG.md'
auth_url = ''

#-------------------------------------------------------------------------

def create_url():
    "check inputs and generate Authorization URL"

    global auth_url
    
    #retrieve data from input box
    key =  key2_1.get().strip(' ')
    secret = secret3_1.get().strip(' ')
    redirect_uri = redirect_uri4_1.get().strip(' ')

    clear_status()
   
    e_msg = []
    
    #key and secrect should be 26 characters
    if len(key) != 26: 
        e_msg.append('Invalid Key (should be 26 characters)')

    if len(secret) != 26:
        e_msg.append('Invalid Secret (should be 26 characters)')

    #validate the URL
    if redirect_uri == '':
        e_msg.append('Missing URI')
        
    else:
        parsed_url = urlparse(redirect_uri)
        scheme = parsed_url.scheme
        hostname = parsed_url.hostname

        if (scheme != 'https' and scheme != 'http'): # or not(hostname):
            e_msg.append('Invalid URI (should be http or https)')


    msgbox1['state'] = 'normal'

    #seems valid, generate a URL
    if len(e_msg) == 0:
        auth_url = 'https://secure.meetup.com/oauth2/authorize' + \
            '?client_id=' + str(key) + \
            '&response_type=code' + \
            '&redirect_uri=' + str(redirect_uri) + \
            '&set_mobile=on'
       
        #copy the URL to clipboard
        window.clipboard_clear()
        window.clipboard_append(auth_url)

        msgbox1.insert('end', auth_url)
       
        enable_step2()

    else:
        for x in e_msg:
            msgbox1.insert('end', x + '\n', 'err')

    msgbox1['state'] = 'disabled'

    return
    
#-------------------------------------------------------------------------

def enable_step1():
    'enable step1 buttons/input, disable step2 buttons/input'

    key2_1['state'] = 'normal'
    secret3_1['state'] = 'normal'
    redirect_uri4_1['state'] = 'normal'
    btn1['state'] = 'normal'
    btn4['state'] = 'disabled'

    code2_1['state'] = 'disabled'
    msgbox1['state'] = 'disabled'
    btn2['state'] = 'disabled'

    return

#-------------------------------------------------------------------------

def enable_step2():
    'enable step2 buttons/input, disable step1 buttons/input'
    
    key2_1['state'] = 'disabled'
    secret3_1['state'] = 'disabled'
    redirect_uri4_1['state'] = 'disabled'
    btn1['state'] = 'disabled'
    btn4['state'] = 'normal'

    code2_1['state'] = 'normal'
    msgbox1['state'] = 'normal'
    btn2['state'] = 'normal'
        
    return

#-------------------------------------------------------------------------

def clear_entry():
    'clear the content of the entry widget and text box'

    enable_step2()
    code2_1.delete(0, 'end')
    
    enable_step1()
    key2_1.delete(0, 'end')
    secret3_1.delete(0, 'end')
    redirect_uri4_1.delete(0, 'end')

    clear_status()
    
    return

#-------------------------------------------------------------------------

def clear_status():
    
    msgbox1['state'] = 'normal'
    msgbox1.delete('1.0', 'end')
    msgbox1['state'] = 'disabled'

    window.clipboard_clear()

    clear_status2()
    
    return

#-------------------------------------------------------------------------

def clear_status2():

    msgbox2['state'] = 'normal'
    msgbox2.delete('1.0', 'end')
    msgbox2['state'] = 'disabled'
    
    return

#-------------------------------------------------------------------------

def retreive_token_from_meetup():
    "retreive access token from meetup"

    clear_status2()

    msgbox2['state'] = 'normal'

    code = code2_1.get()
    if len(code) != 32: 
        msgbox2.insert('end', 'Invalid code (should be 32 characters)', 'err')

    else:
        #retrieve data from input box
        key =  key2_1.get().strip(' ')
        secret = secret3_1.get().strip(' ')
        redirect_uri = redirect_uri4_1.get().strip(' ')

        meetup_url = 'https://secure.meetup.com/oauth2/access'
        data = {
            'client_id' : key,
            'client_secret' : secret,
            'grant_type' : 'authorization_code',
            'redirect_uri' : redirect_uri,
            'code' : code
            }
        r = requests.post(url=meetup_url, data=data)

        msgbox2.insert('end', r.text)
    
        #write json to file
        text_file = open('access.json', 'w')
        text_file.write(r.text)
        text_file.close()
        
    msgbox2['state'] = 'disabled'

    return



#---------------------------------------------------------------------------
#window layout

window = tk.Tk()
window.title('Authorization Setup')
window.resizable(False, False)

#---------------------------------------------------------------------------
#window menu

menu = tk.Menu(window)

file_item = tk.Menu(menu, tearoff=0)
file_item.add_command(label='Exit', command=lambda: window.destroy())
menu.add_cascade(label='File', menu=file_item)
menu.add_command(label='Help', command=lambda: webbrowser.open(github_url, 1))

window.config(menu=menu)

#---------------------------------------------------------------------------

frame0 = ttk.Frame(window)
frame0.grid(row=0, column=0, padx=10, pady=5)

#---

y=0
label1 = ttk.Label(frame0, wraplength=360, justify='left', foreground='red', text=\
'**FYI** Information entered on this screen will be use to generate an Authorization\'s \
request URL and Access Token\'s request URL. The \'Access token\' will be saved on the \
system. All other information are discarded. Please refer to Meetup API website for information.')
label1.grid(row=y, column=0, columnspan=2, sticky='nsew')

y += 1
info_url2 = 'https://www.meetup.com/meetup_api/auth/#oauth2server'
label2 = ttk.Label(frame0, text=info_url2, cursor='hand2', foreground='blue', anchor='center')
label2.grid(row=y, column=0, columnspan=2, sticky='nsew')
label2.bind('<Button-1>', lambda e: webbrowser.open(info_url2, 1))

y += 1
div1 = ttk.Separator(frame0, orient='horizontal')
div1.grid(row=y, column=0, columnspan=2, sticky='ew', pady=3)

#---

y += 1
label3 = ttk.Label(frame0, anchor='w', wraplength=360, text='Your can obtain your Meetup OAuth information at this URL:')
label3.grid(row=y, column=0, columnspan=2, sticky='nsew')

y += 1
info_url1 = 'https://secure.meetup.com/meetup_api/oauth_consumers/'
label4 = ttk.Label(frame0, text=info_url1, cursor='hand2', foreground='blue', anchor='center')
label4.grid(row=y, column=0, columnspan=2, sticky='nsew')
label4.bind('<Button-1>', lambda e: webbrowser.open(info_url1, 1))

y += 1
div2 = ttk.Separator(frame0, orient='horizontal')
div2.grid(row=y, column=0, columnspan=2, sticky='ew', pady=3)

#---

y += 1
step1 = ttk.Label(frame0, text='Step 1: Create Authorization URL', anchor='w')
step1.grid(row=y, column=0, columnspan=2, sticky='ew', pady=5)
step1.config(font=('',12,'bold'))

y += 1
key2_0 = ttk.Label(frame0, text='Key: ', anchor='e')
key2_0.grid(row=y, column=0, sticky='ew', pady=5)
key2_1 = ttk.Entry(frame0)
key2_1.grid(row=y, column=1, sticky='ew')

y += 1
secret3_0 = ttk.Label(frame0, text='Secret: ', anchor='e')
secret3_0.grid(row=y, column=0, sticky='ew', pady=5)
secret3_1 = ttk.Entry(frame0)
secret3_1.grid(row=y, column=1, sticky='ew')

y += 1
redirect_uri4_0 = ttk.Label(frame0, text='Redirect URI: ', anchor='e')
redirect_uri4_0.grid(row=y, column=0, sticky='ew', pady=5)
redirect_uri4_1 = ttk.Entry(frame0)
redirect_uri4_1.grid(row=y, column=1, sticky='ew')

#---

y += 1
btn1 = ttk.Button(frame0, text='Create Authorization URL', command=create_url)
btn1.grid(row=y, column=0, sticky='nsew', pady=10)

btn4 = ttk.Button(frame0, text='Open URL', command=lambda: webbrowser.open(auth_url, 1))
btn4.grid(row=y, column=1, sticky='nsew', pady=10)
btn4['state'] = 'disabled'

y += 1
msgbox1 = tk.Text(frame0, foreground='blue', background='lightgrey', state='disabled', height=4, width=10)
msgbox1.grid(row=y, column=0, columnspan=3, sticky='nsew')
msgbox1.tag_config('err', foreground='red')

#---

y += 1
div3 = ttk.Separator(frame0, orient='horizontal')
div3.grid(row=y, column=0, columnspan=2, sticky='ew', pady=3)

y += 1
step2 = ttk.Label(frame0, text='Step 2: Request for Access Token', anchor='w')
step2.grid(row=y, column=0, columnspan=2, sticky='ew', pady=5)
step2.config(font=('',12,'bold'))

y += 1
code2_0 = ttk.Label(frame0, text='Code: ', anchor='e')
code2_0.grid(row=y, column=0, sticky='ew', pady=5)
code2_1 = ttk.Entry(frame0)
code2_1.grid(row=y, column=1, sticky='ew')
code2_1['state'] = 'disabled'

y += 1
btn2 = ttk.Button(frame0, text='Request for Access Token', command=retreive_token_from_meetup)
btn2.grid(row=y, column=0, columnspan=2, sticky='nsew', pady=10)
btn2['state'] = 'disabled'

y += 1
msgbox2 = tk.Text(frame0, foreground='blue', background='lightgrey', state='disabled', height=4, width=10)
msgbox2.grid(row=y, column=0, columnspan=3, sticky='nsew')
msgbox2.tag_config('err', foreground='red')

#---

y += 1
div4 = ttk.Separator(frame0, orient='horizontal')
div4.grid(row=y, column=0, columnspan=2, sticky='ew', pady=3)

y += 1
btn3 = ttk.Button(frame0, text='Clear all / Restart', command=clear_entry)
btn3.grid(row=y, column=0, columnspan=2, sticky='nsew', pady=10)


#---------------------------------------------------------------------------

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


#-------------------------------------------------------------------------
#main


window.mainloop()


