from rich.console import Console
from rich.table import Table


console = Console()


def print_table(table_info, heading):
    '''
    Prints table with information from the table_info list and heading string
    as the table heading

            Parameters:
                    table_info  (2D-list): List of information per table row
                    heading         (str): Heading to be printed above table
    '''

    table_headings = ['Command type', 'Definition', 'Format',
                                            'Optional format']
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
    '''
    Prints table with information from the table_info list and heading string
    as the table heading.

            Parameters:
                    table_info  (2D-list): List of information per table row
                    heading         (str): Heading to be printed above table
    '''

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
    '''
    Information on commands added to table_info list and printed to the 
    terminal in a table format
    '''

    table_info = []
    table_info.append(['Register user', 
               'Registers user with username and password\n',
               'register <username> <password>',
               '-'])
    table_info.append(['Login user', 
               'User logs-in to computer system with username and password\n',
               'login <username> <password>',
               '-'])
    table_info.append(['Create a volunteer slot',
               'Create a 90 minute volunteer slot as a volunteer\n',
               '<username> volunteer create <date> <time>',
               '-'])
    table_info.append(['Cancel a volunteer slot',
               'Cancel existing volunteer slots; only if patient has'\
               +' not booked any slot\n',
               '<username> volunteer cancel <date> <time>',
               '-'])
    table_info.append(['Book a slot',
               'Book an open 30 minute volunteer slot as a patient\n',
               '<username> patient create <event ID> <description>',
               '-'])
    table_info.append(['Cancel a booking',
               'Cancel previous 30 minute booked slot as a patient\n',
               '<username> patient cancel <event ID>',
               '-'])
    table_info.append(['List booked slots',
               'Print table with all booked slots\n',
               '<username> list-bookings', '<username> list-bookings <#days>'])
    table_info.append(['List open volunteer slots',
               'Print table with all open volunteer slots for specified date\n',
               '<username> list-open <date>', '-'])
    table_info.append(['List slots open for booking',
               'Print table with all open slots for booking\n',
               '<username> list-slots', '<username> list-slots <#days>'])
    table_info.append(['List format information',
               'Describes each command\n', 
               '<username> help format', 
               '<username> -h format'])
    table_info.append(['Export Code Clinic calendar',
               'Exports the calendar as an iCal file, allows import to '\
               +'desktop calendar app.\n', 
               '<username> export',
               '-'])
    print_table(table_info, 'Functionality:')
    print()


def print_user_type():
    '''
    Information on user type added to table_info list and printed to the
    terminal in a table format.
    '''

    table_info = []
    heading = 'User type:'
    table_info.append(['volunteer', 'User offering code clinic service'])
    table_info.append(['patient', 'User attending code clinic service'])
    print_support_commands_table(table_info, heading)
    print()


def print_commands_type(): 
    '''
    Information on command types added to table_info list and printed to the 
    terminal in a table format
    '''

    table_info = []
    heading = 'Commands:'
    table_info.append(['register', 
                       'Registration functionality'])
    table_info.append(['login', 
                       'Login functionality'])
    table_info.append(['create', 
                       'Create volunteer or patient slot'])
    table_info.append(['cancel', 
                       'Cancel volunteer or patient slot'])
    table_info.append(['list-slots', 
                       'Print table with all open slots for booking'])
    table_info.append(['list-bookings', 
                       'Print table with all open volunteer slots'])
    table_info.append(['list-open',
                       'Print table with all open volunteer slots'\
                       +' for specified date'])
    print_support_commands_table(table_info, heading)
    print()


def print_support_type():
    '''
    Information on support arguments added to table_info list and printed to
    the terminal in a table format.
    '''

    table_info = []
    heading = 'Support:'
    table_info.append(['username',
                       'Name to uniquely identify student'])
    table_info.append(['password', 
                       'String of 8 characters used for authenticating user'])
    table_info.append(['date', 
                       'Date in format <yyyy-mm-dd>'])
    table_info.append(['time', 
                       'Time the slot starts in format <hh:mm>'])
    table_info.append(['description',
                       'Topic to be discussed (entered in enclosed quotation marks)'])
    table_info.append(['#days', 'Specify amount of days the listing lists'])
    print_support_commands_table(table_info, heading)
    print()


def print_help_format_command():
    '''
    Format information printed to the terminal in table format.
    '''
    
    print_user_type()
    print_commands_type()
    print_support_type()