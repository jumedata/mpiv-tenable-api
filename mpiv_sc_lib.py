# Use Tenable SC through Pytenable
# By: MPIV Partners
# v1.3 - Jan 25th, 2022
#### NOTES #######################################
# Added doctring comments and edit function
#
#################IMPROVEMENTS#####################
# 
#


from tenable.sc import TenableSC

def connect_pass_sc():
    '''
    Creates a connection to Tenable.sc using an user name and paswword. 
    The user name and password are read from a  file called SC_Pass_Keys.txt 
    
    The file should have only three lines in the
    following order:

    1st Line: IP addres of the Tenable.sc
    2nd Line: username
    3rd Line: password

    Returns an sc object which allows to use al pytenable methods.

    Because of the type of connection, will return a in screen message alerting.
    it is starting an unauthenticated session
    '''

    with open("SC_Pass_Keys.txt") as file:
        connection_details = [line.rstrip() for line in file]
        ip_addr = connection_details[0]
        user_name = connection_details[1]
        password = connection_details[2]
    
    sc = TenableSC(ip_addr)
    sc.login(user_name, password)
    return sc

def connect_apik_sc():

    '''
    Creates a connection to Tenable.sc using API keys. The keys are read from a 
    file called SC_API_Keys.txt. The file should have only three lines in the
    following order:

    1st Line: IP addres of the Tenable.sc
    2nd Line: Access Key
    3rd Line: Secret Key

    Returns an sc object which allows to use all pytenable methods.
    '''

    with open("SC_API_Keys.txt") as file:
        connection_details = [line.rstrip() for line in file]
        host = connection_details[0]
        AK = connection_details[1]
        SK = connection_details[2]
    sc = TenableSC(host, access_key = AK, secret_key = SK)
    return sc 


def create_csv_al(filename,al_name):
    '''
    Create an Asset list in Tenable.sc using as input a .csv file only containing
    IP addresses.

    Required Parameters:
    filename: String that includes the .csv, eg: filename.csv
    al_name: String with the desired name for the new asset list
    '''
    sc = connect_apik_sc()
    f = open(filename, "r")
    lines = f.readlines()
    list_ip=[]
    for line in lines:
        list_ip.append(line.strip())
    sc.asset_lists.create(al_name, 'static',ips=list_ip)
    print("Asset list "+al_name+" successfully created")
    return "Asset list {} successfully created".format(al_name)

def show_asset_lists(mode='detail'):
    
    '''
    In all cases the functions returns a list with the id's of all the scans
    currently configured in Tenable.sc. If no additional parameter specified,
    the function uses the detailed mode and prints all the scan names and ids.

    If mode set to 'silent' will not print any details

    If wrong mode selectes will return an alert message    
    '''

    al_ids=[]
    sc = connect_apik_sc()
    asset_lists = sc.asset_lists.list()['manageable']

    if mode == 'silent':
        for al in asset_lists:
            al_ids.append(int(al['id']))
        return al_ids
    
    elif mode == "detail":

        print("Asset List ID\tAsset List Name")
        for al in asset_lists:
            print("{}\t\t{}".format(al['id'], al['name']))
            al_ids.append(int(al['id']))
    
        return al_ids
    
    else:
        return "Mode {} not specified".format(mode)

def scan_details_report():
    '''
    Generates a .csv file detailing the credentials, scan policies and asset lists
    that each scan uses. Does not require imput parameters

    File generated: scans_details_report.csv
    '''

    sc = connect_apik_sc()
    iline =""
    with open('scans_details_report.csv', 'w') as file:
        file.write("Scan ID,Scan Name, Credentials, Scan Policy, Asset Lists\n")
        
        for scan in sc.scans.list()['manageable']:
            
            scan_detail = sc.scans.details(scan['id'])
            
            # Add the scan id and name to the line
            iline+=scan_detail['id']+','+scan_detail['name']+','
            
            # Add the credentials to the line
            if len(scan_detail['credentials']) == 0:
                iline+='None'
            else:
                for credential in scan_detail['credentials']:
                    iline+=credential['name']+';'
                    
            rev_n = iline[::-1].replace(";", "", 1)
            iline = rev_n[::-1]

            # Add the Scan policy
            
            iline+= ','+scan_detail['policy']['name']
            
           
            # Add the Assets List Name

            if len(scan_detail['assets']) == 0:
                iline+= ',None'
            elif len(scan_detail['assets']) == 1:
                iline+= ','+scan['assets'][0]['name']
            else:
                iline+=','
                for al in scan_detail['assets']:
                    iline+=al['name']+';'
                rev_n = iline[::-1].replace(";", "", 1)
                iline = rev_n[::-1]
          
            file.write(iline+'\n')
            iline=""
            
    return "Scans details report generated"

def edit_csv_al(al_id,filename,mode='add'):

    '''
    Edits an asset list from a .csv file. If no mode selected, by default the 
    function will add the ip's on the .csv file to the current ip config. If full 
    mode specified, the current ip's  will be deleted and the ones specified in 
    the csv file will be configured to the asset list
    '''
    
    sc = connect_apik_sc()
    al_ids = show_asset_lists(mode = 'silent')

    if al_id not in al_ids:
        return "Asset list id {} does not exists".format(al_id)
    else:
        pass

    f = open(filename, "r")
    lines = f.readlines()
    new_ips=[]
    for line in lines:
        new_ips.append(line.strip())
        
    if mode=='add':
        al_detail = sc.asset_lists.details(al_id)
        current_ips = al_detail['typeFields']['definedIPs'].split(',')
        
        sc.asset_lists.edit(al_id,ips = new_ips + current_ips)
        
        return "Succesfully added IP's to {}".format(al_detail['name'])
    
    elif mode=='full':
        sc.asset_lists.edit(al_id,ips = new_ips)
        
        return "Succesfully Edited IP's on {}".format(al_detail['name'])
        
    else:
        return "{} mode not specified, use full for full edit or no parameter to add new IP's".format(mode)


#def get_assetlist_id(al_name):
