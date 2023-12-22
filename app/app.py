"""
===============================================================================
ENGR 13000 Fall 2022

Program Description
    This Program acts as a reminders list, where I can send it reminders to add or delete from the digital list through text
     and then also ask through text what my reminders are. Additionally, at specific times during the day the program will text me the list of my current reminders. 

Assignment Information
    Assignment:     Proj4
    Author:         Josh Mansky, jmansky@purdue.edu
    Team ID:        Team 06
th
Contributor:    None
    My contributor(s) helped me:
    [ ] understand the assignment expectations without
        telling me how they will approach it.
    [ ] understand different ways to think about a solution
        without helping me plan my solution.
    [ ] think through the meaning of a specific error or
        bug present in my code without looking at my code.
    Note that if you helped somebody else with their code, you
    have to list that person as a contributor here as well.
    
ACADEMIC INTEGRITY STATEMENT
I have not used source code obtained from any other unauthorized
source, either modified or unmodified. Neither have I provided
access to my code to another. The project I am submitting
is my own original work.
===============================================================================
"""

# Importing files used to send and recieve sms messages
from flask import Flask, Response, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from messages import reminder_adder, reminder_deleter, reminders_message
from dotenv import load_dotenv
import pickle # Pickle is used to store data in between runs of the program in a pickle file, which makes the data/reminders list easier to retrieve and update than in a traditional .txt file

# Importing files to allow the reminders list to be sent to the user at certain times of day
from datetime import datetime
from multiprocessing import Process
from time import sleep
import os

# Initializing app to an instance of the flask class
app = Flask(__name__)

# Initializing reminder list and the file it is stored in
reminders_file = "reminders_file.pkl"

# Uncomment these lines only on the very first run of the program to create the pickle file in the projects folder
"""
# reminders = []
# with open(reminders_file, 'wb') as file:
#   pickle.dump(reminders, file)
"""

# Initializing the checks that confirm the user wants to add or delete a reminder
reminder_add_check = False
reminder_del_check = False


# Decorator that allows the output of the function to route to web interface linked to the digital twilio number
# Function takes in whatever the user sends as input and then outputs the appropriate response
@app.route("/sms", methods=['GET', 'POST']) 
def sms_reply(): 
    # Initializing global variables because since importing app.route decorator from flask, 
    # these variables cannot be inputted as parameters/arguments
    #global reminders
    global reminder_add_check
    global reminder_del_check

    
    body = request.values.get('Body').lower() # converts the body of the SMS to a string in all lowercase
    resp = MessagingResponse() # Sets resp equal to an instance of the MessageingResponse class so that it can be used to take in strings and convert them to the twilio's SMS format

    # Checks if the user texted add reminder
    if "add reminder" in body:
        response = reminder_adder() # sets response to the appropriate response SMS 
        resp.message(response) # Adds the response message to the return SMS
        message = reminders_message(load_list()) # Loads the current list from its pickle file 
        resp.message(message) # Adds the reminder list message to the return SMS 
        reminder_add_check = True # Tells program the user wants to add a reminder
        return Response(str(resp), mimetype="application/xml") # Returns the SMS message to be sent to the user 
    # Checks if the user texted add reminder
    elif "delete reminder" in body:
        response = reminder_deleter() # sets response to the appropriate response SMS
        resp.message(response) # Adds the response message to the return SMS
        message = reminders_message(load_list()) # Loads the current list from its pickle file
        resp.message(message) # Adds the reminder list message to the return SMS 
        reminder_del_check = True # Tells program that the user wants to delete a reminder
        return Response(str(resp), mimetype="application/xml") # Returns the SMS message to be sent to the user

    # Adds a reminder to the reminder list if the user has indicated they want to add one
    if reminder_add_check == True:
        reminders = load_list() # Sets reminders equal to the current version of the reminder list from the pickle file 
        # Error Checking: checks if the reminder the user wants to add is already in the list and sends an error message if it is
        if body in reminders:
            resp.message("This reminder is already in your reminder list, try writing it again.") # Adds error message to SMS response
            return Response(str(resp), mimetype="application/xml") # Returns SMS response
        reminders.append(body) # Adds the new reminder to the current reminders list
        save_list(reminders) # Saves the new reminders list to the pickle file
        resp.message("Reminder Added") # Adding confirmation message to the SMS response
        reminder_add_check = False # Resetting the reminder_add_check variable
        return Response(str(resp), mimetype="application/xml") # Returns the SMS response
    # Adds a reminder to the reminder list if the user has indicated they want to add one
    elif reminder_del_check == True:
        # Executes a try-except-else block to try deleteing the reminder from the list.
        try:
            reminders = load_list() # Loading the current reminders list from the pickle file
            reminders.remove(body) # Removing the specific reminder from the list
            save_list(reminders) # Saving the new reminders list to the pickle file
        # If the reminder is not in the list the remove function returns a ValueError, which the except block takes and returns an error message to user
        except ValueError:
            resp.message("This reminder is not in your Reminders, try writing it again.") # Adding the error message to the SMS repsonse
            return Response(str(resp), mimetype="application/xml") # Returning the SMS response to the user 
        else:
            resp.message("Reminder Deleted") # Adding deletion confirmation to SMS response
            reminder_del_check = False # Resetting the reminder_del_check variable
            return Response(str(resp), mimetype="application/xml") # Returning SMS response to the user

    # Outputs the current reminders list to the user if they ask "what are my reminders" in there SMS
    if "what are my reminders" in body:
        message = reminders_message(load_list()) # Loads current reminder list from the pickle file and formats reminder list
        resp.message(message) # Adds the reminder list message to the SMS response
        return Response(str(resp), mimetype="application/xml") # Returns the SMS response

    # Outputs default introduction if the user texts none of the above phrases to the twilio number
    resp.message("Hello, welcome to reminders!\n\nTo add a reminder type: add reminder\n\nTo delete a reminder type: delete reminder\n\nTo get a list of your reminders type: what are my reminders")   
    return Response(str(resp), mimetype="application/xml")

# Saves the inputted reminders list to the reminder list pickle file using the dunp function
def save_list(reminders):
    with open(reminders_file, 'wb') as file:
        pickle.dump(reminders, file)

# Loads the current reminders list from the reminder list pickle file and then outputs this list
def load_list():
    with open(reminders_file, 'rb') as file:
        reminders = pickle.load(file)
    return reminders

# Runs the send_sms function at the given times specified in the reminder_times list
def sender():
    reminder_times = [9, 12, 15, 18, 23] # Initializes reminder_times variable
    # Continously checks if the current time is equal a time in the reminder_times list, down to the second
    while True:
        for time in reminder_times:
            if datetime.now().hour == time:
                if datetime.now().minute == 54:
                    if datetime.now().second == 0:
                        send_sms() # Sends reminder list to user
                        sleep(2) # Ensures that the reminder list is only sent once

# Sends an SMS message to the user with a specified message
def send_sms():
    load_dotenv() # Loads the .env file with the Twilio account sid and auth token from the users Twilio account

    content = reminders_message(load_list()) # Assigns the content variable to the formatted version of the current reminders list

    account_sid = os.getenv("TWILLIO_ACCOUNT_SID") # Assigns the account_sid variable to the value of it from the .env file
    auth_token = os.getenv('TWILLIO_AUTH_TOKEN') # Assigns the auth_token viarable to the value of it from the .env file
    client = Client(account_sid, auth_token) # Assigns client to an instance of Twilio Client class, so that the message can be routed through the users Twilio account

    # Creating the message to be sent which numbers it should be sent from and to 
    message = client.messages \
        .create(
            body=content,
            from_="+19498284392", # Twilio number
            to='+16124178662' # Users number
        )


def main():
    process = Process(target = sender) # Creates a seperate process for the sender function so it can be run in parallel to the rest of the program
    process.daemon = True # Makes the process a daemon process so that it will end when the main program ends 
    process.start() # Starting the process
    app.run() # Runs the send_reply function so that it is constantly checking for input from the user, so it can output the appropriate output.

# Runs main() only if it is the main file
if __name__ == "__main__":
    main()