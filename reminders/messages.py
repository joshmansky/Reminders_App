"""
===============================================================================
ENGR 13000 Fall 2022

Program Description
    This Program outputs the appropriate response messages when the user wants to add a reminder, delete a reminder, or see the current reminders list

Assignment Information
    Assignment:     Proj4
    Author:         Josh Mansky, jmansky@purdue.edu
    Team ID:        Team 06

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

# Asking the user what reminder they want to add to their reminder list
def reminder_adder():
    response = "What is the reminder you want to add?"
    return response

# Asking the user what reminder they want to delete from their reminder list
def reminder_deleter():
    response = "What is the reminder you want to delete?"
    return response

# Returning the users current list of reminders to them
def reminders_message(reminders):
    message = "The Current list of reminders:\n"
    for reminder in reminders:
        message = message + f" -{reminder}\n"
    return message