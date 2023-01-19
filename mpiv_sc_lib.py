# Use Tenable SC through Pytenable
# By: MPIV Partners
# v1.0 - Jan 18th, 2022
#### NOTES ################################
# Current connection only through user/password combination
#
#################IMPROVEMENTS#####################
# Use API Keys
#


from tenable.sc import TenableSC

def connect_sc():
    '''This function connects to Tenable.sc, user should store user and password in a file named
    SC_API_Keys.txt. That file should contain only three lines: 1st Tenable.sc IP, 2nd: user name,
    3rd: password'''

    with open("SC_API_Keys.txt") as file:
        connection_details = [line.rstrip() for line in file]
        ip_addr = connection_details[0]
        user_name = connection_details[1]
        password = connection_details[2]
    
    sc = TenableSC(ip_addr)
    sc.login(user_name, password)
    return sc

def create_csv_al(filename,al_name):
    sc =    connect_sc()
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
    sc = connect_sc()
    asset_lists = sc.asset_lists.list()['manageable']
    print("Asset List ID\tAsset List Name")
    for al in asset_lists:
        print("{}\t\t{}".format(al['id'], al['name']))
        al_ids.append(int(al['id']))
   
    return al_ids

def scan_creds_report():
    sc = connect_sc()
    iline =""
    with open('scans_creds_report.csv', 'w') as file:
        file.write("Scan ID,Scan Name, Credentials\n")
        
        
        for scan in sc.scans.list()['manageable']:
            scan_detail = sc.scans.details(scan['id'])
            iline+=scan_detail['id']+','+scan_detail['name']+','
            
            if len(scan_detail['credentials']) == 0:
                iline+='None'
            else:
                for credential in scan_detail['credentials']:
                    iline+=credential['name']+';'
                    
            rev_n = iline[::-1].replace(";", "", 1)
            iline = rev_n[::-1]
                
            file.write(iline+'\n')
            iline=""
    print("Scans/Credentials report generated")
    return None




#def get_assetlist_id(al_name):
