from base_functions import *

class assets_lists:


    def used_in(self, al_id):

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

    def show_lists(self, mode='silent'):
    
        '''
        In all cases the functions returns a .csv file with the details of all 
        assets list configured in Tenable.sc. If no parameter specified, the
        funtion will only generate the CSV report, if detailed mode selected,
        the function will alson print details in screen.

        '''
        rawdata = get_sc(resource='asset?fields=id,name,type,owner&filter=excludeAllDefined,usable')
        response = rawdata.json()
        list_ids = []

        with open('sc_asset_list_report.csv', 'w') as file:
            
            file.write("Asset List ID,Ownwer,Type,Asset List Name\n")

            if mode=='detail':
                print("Asset List ID\tOwner\t\tType\t\tAsset List Name")
            
            for asset_list in response['response']['usable']:
                list_ids.append(asset_list['id'])
            
                if mode=='detail':
                    print('{}\t\t{}\t\t{}\t\t{}'.format(asset_list['id'], asset_list['owner']['username'],asset_list['type'], asset_list['name']))
                
                file.write(asset_list['id']+','+asset_list['owner']['username']+','+asset_list['type']+','+asset_list['name']+"\n")
        
        return list_ids
    

    def create_from_csv(self, filename,al_name):
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

        if response.ok == True:
            return "Asset List"+al_name+"Created"
        
        else:
            return "Could not create Asset list"
    
    def edit_from_csv(self, al_id,filename,mode='add'):

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
    
