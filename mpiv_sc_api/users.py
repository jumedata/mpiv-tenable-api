# Groups all methods related to retrieval or modifications of users in Tenable.sc

from base_functions import *

class users:

    def created_items(self):

        '''
        Returns a csv and a dictionary detailing items created by each user.
        The items are: Asset lists, scans, credentials, policies, reports and dashboards
        '''

        def del_semicolon(column):
            # Internal function used to delete semicolons at the end of each item to be written

            for user in user_item:
            
                if len(user[column]) != 0:
                    user[column] = user[column].strip(';')
            return None


        user_item = [] # List of dictionaries with the items related to each user


        # Get a list of all the user created in Tenable.sc
        r_users = get_sc(resource='user?fields=username,role')
        user_details = r_users.json()['response']

        
        # For each user in Tenable.sc create an entry in the user_item list
        for user in user_details:
            user_item.append({'username':user['username'],'role':user['role']['name'], 'Asset Lists':'', 'Scans':'', 'Credentials':'',
                            'Policies':'', 'Reports':'', 'Dashboards':''})
        
        # Get a list of the assets list created in Tenable.sc
        r_asset = get_sc(resource='asset?filter=excludeAllDefined,usable&fields=id,name,creator')
        asset_details = r_asset.json()['response']['usable']

        # For each asset list created in Tenable.sc, check who created it, and add the asset list name 
        # to the user details

        for al in asset_details:
        
            for user in user_item:
                
                if user['username'] == al['creator']['username']:

                    user['Asset Lists']+=al['name']+';'

                else:
                    pass
            
        del_semicolon('Asset Lists')    
                
        # Get a list of the scans created in Tenable.sc
        r_scan = get_sc(resource='scan?fields=id,name,creator')
        scan_details = r_scan.json()['response']['usable']

        # For each scan created in Tenable.sc, check who created it, and add the scan name 
        # to the user details

        for scan in scan_details:
        
            for user in user_item:
                
                if user['username'] == scan['creator']['username']:

                    user['Scans']+=scan['name']+';'
                    
                else:
                    pass
        
        del_semicolon('Scans')
    
    
        # Get a list of the credentials created in Tenable.sc
        r_cred = get_sc(resource='credential?fields=id,name,creator')
        cred_details = r_cred.json()['response']['usable']

        # For each credential created in Tenable.sc, check who created it, and add the credential name 
        # to the user details

        for cred in cred_details:
        
            for user in user_item:
                
                if user['username'] == cred['creator']['username']:

                    user['Credentials']+=cred['name']+';'

                else:
                    pass
        
        del_semicolon('Credentials')

        # Get a list of the policies created in Tenable.sc

        r_policy = get_sc(resource='policy?fields=id,name,creator')
        policy_details = r_policy.json()['response']['usable']

        # For each policy created in Tenable.sc, check who created it, and add the policy name 
        # to the user details

        for policy in policy_details:
        
            for user in user_item:
                
                if user['username'] == policy['creator']['username']:

                    user['Policies']+=policy['name']+';'

                else:
                    pass
        
        del_semicolon('Policies')

        # Get a list of the reports created in Tenable.sc

        r_report = get_sc(resource='reportDefinition?fields=id,name,creator')
        report_details = r_report.json()['response']['usable']

        # For each report created in Tenable.sc, check who created it, and add the report name 
        # to the user details

        for report in report_details:
        
            for user in user_item:
                
                if user['username'] == report['creator']['username']:

                    user['Reports']+=report['name']+';'

                else:
                    pass
        
        del_semicolon('Reports')

        # Get a list of the dashboards created in Tenable.sc

        r_dash = get_sc(resource='dashboard?fields=id,name,owner')
        dashboard_details = r_dash.json()['response']['usable']

        # For each dashboard created in Tenable.sc, check who created it, and add the dashboard name 
        # to the user details

        for dashboard in dashboard_details:
        
            for user in user_item:
                
                if user['username'] == dashboard['owner']['username']:

                    user['Dashboards']+=dashboard['name']+';'

                else:
                    pass

        del_semicolon('Dashboards')
        
        # Convert the results list of dictionaries in a .csv file
        dict_to_csv(user_item,'sc_user_created_items')
    
        return "Users report generated"