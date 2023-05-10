# Groups all methods related to retrieval or modifications of the scans in Tenable.sc

from base_functions import *

class scans:

    def details_report(self):
        '''
        Generates a .csv file detailing the credentials, scan policies and asset lists
        that each scan uses. Does not require input parameters

        File generated: sc_scans_details_repo.csv
        '''

        # Request info through a API get request
        response = get_sc(resource='scan?fields=id,name,credentials,policy,assets,owner&filter=excludeAllDefined,usable')
        scan_details = response.json()

        iline = ""
        creds = ""
        als = ""

        with open('sc_scans_details_repo.csv', 'w') as file:
            
            file.write("Scan ID,Scan Name,Scan Policy, Credentials, Asset Lists\n")

            for scan in scan_details['response']['usable']:

                iline+=scan['id']+','+scan['name']+','+scan['policy']['name']

                if len(scan['credentials']) == 0:
                    creds += 'None'

                else:
                    for credential in scan['credentials']:
                        creds += credential['name'] + ';'

                    creds = creds.strip(';')

                iline += ','+creds

                if len(scan['assets']) == 0:
                    als += 'None'

                else:
                    for al in scan['assets']:
                        als += al['name'] + ';'

                    als = als.strip(';')

                iline += ','+als

                file.write(iline+'\n')

                iline = ""
                creds = ""
                als = ""
        
        return "Scans details report generated"