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

def scan_details_report():
    '''
    Generates a .csv file detailing the credentials, scan policies and asset lists
    that each scan uses. Does not require imput parameters

    File generated: scans_details_report.csv
    '''
    response = get_sc(resource='scan?fields=id,name,credentials,policy,assets,owner&filter=excludeAllDefined,usable')

    scan_details = response.json()

    iline = ""
    creds = ""
    als = ""

    with open('scans_details_report.csv', 'w') as file:
        
        file.write("Scan ID,Scan Name, Credentials, Scan Policy, Asset Lists\n")

        for scan in scan_details['response']['usable']:

            iline+=scan['id']+','+scan['name']+','+scan['policy']['name']

            if len(scan['credentials']) == 0:
                creds += 'None'

            else:
                for credential in scan['credentials']:
                    creds += credential['name'] + ';'

                rev_n = creds[::-1].replace(";", "", 1)
                creds = rev_n[::-1]

            iline += ','+creds

            if len(scan['assets']) == 0:
                als += 'None'

            else:
                for al in scan['assets']:
                    als += al['name'] + ';'

                rev_n = als[::-1].replace(";", "", 1)
                als = rev_n[::-1]

            iline += ','+als

            file.write(iline+'\n')

            iline = ""
            creds = ""
            als = ""
    
    return "Scans details report generated"



