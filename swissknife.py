import glitter

def login():
    username = input("Please enter username: ")
    password = input("Please enter password: ")
    print("Logging in...")
    return glitter.login(username, password)

def main():
    print("Welcome to Glitter Swissknife!")
    while not login():
        None
    print("Logged in!")
    while True:
        print(
            "\nEnter Choice:\n1. Add likes\n2. Get user's id\n3. Get user's email\n4. Publish special colored glit\n5. Force request accept\n6. Reply private glit\n"
            "7. Update user name\n8. Create account with long name\n9. Get account's feed\n-----------\n"
            "Challenges:\n10. Login with only username\n11. Get user's password\n12. Get user's cookie\n13. Get user's search history\n")
        try:
            choice = int(input())
            if choice == 1:
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
                print(
                    "In order for this to succeed, you must first send a glance request to someone and know their id, or you can send to " + glitter.default_user_name)
                sender_id = input("Enter your account's id (if you don't know it use command number 2 ;)): ")
                target_id = input('Enter your target id (Or if you sent to the default account use ' + glitter.default_id + ')')
                accept_request(sender_id, target_id)
            elif choice == 6:
                print(
                    'This will send a reply to a glit in the account "SecretPrivateAccount" by ' + glitter.default_user_name + ','
                                                                                                                       'In order for you to see the result, you will have to be friends with SecretPrivateAccount,\nso use command number 6 with target id 54472.')
                opt = input("Do you want to continue? y for yes / anything else for no: \n")
                if opt == 'y':
                    message = input("Enter message")
                    comment(message)
            elif choice == 7:
                print("This option will change the username of " + default_user_name + ", so make sure you change"
                                                                                       "\nit back for future uses")
                new_user_name = input("Enter new long username: ")
                change_user_name(new_user_name)
            elif choice == 8:
                print(
                    "This option creates a user with a name longer than the restricted length in the app.\nBeware that every input has to be longer than 5 characters.\n")
                screen_name = input("Enter screen name: ")
                username = input("Enter account's username: ")
                password = input("Enter your password: ")
                create_account(screen_name, username, password)
            elif choice == 9:
                print(
                    "This option can show you the feed of a private account.\n(You can use 54472, the id of SecretPrivateAccount.)")
                account_id = input("Enter account ID: ")
                get_feed(account_id)
            elif choice == 10:
                username = input("Enter account's username (not full name):")
                glitter.login_no_pass(username)
                print("Logged in!")
            elif choice == 11:
                username = input("Enter account's username (not full name):")
                password = glitter.get_password(username)
                if password:
                    print(f"Password is: {password}")
            elif choice == 12:
                username = input("Enter account's username")
                cookie = glitter.get_cookie(username)
                if cookie:
                    print(f"Cookie is: {cookie}")
            elif choice == 13:
                username = input("Enter account's username: ")
                glitter.print_history(username)
            else:
                print("No such option..")
        except Exception as e:
            print(e)

if __name__ == '__main__':
    main()