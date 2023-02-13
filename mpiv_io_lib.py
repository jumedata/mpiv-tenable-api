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

def connect_io():
    '''
    Creates a connection to Tenable.io using API keys. The keys are read from a 
    file called IO_API_Keys.txt. The file should have only two lines in the
    following order:

    1st Line: Access Key
    2nd Line: Secret Key

    Returns an io object which allows to use all pytenable methods.
    '''

    with open("IO_API_Keys.txt") as file:
        api_keys = [line.rstrip() for line in file]
        access_key = api_keys[0]
        secret_key = api_keys[1]
    tio = TenableIO(access_key, secret_key)
    print(tio.server.status())
    return tio
    
def show_scans():
    
    '''
    Connects to tenable.io using connect_IO and then shows in screen the list
    of all the scans created in T.io. 
    
    Returns a list with all the scans id's
    '''

    tio = connect_io()
    scans_id = []
    print('Scan ID\tStatus\t\t Name')
    for scan in tio.scans.list(): 
        print('{id}\t{status}\t {name} '.format(**scan))
        scans_id.append(scan['id'])
    return scans_id

def vuln_report(*args, filename):
    '''
    Creates a vulnerabilities csv report. The filename is a string that should be
    provided always without specifying the format.
    
    If used without arguments, will generate a vulnerabilities report of all the
    available scans in Tenable.io.
    
    If scans id's passed as parameters, the report will only contain data of the
    specified id's
    
   '''
    
    # This line connects to T.io and gets the scan id's using show_scans
    all_scans = show_scans() 
    tio = connect_io()
    
    if len(args) == 0:
        with open(filename+'.csv', 'ab') as reportobj:
            for i in all_scans:
                tio.scans.export(i,('severity', 'neq', 'Info'), fobj=reportobj, format='csv')
                print("Done with scan id:"+str(i))
    
        return "All vulnerabilities report completed!"
        
    else:
        for i in args:
            
            if i in all_scans:
                with open(filename+'.csv', 'ab') as reportobj:
                    tio.scans.export(i,('severity', 'neq', 'Info'), fobj=reportobj, format='csv')
                    print("Done with scan id:"+str(i))
            else:
                print("The scan id: "+str(i)+" does not exist, skipping to next scan id!")
                continue
                
        return "Selected scans report completed!"

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

def asset_report(filename):

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
    '''
    Prints in screen the list of tags avaialble in T.io
    '''
    tags = get_tag_list()
    
    print("Category\tValue\t\tTag UUID")
    
    for tag in tags:
        print(tag['category_name']+'\t\t'+tag['value']+'\t\t'+tag['uuid'])
    return "Done"
    
    
