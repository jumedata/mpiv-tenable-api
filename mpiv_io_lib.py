# Use Tenable IO through Pytenable
# By: MPIV Partners
# v1.3 - Jan 18th, 2022
#### NOTES ################################
# The user should store API keys in a file named TIO_API_Keys.txt 
# that file should contain only two lines:
# 1st line Access Key
# 2nd line Secret Key
#
#################IMPROVEMENTS#####################
# Use ciphered version of the API Keys files
#


from tenable.io import TenableIO

def connect_io():
    '''Connects to Tenable.io, user should store API keys in a file
    named IO_API_Keys.txt. That file should contain only two lines: 1st line AK, second: SK.
    After connecting it will show the status of the connection. Returns an object called: tio,
    which contains all the tio objects avaibale with pytenable'''

    with open("IO_API_Keys.txt") as file:
        api_keys = [line.rstrip() for line in file]
        access_key = api_keys[0]
        secret_key = api_keys[1]
    tio = TenableIO(access_key, secret_key)
    print(tio.server.status())
    return tio
    
def show_scans():
    '''This function first, connects to tenable.io using connect_IO and then shows in screen the 
    list of all the scans created in T.io. Returns a list with all the scans id's'''

    tio = connect_io()
    scans_id = []
    print('Scan ID\tStatus\t\t Name')
    for scan in tio.scans.list(): 
        print('{id}\t{status}\t {name} '.format(**scan))
        scans_id.append(scan['id'])
    return scans_id

def vuln_report(*args, filename):
    '''This function creates a vulnerabilities csv report. The user will always need to provide the
    filename as 'filename' (No need to add the format). if no arguments added, the function will
    generate a vulnerabilities report of all scans. If sacn id's passed, it will only generate
    the report of the provided scan id's. The function returns nothing but, generates the .csv 
    report. The function prints messages on screen when report is completed'''
    
    # This line connects to T.io and gets the scan id's using show_scans
    all_scans = show_scans() 
    tio = connect_io()
    
    if len(args) == 0:
        with open(filename+'.csv', 'ab') as reportobj:
            for i in all_scans:
                tio.scans.export(i,('severity', 'neq', 'Info'), fobj=reportobj, format='csv')
                print("Done with scan id:"+str(i))
    
        print("All vulnerabilities report completed!")
        
    else:
        for i in args:
            
            if i in all_scans:
                with open(filename+'.csv', 'ab') as reportobj:
                    tio.scans.export(i,('severity', 'neq', 'Info'), fobj=reportobj, format='csv')
                    print("Done with scan id:"+str(i))
            else:
                print("The scan id: "+str(i)+" does not exist, skipping to next scan id!")
                continue
                
        print(".csv Report Completed!")
    return None

def get_asset_list():

    '''This function connects to Tenable.io and returns a list of dictionaries with the assets info
    '''
    
    tio = connect_io()
    list_assets =[]
    
    for asset in tio.exports.assets():
        list_assets.append(asset)
    
    return list_assets

def get_tag_list():
    
    '''This function connects to Tenable.io and returns a list of dictionaries with tags info'''

    tio = connect_io()
    lista_tags = []
    
    for tag in tio.tags.list():
        lista_tags.append(tag)
    return lista_tags

def asset_report(filename):

    '''This function generates a csv file with the list of assets found in Tenable.io. The file has
    the following fields for each asset: UUID, IP, DNS Name and Tags. If an asset has more than one
    IP or assigned to more than one tag, all the available options willbe semicolon separated.
    The function returns nnothing but shows in screen when the report is finished'''
    
    list_assets = get_asset_list()
    
    with open(filename+'.csv', 'w') as file:
        
        file.write("UUID,IP,NAME,TAGS(Category:Value)\n")
    
        for asset in list_assets:

            ips = ""
            names = ""
            tags = ""

            if len(asset['ipv4s']) == 1:
                ips = asset['ipv4s'][0]
            elif len(asset['ipv4s']) > 1:

                for i in range(len(asset['ipv4s'])):
                    ips += asset['ipv4s'][i]+';'

                rev = ips[::-1].replace(";", "", 1)
                ips = rev[::-1]
            else:
                continue

            if len(asset['fqdns']) == 1:
                names = asset['fqdns'][0]
            elif len(asset['fqdns']) > 1:

                for i in range(len(asset['fqdns'])):
                    names += asset['fqdns'][i]+';'

                rev_n = names[::-1].replace(";", "", 1)
                names = rev_n[::-1]
            else:
                continue
                
            if len(asset['tags']) == 1:
                
                tags = asset['tags'][0]['key']+":"+asset['tags'][0]['value']
            
            elif len(asset['tags']) > 1:

                for i in range(len(asset['tags'])):
                    tags += asset['tags'][i]['key']+':'+asset['tags'][i]['value']+';'

                rev_n = tags[::-1].replace(";", "", 1)
                tags = rev_n[::-1]
            else:
                continue

            file.write(asset['id']+','+ips+','+names+','+tags+'\n')
    print(".csv Report Completed!")
    return None

def tag_summary():
    '''This functions print in screen the list of tags avaialble in T.io'''
    tags = get_tag_list()
    
    print("Category\tValue\t\tTag UUID")
    
    for tag in tags:
        print(tag['category_name']+'\t\t'+tag['value']+'\t\t'+tag['uuid'])
    return None
    
    
