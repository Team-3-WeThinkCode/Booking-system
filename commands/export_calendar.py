import webbrowser

def export_calendar():
    '''
    Exports Code Clinic calendar in iCal format and allows for import into
    desktop calendar.
    '''
    
    link = 'https://calendar.google.com/calendar/ical/code.'\
    +'clinic.test%40gmail.com/private-1b7243fed80557dcf7f6b3d758948d30/'\
    +'basic.ics'
    webbrowser.open_new_tab(link)