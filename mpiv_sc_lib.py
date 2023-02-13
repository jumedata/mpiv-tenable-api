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

def connect_sc(resource = 'currentUser'):

    '''
    Creates a connection to Tenable.sc using API keys. The keys are read from a 
    file called SC_API_Keys.txt. The file should have only three lines in the
    following order:

    1st Line: IP addres of the Tenable.sc
    2nd Line: Access Key
    3rd Line: Secret Key

    Returns an response with the specified resource.
    '''

    with open("SC_API_Keys.txt") as file:
        connection_details = [line.rstrip() for line in file]
        host = connection_details[0]
        AK = connection_details[1]
        SK = connection_details[2]
    
    
    headers = {'x-apikey':'accesskey='+AK+'; secretkey='+SK}
    response = requests.get('https://'+host+'/rest/'+resource, headers = headers, verify = False)

    return response

def show_asset_lists(mode='silent'):
    
    '''
    In all cases the functions returns a list with the id's of all the scans
    currently configured in Tenable.sc. If no additional parameter specified,
    the function uses the detailed mode and prints all the scan names and ids.

    If mode set to 'silent' will not print any details

    If wrong mode selected will return an alert message    
    '''
    rawdata = connect_sc(resource='asset?fields=id,name,owner&filter=excludeAllDefined,usable')
    response = rawdata.json()
    list_ids = []

    if mode=='detail':
        print("Asset List ID\tAsset List Name")
    
    for asset_list in response['response']['usable']:
        list_ids.append(asset_list['id'])
        if mode=='detail':
            print('{}\t\t{}'.format(asset_list['id'], asset_list['name']))
    
    return list_ids

