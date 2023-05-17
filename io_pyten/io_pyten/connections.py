# Contains all basic functions and importas required by all classes and methods

# Import pytenable to be able to use our library
from tenable.io import TenableIO

###################### ADDITIONAL REQUIRED IMPORTS FOR CLASSES ################
import csv
import smtplib

def connect_io(*args):
    '''
    Creates a connection to Tenable.io using API keys. 
    
    Fisrt operation mode, no parameters
    
    The function will read the API keys from a file named IO_API_Keys.txt. 
    The file should have only two lines with the following order:

    1st Line: Access Key
    2nd Line: Secret Key

    Second operation mode, with parameters:
    The function can be used by providing the AK and SK directly to the
    funtion like this:

    connect_io(ACCESS_KEY, SECRET_KEY)

    The function will always print in screen the connection status

    '''

    # First Opetation mode, no parameters
    if len(args) == 0:
        with open("input_files/IO_API_Keys.txt") as file:
            api_keys = [line.rstrip() for line in file]
            access_key = api_keys[0]
            secret_key = api_keys[1]
        tio = TenableIO(access_key, secret_key)
        print(tio.server.status())
        return tio
    
    # Second operation mode, provide API keys as parameters
    # For first time usage
    elif len(args) == 2:
        tio = TenableIO(args[0], args[1])
        print(tio.server.status())

        with open('input_files/IO_API_Keys.txt', 'w') as file:
            
            file.write(args[0]+"\n")
            file.write(args[1]+"\n")

        return tio

    # Void if incorrect number of parameters provided
    else:
        return "Incorrect number of parameters"