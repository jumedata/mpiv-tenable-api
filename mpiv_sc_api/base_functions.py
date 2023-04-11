# Contains all basic functions and imports required by all classes and methods

###################### ADDITIONAL REQUIRED IMPORTS FOR CLASSES ################
import requests
import csv

def read_con_data(file = "SC_API_Keys.txt"):

    '''
    Gets connection data from a file. The file should have three lines:

    1. Hostname/IP URL to connect to Tenable.sc
    2. API Access Key
    3. API Secret Key
    
    
    This functions Returns a list with the hostname and a dictionary with 
    the AK and SK ready to be used in  the HTTP methods (get, post, patch)
    '''

    with open("SC_API_Keys.txt") as file:
        connection_details = [line.rstrip() for line in file]
        host = connection_details[0]
        AK = connection_details[1]
        SK = connection_details[2]
    
    headers = {'x-apikey':'accesskey='+AK+'; secretkey='+SK}

    return [host, headers]

def get_sc(resource = 'currentUser'):

    '''
    Uses a HTTP GET method to retrive info from Tenable.sc. If no
    resource specified, it will get data from the current user.
    '''

    data = read_con_data()
    host = data[0]
    headers = data[1]

    response = requests.get('https://'+host+'/rest/'+resource, headers = headers, verify = False)
    
    return response
   
def post_sc(resource, payload):

    '''
    Uses a HTTP POST method to add elements to Tenable.sc, requires the
    resource which is the Tenable.sc section to use and the data that 
    will be sent. Data must be a python dictionary.
    '''

    data = read_con_data()
    host = data[0]
    headers = data[1]
    headers["Accept"] = 'application/json'


    response = requests.post('https://'+host+'/rest/'+resource, json=payload, headers=headers, verify=False)
    
    return response

def patch_sc(resource, payload):

    '''
    Uses a HTTP POST method to add elements to Tenable.sc, requires the
    resource which is the Tenable.sc section to use and the data that 
    will be sent. Data must be a python dictionary.
    '''

    data = read_con_data()
    host = data[0]
    headers = data[1]
    headers["Accept"] = 'application/json'

    response = requests.patch('https://'+host+'/rest/'+resource, json=payload, headers=headers, verify=False)
    
    return response

def dict_to_csv(dict_data, filename):

    '''
    Converts a python dictionary into a csv file
    '''


    headers = dict_data[0].keys()
    
    with open(filename+'.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(dict_data)

    return "CSV File Generated"
