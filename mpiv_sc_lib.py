# Use Tenable SC through Tenable.sc Official API
# By: MPIV Partners
# v1.5 - Feb 22nd, 2023
#### NOTES #######################################
# 
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

def show_asset_lists(mode='silent'):
    
    '''
    In all cases the functions returns a list with the id's of all the scans
    currently configured in Tenable.sc. If no additional parameter specified,
    the function uses the detailed mode and prints all the scan names and ids.

    If mode set to 'silent' will not print any details
   
    '''
    rawdata = get_sc(resource='asset?fields=id,name,type,owner&filter=excludeAllDefined,usable')
    response = rawdata.json()
    list_ids = []

    if mode=='detail':
        print("Asset List ID\tAsset List Name\tOwner\tType")
    
    for asset_list in response['response']['usable']:
        list_ids.append(asset_list['id'])
        
        if mode=='detail':
            print('{}\t\t{}\t\t{}\t\t{}'.format(asset_list['id'], asset_list['name'], asset_list['owner']['username'],asset_list['type']))
    
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

def edit_csv_al(al_id,filename,mode='add'):

    '''
    Edits an asset list from a .csv file. If no mode selected, by default the 
    function will add the ip's on the .csv file to the current ip config. If full 
    mode specified, the current ip's  will be deleted and the ones specified in 
    the csv file will be configured to the asset list
    '''

    response = get_sc(resource='asset/'+str(al_id))

    if response.ok != True:
        return "Asset list id {} does not exists".format(al_id)
    else:
        f = open(filename, "r")
        lines = f.readlines()
        new_ips=[]
        for line in lines:
            new_ips.append(line.strip())
        
        if response.json()['response']['type'] != 'static':
            return "Asset list id {} is not static and cannot be editted".format(al_id)
        else:
            if mode == 'add':
                
                current_ips = response.json()['response']['typeFields']['definedIPs'].split(',')
                new_ips += current_ips
                payload = {"definedIPs": ','.join(new_ips)}
                patch_sc('asset/'+str(al_id), payload)
                
                return "Succesfully added IP's to {}".format(response.json()['response']['name'])
                
            elif mode == 'full':
                
                payload = {"definedIPs": ','.join(new_ips)}
                patch_sc('asset/'+str(al_id), payload)
                                
                return "Succesfully edited IP's on {}".format(response.json()['response']['name'])
            
            else:
                return "Mode not specified"
            
def al_used_in(al_id):

    '''
    Returns a dictionary with the names of queries and scans where a given 
    asset list is used. If the dictionary is empty it means it is not used
    '''
    queries = []
    scans = []

    r_query = get_sc(resource='query?filter=usable&fields=id,name,filters')
    r_scan = get_sc(resource='scan?filter=excludeAllDefined,usable&fields=id,name,assets')

    query_details = r_query.json()['response']['usable']
    scan_details = r_scan.json()['response']['usable']
    
    for query in query_details:
        
        for fil in query['filters']:
            if fil['filterName'] == 'asset' and fil['value']['id'] == str(al_id):
                
                queries.append(query['name'])
                
    for scan in scan_details:
    
        if len (scan['assets']) > 0:


            for al in scan ['assets']:
                if al['id'] == str(al_id):

                    scans.append(scan['name'])
    
    return {'queries': queries, 'scans': scans}


def user_created_items():

    '''
    Returns a dictionary detailing the scans and asset lists create by  
    each user
    '''
    user_item = []
    r_users = get_sc(resource='user?fields=username,role')
    user_details = r_users.json()['response']


    for user in user_details:
        user_item.append({'username':user['username'],'role':user['role']['name'], 'Asset Lists':[], 'Scans':[], 'Credentials':[],
                          'Policies':[], 'Reports':[], 'Dashboards':[]})
    
    r_asset = get_sc(resource='asset?filter=excludeAllDefined,usable&fields=id,name,creator')
    asset_details = r_asset.json()['response']['usable']

    for al in asset_details:
    
        for user in user_item:
            
            if user['username'] == al['creator']['username']:

                user['Asset Lists'].append(al['name'])

            else:
                pass
    
    r_scan = get_sc(resource='scan?fields=id,name,creator')
    scan_details = r_scan.json()['response']['usable']

    for scan in scan_details:
    
        for user in user_item:
            
            if user['username'] == scan['creator']['username']:

                user['Scans'].append(scan['name'])

            else:
                pass

    r_cred = get_sc(resource='credential?fields=id,name,creator')
    cred_details = r_cred.json()['response']['usable']

    for cred in cred_details:
    
        for user in user_item:
            
            if user['username'] == cred['creator']['username']:

                user['Credentials'].append(cred['name'])

            else:
                pass

    r_policy = get_sc(resource='policy?fields=id,name,creator')
    policy_details = r_policy.json()['response']['usable']

    for policy in policy_details:
    
        for user in user_item:
            
            if user['username'] == policy['creator']['username']:

                user['Policies'].append(policy['name'])

            else:
                pass

    r_report = get_sc(resource='reportDefinition?fields=id,name,creator')
    report_details = r_report.json()['response']['usable']

    for report in report_details:
    
        for user in user_item:
            
            if user['username'] == report['creator']['username']:

                user['Reports'].append(report['name'])

            else:
                pass

    r_dash = get_sc(resource='dashboard?fields=id,name,owner')
    dashboard_details = r_dash.json()['response']['usable']

    for dashboard in dashboard_details:
    
        for user in user_item:
            
            if user['username'] == dashboard['owner']['username']:

                user['Dashboards'].append(dashboard['name'])

            else:
                pass
 
    return user_item

