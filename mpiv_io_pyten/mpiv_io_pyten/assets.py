# Groups all methods related to retrieval or modifications of the assets found in Tenable.io

from .base_functions import *

class assets:

    # Connect to Tenable.io with no parameter mode
    

    def get_list():

        '''
        Returns a python list of dictionaries with the assets info
        '''

        tio = connect_io()
        list_assets =[]
        
        for asset in tio.exports.assets():
            list_assets.append(asset)
        
        return list_assets
    

    def report(filename='io_assets_report'):

        '''
        Generates a csv file with the list of assets found in Tenable.io. The file 
        has the following fields for each asset: 
        
            UUID: Unique asset Tenable.io identifier
            IP: IP's related to the asset
            DNS Name
            Tags: Tags assigned to the asset
            
        If an asset has more than one related tag or IP, all the available options 
        will be shown in the same cell separated by a semicolon.

        If no file name provided the name of the csv file will be: io_assets_report.csv
        '''

        # Create an asset object to use the get asset list
        
        my_assets = assets()
        list_assets = my_assets.get_list()

        with open(filename+'.csv', 'w') as file:
            
            file.write("UUID,IP,NAME,TAGS(Category:Value)\n")
        
            for asset in list_assets:

                ips = ""
                names = ""
                tags = ""

                # Identify how many ips an asset has

                if len(asset['ipv4s']) == 1:
                    ips = asset['ipv4s'][0]
                elif len(asset['ipv4s']) > 1:

                    for i in range(len(asset['ipv4s'])):
                        ips += asset['ipv4s'][i]+';'

                    ips = ips.strip(';')

                else:
                    continue

                # Identify how many fqdn's an asset has

                if len(asset['fqdns']) == 1:
                    names = asset['fqdns'][0]
                elif len(asset['fqdns']) > 1:

                    for i in range(len(asset['fqdns'])):
                        names += asset['fqdns'][i]+';'

                    names = names.strip(';')
                else:
                    continue
                    
                # Identify how many tags an asset has

                if len(asset['tags']) == 1:
                    
                    tags = asset['tags'][0]['key']+":"+asset['tags'][0]['value']
                
                elif len(asset['tags']) > 1:

                    for i in range(len(asset['tags'])):
                        tags += asset['tags'][i]['key']+':'+asset['tags'][i]['value']+';'

                    tags = tags.strip(';')
                else:
                    tags = ""

                # Writes the line to the .csv file
                file.write(asset['id']+','+ips+','+names+','+tags+'\n')
        
        return "Assets .csv Report Completed!"
    
    def update_tags_csv(filename):

        '''
        Updates the tags of an assets according to the information provided in a .csv file
        The file should only have two columns, the UUID and the tag that wants to be assigned
        '''
        tio = connect_io()
        reader = csv.DictReader(open(filename))
        
        try:
            for row in reader:
            
                tio.tags.assign(assets=['{UUID}'.format(**row)],tags=['{TAG_ID}'.format(**row)])
        except Exception:
            print("Could not UPDATE: "+row('UUID'))
        
        return "Tag information updated in provided assets"
    
    def untagged():

        '''
        Generates a .csv report of untagged assets
        '''

        my_assets = assets()
        list_assets = my_assets.get_list()
        untagged_assets = []
   
        
        with open('output_files/io_untagged_assets.csv', 'w') as file:
            
            file.write("UUID,IP,NAME\n")
        
            for asset in list_assets:

                if len(asset['tags']) == 0:
                    untagged_assets.append(asset)

                    ips = ""
                    names = ""

                    # Identify how many ips an asset has

                    if len(asset['ipv4s']) == 1:
                        ips = asset['ipv4s'][0]
                    elif len(asset['ipv4s']) > 1:

                        for i in range(len(asset['ipv4s'])):
                            ips += asset['ipv4s'][i]+';'

                        ips = ips.strip(';')

                    else:
                        continue

                    # Identify how many fqdn's an asset has

                    if len(asset['fqdns']) == 1:
                        names = asset['fqdns'][0]
                    elif len(asset['fqdns']) > 1:

                        for i in range(len(asset['fqdns'])):
                            names += asset['fqdns'][i]+';'

                        names = names.strip(';')
                    else:
                        continue
                        
                    # Identify how many tags an asset has


                    # Writes the line to the .csv file
                    file.write(asset['id']+','+ips+','+names+'\n')

        return "Untagged report completed"