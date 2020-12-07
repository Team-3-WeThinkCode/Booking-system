from utilities import print_output

try:
    import rich
except ModuleNotFoundError:
    print_output('ERROR: Use the following command to install supporting libraries:')
    print('pip3 install rich\n')