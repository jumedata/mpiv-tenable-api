# Use Tenable SC through Tenable.sc API
# By: MPIV Partners
# v1.0 - Feb 12th, 2023
#### NOTES #######################################
# Added docstring comments and edit function
#
#################IMPROVEMENTS#####################
#
#


import requests

def read_con_data(file = "SC_API_Keys.txt"):

    '''
    Gets connection data from a file. Returns a list with the hostname
    and a dictionary with the AK and SK ready to be use on HTTP methods
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
    

def show_asset_lists(mode='silent'):
    
    '''
    In all cases the functions returns a list with the id's of all the scans
    currently configured in Tenable.sc. If no additional parameter specified,
    the function uses the detailed mode and prints all the scan names and ids.

    If mode set to 'silent' will not print any details
   
    '''
    rawdata = get_sc(resource='asset?fields=id,name,owner&filter=excludeAllDefined,usable')
    response = rawdata.json()
    list_ids = []

    if mode=='detail':
        print("Asset List ID\tAsset List Name")
    
    for asset_list in response['response']['usable']:
        list_ids.append(asset_list['id'])
        
        if mode=='detail':
            print('{}\t\t{}'.format(asset_list['id'], asset_list['name']))
    
    return list_ids

def create_csv_al(filename,al_name):
    '''
    Create an Asset list in Tenable.sc using as input a .csv file only containing
    IP addresses.

    Required Parameters:
    filename: String that includes the .csv, eg: filename.csv
    al_name: String with the desired name for the new asset list
    '''
    
    f = open(filename, "r")
    lines = f.readlines()
    list_ip=[]

    for line in lines:
        list_ip.append(line.strip())

    payload = { "type":"static",
                "definedIPs": ','.join(list_ip),
                "name": al_name
                }
    response = post_sc('asset', payload)
    
    return response