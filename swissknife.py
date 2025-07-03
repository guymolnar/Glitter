import glitter

def login():
    username = input("Please enter username: ")
    password = input("Please enter password: ")
    print("Logging in...")
    return glitter.login(username, password)

def main():
    print("Welcome to Glitter Swissknife!")
    while not login(): #This loop will continue until theres a valid login
        None
    print("Logged in!")
    try:
        while True:
            print(
                "\nEnter Choice:\n0. Exit\n1. Add likes\n2. Get user's id\n3. Get user's email\n4. Publish special colored glit\n5. Force request accept\n6. Force request reject\n"
                "7. Reply private glit\n" "8. Update user name\n9. Create account with long name\n10. Get account's feed\n11. Show current account stats\n-----------\n"
                "Challenges:\n12. Login with only username\n13. Get user's password\n14. Get user's cookie\n15. Get user's search history\n"
                "16. Post malicious xss post\n")
            try:
                choice = int(input())
                if choice == 0:
                    print("Logging out...")
                    glitter.logout()
                    break
                elif choice == 1:
                    glitter.like_post()
                    print("Like added! check out DummyTestPage's 'LIKES GLIT' post for the result.\n")
                elif choice == 2:
                    name = input("Enter target user:")
                    id = glitter.get_id(name)
                    if id is None:
                        print("User not found!")
                    else:
                        print(f"ID is: {id}")
                elif choice == 3:
                    name = input("Enter target user:")
                    email = glitter.get_email(name)
                    if email is None:
                        print("User not found!")
                    else:
                        print(f"Email is: {email}")
                elif choice == 4:
                    message = input("Enter message:")
                    box_color = input("Enter special color: (Blue, Black, Grey...)")
                    font_color = input("Enter font color: (Blue, Black, Grey...)")
                    glitter.special_color_post(message, box_color, font_color)
                elif choice == 5:
                    print("In order for this to succeed, you must first send a glance request to someone")
                    sender_id = glitter.default_id
                    target_name = input('Enter your target name: ')
                    target_id = glitter.get_id(target_name)
                    if target_id:
                        glitter.accept_request(sender_id, target_id)
                    else:
                        print("Wrong username, maybe try full name?")
                elif choice == 6:
                    sender_id = glitter.get_id(input('Enter your sender name: '))
                    target_id = glitter.get_id(input('Enter target name: '))
                    if target_id and sender_id:
                        glitter.reject_request(sender_id, target_id)
                    else:
                        print("Wrong username, maybe try full name?")
                elif choice == 7:
                    print(
                        'This will send a reply to a glit in the account "SecretPrivateAccount" by ' + glitter.default_user_name + ','
                        'In order for you to see the result, you will have to be friends with SecretPrivateAccount,\nso use command number 6.')
                    opt = input("Do you want to continue? y for yes / anything else for no: \n")
                    if opt == 'y':
                        message = input("Enter message")
                        glitter.comment(message)
                elif choice == 8:
                    print("This option will change the username of " + glitter.default_user_name + ", so make sure you change"
                                                                                           "\nit back for future uses")
                    new_user_name = input("Enter new long username: ")
                    glitter.change_user_name(new_user_name)
                elif choice == 9:
                    print(
                        "This option creates a user with a name longer than the restricted length in the app.\nBeware that every input has to be longer than 5 characters.\n")
                    screen_name = input("Enter screen name: ")
                    username = input("Enter account's username: ")
                    password = input("Enter your password: ")
                    glitter.create_account(screen_name, username, password)
                elif choice == 10:
                    print("This option can show you the feed of a private account.\n(try SecretPrivateAccount.)")
                    account_id = input("Enter account name: ")
                    glitter.get_feed(account_id)
                elif choice == 11:
                    print("This option is mainly used for debugging for option #12 but still cool.\n")
                    print(f"Account ID:           {glitter.default_id}")
                    print(f"Username:             {glitter.default_user_name}")
                    print(f"Password:             {glitter.default_password}")
                    print(f"Email:                {glitter.default_email}")
                    print(f"Profile Image:        {glitter.default_img}")
                    print(f"Privacy Setting:      {glitter.default_privacy}")
                    print(f"Description:          {glitter.default_description}")
                    print(f"Gender:               {glitter.default_gender}")
                elif choice == 12:
                    username = input("Enter account's username (not full name):")
                    if glitter.login_no_pass(username):
                        print("Logged in!")
                elif choice == 13:
                    username = input("Enter account's username (not full name):")
                    password = glitter.get_password(username)
                    if password:
                        print(f"Password is: {password}")
                elif choice == 14:
                    print("Disclamer: This only works on accounts that you are not currently friends with / have an ongoing friend request.\n")
                    username = input("Enter account's username")
                    cookie = glitter.get_cookie(username)
                    if cookie:
                        print(f"Cookie is: {cookie}")
                elif choice == 15:
                    username = input("Enter account's username: ")
                    glitter.print_history(username)
                elif choice == 16:
                    print("This option will post a glit in your account with a link asking for donations, and when clicked it will post a glit in the victim's account with a message of your choice.")
                    message = input("Enter victim's glit content: (Hacked!, Your account is mine now! etc...)")
                    glitter.xss(message)
                else:
                    print("No such option..")
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
        glitter.logout()

if __name__ == '__main__':
    main()