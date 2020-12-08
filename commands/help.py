import os
import sys
from rich.console import Console
from rich.table import Table

USER_PATHS = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../'))
sys.path.insert(0, USER_PATHS)
import utilities as utils

console = Console()

def print_table(table_info, heading):

    table_headings = ['Command type', 'Definition', 'Format', 'Optional format']
    table = Table(title=heading, show_header=True, header_style="bold green")
    for heading in table_headings:
        table.add_column(heading)
    for row in table_info:
        table.add_row(
            row[0],
            row[1],
            row[2],
            row[3]
        )
    console.print(table)


def print_support_commands_table(table_info, heading):
    table_headings = ['Command', 'Definition']
    table = Table(title=heading, show_header=True, header_style="bold green")
    for heading in table_headings:
        table.add_column(heading)
    for row in table_info:
        table.add_row(
            row[0],
            row[1],
        )
    console.print(table)


def print_help_functionality():
    table_info = []
    table_info.append(['Register user', 'Registers user with username and password', 'register <username> <password>', '-'])
    table_info.append(['Login user', 'User logs-in to computer system with username and password', 'login <username> <password>', '-'])
    table_info.append(['Create a volunteer slot', 'Create a 90 minute volunteer slot as a volunteer', '<username> volunteer create <date> <time>', '-'])
    table_info.append(['Cancel a volunteer slot', 'Cancel existing volunteer slots; only if patient has not booked any slot', '<username> volunteer cancel <date> <time>', '-'])
    table_info.append(['Book a slot', 'Book an open 30 minute volunteer slot as a patient', '<username> patient create <event ID>', '-'])
    table_info.append(['Cancel a booking', 'Cancel previous 30 minute booked slot as a patient', '<username> patient cancel <event ID>', '-'])
    table_info.append(['List booked slots', 'Print table with all booked slots', '<username> list-bookings', '<username> list-bookings <#days>'])
    table_info.append(['List open volunteer slots', 'Print table with all open volunteer slots for specified date', '<username> list-open <date>', '-'])
    table_info.append(['List slots open for booking', 'Print table with all open slots for booking', '<username> list-slots', '<username> list-slots <#days>'])
    print_table(table_info, 'Functionality:')
    print()


def print_user_type():
    table_info = []
    heading = 'User type:'
    table_info.append(['volunteer', 'User offering code clinic service'])
    table_info.append(['patient', 'User attending code clinic service'])
    print_support_commands_table(table_info, heading)
    print()


def print_commands_type(): 
    table_info = []
    heading = 'Commands:'
    table_info.append(['register', 'Registration functionality'])
    table_info.append(['login', 'Login functionality'])
    table_info.append(['create', 'Create volunteer or patient slot'])
    table_info.append(['cancel', 'Cancel volunteer or patient slot'])
    table_info.append(['list-slots', 'Print table with all open slots for booking'])
    table_info.append(['list-bookings', 'Print table with all open volunteer slots'])
    table_info.append(['list-open', 'Print table with all open volunteer slots for specified date'])
    print_support_commands_table(table_info, heading)
    print()


def print_support_type():
    table_info = []
    heading = 'Support:'
    table_info.append(['username', 'Name to uniquely identify student'])
    table_info.append(['password', 'String of 8 characters used for authenticating user'])
    table_info.append(['date', 'Date in format <yyyy-mm-dd>'])
    table_info.append(['time', 'Time the slot starts in format <hh:mm>'])
    table_info.append(['#days', 'Specify amount of days the listing lists'])
    print_support_commands_table(table_info, heading)
    print()


def print_help_command():
    print_help_functionality()
    print_user_type()
    print_commands_type()
    print_support_type()