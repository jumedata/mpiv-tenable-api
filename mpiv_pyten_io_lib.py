# Use Tenable IO through Pytenable
# By: MPIV Partners
# v1.3 - Jan 23th, 2023
#### NOTES ################################
# Added doc string comments 
# 
#
#################IMPROVEMENTS#####################
# Use ciphered version of the API Keys files
#


from tenable.io import TenableIO
import csv

def connect_io(*args):
    '''
    Creates a connection to Tenable.io using API keys. The keys are read from a 
    file called IO_API_Keys.txt. The file should have only two lines in the
    following order:

    1st Line: Access Key
    2nd Line: Secret Key

    Returns an io object which allows to use all pytenable methods.
    '''

    if len(args) == 0:
        with open("IO_API_Keys.txt") as file:
            api_keys = [line.rstrip() for line in file]
            access_key = api_keys[0]
            secret_key = api_keys[1]
        tio = TenableIO(access_key, secret_key)
        print(tio.server.status())
        return tio
    
    elif len(args) == 2:
        tio = TenableIO(args[0], args[1])
        print(tio.server.status())
        return tio

    else:
        return "Incorrect number of parameters"


def get_scan_ids():
    '''
    Returns a list with all scan id's in Tenable.io
    '''

    tio = connect_io()
    scan_ids = []

    for scan in tio.assets.list(): 
        scan_ids.append(scan['id'])
    return scan_ids

def get_asset_list():

    '''
    Connects to Tenable.io, returns a list of dictionaries with the assets info
    '''
    
    tio = connect_io()
    list_assets =[]
    
    for asset in tio.exports.assets():
        list_assets.append(asset)
    
    return list_assets

def get_tag_list():
    
    '''
    Connects to Tenable.io and returns a list of dictionaries with tags info
    '''

    tio = connect_io()
    lista_tags = []
    
    for tag in tio.tags.list():
        lista_tags.append(tag)
    
    return lista_tags

def show_scans():
    '''
    Connects to tenable.io using and creates a .csv report with all
    the scans created in T.io. Also Returns a list with all the scans id's
    '''

    tio = connect_io()
    
    with open('tio_scans_report.csv', 'w') as file:
        file.write("Scan ID,Status,Name,Owner\n")
        #print("Scan ID\tStatus\tName\tOwner") 
    
        for scan in tio.scans.list(): 
            #print('{id}\t{status}\t{name}\t{owner}'.format(**scan))
            line = '{id},{status},{name},{owner}\n'.format(**scan)
            file.write(line)

    return "T.io Scan Report Generated"


def vuln_report(*args, filename):
    '''
    Creates a vulnerabilities csv report. The filename is a string that should be
    provided always without specifying the format.
    
    If used without arguments, will generate a vulnerabilities report of all the
    available scans in Tenable.io.
    
    If scans id's passed as parameters, the report will only contain data of the
    specified id's
   '''
    
    # This line connects to T.io and gets the scan id's using get_scan_ids
    scan_ids = get_scan_ids()
    tio = connect_io()
    
    if len(args) == 0:


        with open(filename+'.csv', 'ab') as reportobj:
            for id in scan_ids:

                try:
                    tio.scans.export(id,('severity', 'neq', 'Info'), fobj=reportobj, format='csv')
                    print("Done with scan id:"+str(id))

                except Exception:
                    print("Could not work with Scan:"+str(id))
                    continue
                

        return "All vulnerabilities report completed!"
        
    else:
        for id in args:
            
            if id in scan_ids:
                with open(filename+'.csv', 'ab') as reportobj:

                    try:
                        tio.scans.export(id,('severity', 'neq', 'Info'), fobj=reportobj, format='csv')
                        print("Done with scan id:"+str(id))
                    except Exception:
                        print("Could not work with Scan:"+str(id))
                        continue
            else:
                print("The scan id: "+str(id)+" does not exist, skipping to next scan id!")
                continue
                
        return "Selected scans report completed!"


def asset_report(filename='io_assets_report'):

    '''
    Generates a csv file with the list of assets found in Tenable.io. The file 
    has the following fields for each asset: 
    
        UUID: Unique asset Tenable.io identifier
        IP: IP's related to the asset
        DNS Name
        Tags: Tags assigned to the asset
        
    If an asset has more than one related tag or IP, all the available options 
    
    will be shown in the same cell, semicolon separated.
    '''
    
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

                ips = ips.strip(';')

            else:
                continue

            if len(asset['fqdns']) == 1:
                names = asset['fqdns'][0]
            elif len(asset['fqdns']) > 1:

                for i in range(len(asset['fqdns'])):
                    names += asset['fqdns'][i]+';'

                names = names.strip(';')
            else:
                continue
                
            if len(asset['tags']) == 1:
                
                tags = asset['tags'][0]['key']+":"+asset['tags'][0]['value']
            
            elif len(asset['tags']) > 1:

                for i in range(len(asset['tags'])):
                    tags += asset['tags'][i]['key']+':'+asset['tags'][i]['value']+';'

                tags = tags.strip(';')
            else:
                tags = ""

            file.write(asset['id']+','+ips+','+names+','+tags+'\n')
    
    print(".csv Report Completed!")
    return None

def tag_summary():
    '''
    Prints in screen the list of tags avaialble in T.io
    '''
    tags = get_tag_list()
    if len(tags) == 0:
        print("Any tags are created yet")
    else:
        print("Category\tValue\t\tTag UUID")

        with open('io_tag_summary.csv', 'w') as file:
        
            file.write("Category,Value,Tag UUID\n")
        
            for tag in tags:
                file.write('{category_name},{value},{uuid}\n'.format(**tag))
                print('{category_name}\t\t{value}\t\t{uuid}'.format(**tag))

        return "Tags summary report generated"
    
def update_tags_csv(filename):

    '''
    Updates tags on assets from a csv file
    '''

    tio = connect_io()
    reader = csv.DictReader(open(filename))
    
    try:
        for row in reader:
        
            tio.tags.assign(assets=['{UUID}'.format(**row)],tags=['{TAG_ID}'.format(**row)])
    except Exception:
        print("Could not UPDATE: "+row('UUID'))
    
    return "Tag information update un provided assets"
    
    
