# Use Tenable SC through Pytenable
# By: MPIV Partners
# v1.1 - Jan 23rd, 2022
#### NOTES #######################################
# Connectio to T.sc changed from user/pass to API keys
#
#################IMPROVEMENTS#####################
# Use API Keys
#


from tenable.sc import TenableSC

def connect_pass_sc():
    '''This function connects to Tenable.sc, user should store user and password in a file named
    SC_API_Keys.txt. That file should contain only three lines: 1st Tenable.sc IP, 2nd: user name,
    3rd: password'''

    with open("SC_Pass_Keys.txt") as file:
        connection_details = [line.rstrip() for line in file]
        ip_addr = connection_details[0]
        user_name = connection_details[1]
        password = connection_details[2]
    
    sc = TenableSC(ip_addr)
    sc.login(user_name, password)
    return sc

def connect_apik_sc():

    with open("SC_API_Keys.txt") as file:
        connection_details = [line.rstrip() for line in file]
        host = connection_details[0]
        AK = connection_details[1]
        SK = connection_details[2]
    sc = TenableSC(host, access_key = AK, secret_key = SK)
    return sc 


def create_csv_al(filename,al_name):
    '''This functions create a Asset list in T.sc using a .csv file
    '''
    sc = connect_apik_sc()
    f = open(filename, "r")
    lines = f.readlines()
    list_ip=[]
    for line in lines:
        list_ip.append(line.strip())
    sc.asset_lists.create(al_name, 'static',ips=list_ip)
    print("Asset list "+al_name+" successfully created")
    return None

def show_asset_lists():
    al_ids=[]
    sc = connect_apik_sc()
    asset_lists = sc.asset_lists.list()['manageable']
    print("Asset List ID\tAsset List Name")
    for al in asset_lists:
        print("{}\t\t{}".format(al['id'], al['name']))
        al_ids.append(int(al['id']))
   
    return al_ids

def scan_details_report():
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
            
    print("Scans details report generated")
    return None




#def get_assetlist_id(al_name):
