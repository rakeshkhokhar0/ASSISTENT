"""
start app
checks if user onboarding is needed or not
Load today's plan
Listen command from telegram/WebUI
Decide which function call is needed
"""

from appdatabase import database as db
from command import parse_command
from taskmanager import handle_command

def main():
    #create tables when user is onboarding
    db.create_tables()


    while True:
        user_text = input("> ")

        command, payload = parse_command(user_text)

        status, message = handle_command(command, payload)

        print(message)




if __name__ == "__main__":
    main()
