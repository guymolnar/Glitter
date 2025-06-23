# glitter.py
from datetime import datetime, timezone
import socket
import requests

# Constants
GLITTER_IP = "44.224.228.136"
GLITTER_PORT_APP = 1336
GLITTER_PORT_WEB = 80

PRIVATE_GLIT_ID = "95440"
LIKE_GLIT_ID = "79822"

PASSWORD_RECOVERY_CODE_REQUEST_URL = "http://glitter.org.il/password-recovery-code-request/"
PASSWORD_RECOVERY_URL = "http://glitter.org.il/password-recovery-code-verification/"
HISTORY_URL = "http://glitter.org.il/history/"
HEADER = {"Content-Type":"application/json"}

# Globals
sock = None
default_user_name = None
default_password = None
default_id = None

def create_sock():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (GLITTER_IP, GLITTER_PORT_APP)
    sock.connect(server_address)
    return sock

def login(username, password):
    global sock, default_user_name, default_password, default_id
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
        return True
    else:
        print("Login failed")
        return False

def logout():
    global sock, default_id
    sock.sendall(('200#{gli&&er}' + default_id + '##').encode())
    sock.close()

def calculate_checksum(string):
    return sum(ord(char) for char in string)

def extract_field(server_msg, field):
    field_index = server_msg.find(field)
    start = field_index + len(field)
    end = start
    while server_msg[end] not in ('"', ',', '{'):
        end += 1
    return server_msg[start:end]

def like_post():
    sock.sendall(('710#{gli&&er}{"glit_id":' + LIKE_GLIT_ID + ',"user_id":' + default_id + ',"user_screen_name":"","id":-1}##').encode())
    print(sock.recv(1024).decode())

def get_id(name):
    sock.sendall(('300#{gli&&er}{"search_type":"SIMPLE","search_entry":"' + str(name) + '"}##').encode())
    server_msg = sock.recv(1024).decode()
    if "id" not in server_msg:
        return None
    return extract_field(server_msg, '"id":')

def get_email(name):
    sock.sendall(('300#{gli&&er}{"search_type":"SIMPLE","search_entry":"' + str(name) + '"}##').encode())
    server_msg = sock.recv(1024).decode()
    if "mail" not in server_msg:
        return None
    return extract_field(server_msg, '"mail":"')

def login_no_pass(name):
    global sock, default_user_name, default_password, default_id
    temp_sock = create_sock()
    try:
        temp_sock.sendall(('100#{gli&&er}{"user_name":"' + name + '","password":"X","enable_push_notifications":true}##').encode())
        server_msg = temp_sock.recv(1024).decode()
        if "User doesn't exist" in server_msg:
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
        sock = temp_sock

        default_password = extract_field(server_msg, '"password":"')
        default_user_name = name
        default_id = extract_field(server_msg, '"id":')
    except Exception as e:
        temp_sock.close()
        return None

def special_color_post(message, box_color, font_color):
    date = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    sock.sendall(('550#{gli&&er}{"feed_owner_id":' + default_id + ',"publisher_id":' + default_id + ',"publisher_screen_name":"","publisher_avatar":"im5","background_color":"' + box_color + '","date":"' + date + '","content":"' + str(message) + '","font_color":"' + font_color + '","id":-1}##').encode())
    print(sock.recv(1024).decode())

def comment(message):
    date = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    sock.sendall(('650#{gli&&er}{"glit_id":' + PRIVATE_GLIT_ID + ',"user_id":' + default_id + ',"user_screen_name":"' + default_user_name + '","id":-1,"content":"' + message + '","date":"' + date + '"}##').encode())
    print(sock.recv(1024).decode())

def accept_request(sender_id, target_id):
    #Functions accepts a friend request between 2 user ids
    sock.sendall(('420#{gli&&er}[' + sender_id + ',' + target_id + ']##').encode())
    print(sock.recv(1024).decode())


def change_user_name(new_name):
    sock.sendall(('350#{gli&&er}{"screen_name":"' + new_name + '","avatar":"im8","description":"ds","privacy":"Public","id":' + default_id + ',"user_name":"' + default_user_name + '","password":"' + default_password + '","gender":"Male","mail":"guy@gmail.com"}##').encode())
    print(sock.recv(1024).decode())

def create_account(screen_name, username, password):
    s = create_sock()
    s.sendall(('150#{gli&&er}{"registration_code":"12345","user":{"screen_name":"' + screen_name + '","avatar":"im1","description":"dsa","privacy":"Public","id":-1,"user_name":"' + username + '!","password":"' + password + '","gender":"Male","mail":"1234@dsddad.cds"}}##').encode())
    print(s.recv(1024).decode())
    s.close()

def get_feed(user_id):
    sock.sendall(('500#{gli&&er}{"feed_owner_id":' + user_id + ',"end_date":"2025-06-19T16:58:48.112Z","glit_count":5}##').encode())
    response = sock.recv(32768).decode()
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

def get_password(name):

    response = requests.post(PASSWORD_RECOVERY_CODE_REQUEST_URL, data=str('"' + name + '"'), headers=HEADER)
    if "Password Recovery Error" in response.text:
        print("Password Recovery Error")
        return None
    id = get_id(name)
    id_str = digits_to_letters(id)
    day_str = datetime.now().strftime("%d%m")
    time_str = datetime.now().strftime("%H%M")
    final_string = day_str + id_str + time_str
    response = requests.post(PASSWORD_RECOVERY_URL, json=[name, final_string], headers=HEADER)
    return response.text

def digits_to_letters(num):
    num_str = str(num)
    result = ''
    for digit in num_str:
        result += chr(ord('A') + int(digit))
    return result

def get_cookie(username):
    target_id = get_id(username)
    if target_id == None:
        print("Wrong username, maybe try full name?")
        return None
    msg = '''410#{gli&&er}[''' + default_id + ''',''' + target_id + ''']##'''
    sock.sendall(msg.encode())
    ans = sock.recv(1024).decode()
    cookie = extract_field(ans, 'session: ')
    return cookie

def print_history(username):
    user_id = get_id(username)
    if user_id == None:
        print("Wrong username, maybe try full name?")
        return None
    response = requests.get(HISTORY_URL + user_id, headers=HEADER)
    history = response.json() #If we do response.text were getting the list as a string so we wont be able to access actual data inside it
    print(username + " searched:")
    for user in history:
        print(user["screen_name"])