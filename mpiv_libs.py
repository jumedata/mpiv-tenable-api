<<<<<<< HEAD
# By: MPIV Partners - v1.3
=======
# By: MPIV Partners - v1.0
>>>>>>> b3fa1b15ae0f2aa8cec2c8895130fbe4c4920461

#### NOTES ################################
# The user should store API keys in a file named API_Keys.txt. 
# that file should contain only two lines:
# 1st line Access Key
# 2nd line Secret Key
#
<<<<<<< HEAD
#################IMPROVEMENTS#####################
# 
#

=======
# To use all functions type in: import mpiv_libs.py *
#
#################IMPROVEMENTS#####################
# How T.io connection can be tested?
#


>>>>>>> b3fa1b15ae0f2aa8cec2c8895130fbe4c4920461
from tenable.io import TenableIO

def connect_IO():
    '''This function connects to Tenable.io, user should store API keys in a file
    named API_Keys.txt. That file should contain only two lines: 1st line AK, second: SK'''
    with open("API_Keys.txt") as file:
        api_keys = [line.rstrip() for line in file]
        access_key = api_keys[0]
        secret_key = api_keys[1]
    tio = TenableIO(access_key, secret_key)
<<<<<<< HEAD
    print(tio.server.status())
    return tio
    
def show_scans():
=======
    return tio
    
def show_scans():
    '''This function shows all scans available in a T.io instance, will print the results'''
>>>>>>> b3fa1b15ae0f2aa8cec2c8895130fbe4c4920461
    tio = connect_IO()
    scans_id = []
    for scan in tio.scans.list(): 
        print('{id}\t{status}\t {name} '.format(**scan))
        scans_id.append(scan['id'])
    return scans_id

<<<<<<< HEAD
def vuln_report(*args, filename):
=======
def report(*args, filename):
    '''This function generates a report of all scans or a selected number of scans
    to call the function do it like this:
    
    eg: report(scan_id, filename='yourfilename')
    
    If no scan ID specified, will generate a full report. Scan ID's should be comma separated '''
    
>>>>>>> b3fa1b15ae0f2aa8cec2c8895130fbe4c4920461
    all_scans = show_scans()
    tio = connect_IO()
    
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
<<<<<<< HEAD
    return None

def get_asset_list():
    
    tio = connect_IO()
    list_assets =[]
    
    for asset in tio.exports.assets():
        list_assets.append(asset)
    
    return list_assets

def get_tag_list():
    
    tio = connect_IO()
    lista_tags = []
    
    for tag in tio.tags.list():
        lista_tags.append(tag)
    return lista_tags

def asset_report(filename):
    
    tio = connect_IO()
    list_assets = get_asset_list()
    
    with open(filename+'.csv', 'w') as file:
        
        file.write("UUID,IP,NAME\n")
    
        for asset in list_assets:

            ips = ""
            names = ""

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

            file.write(asset['id']+','+ips+','+names+'\n')
    print(".csv Report Completed!")
    return None

def tag_exists(category, value):
    
    tio = connect_IO()
    tags = get_tag_list()
    uuid_tags = []
    lista_tags = []
    
    for tag in tags:
        lista_tags.append((tag['category_name'],tag['value']))
        uuid_tags.append(tag['uuid'])
          
    if (category,value) in lista_tags:
        print(uuid_tags[lista_tags.index(('OS','Windows'))])
        return True
    else:
        return False

def tag_summary():
    tio = connect_IO()
    tags = get_tag_list()
    
    print("Category\tValue\t\tTag UUID")
    
    for tag in tags:
        print(tag['category_name']+'\t\t'+tag['value']+'\t\t'+tag['uuid'])
    return None
    
    
    
=======
    return None        
    

>>>>>>> b3fa1b15ae0f2aa8cec2c8895130fbe4c4920461
