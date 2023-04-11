# Groups all methods related to retrieval or modifications of the scans in Tenable.io

from base_functions import *

class scans:
    
    # Connect to Tenable.io with no parameter mode
    tio = connect_io()
    
    def show_scans(self):
        '''
        Creates a .csv report named tio_scans_report.csv with the deatils of the id, 
        status, name of the scan and owner of a scan
        '''
        
        with open('io_scans_report.csv', 'w') as file:
            
            file.write("Scan ID,Status,Name,Owner\n")
            #print("Scan ID\tStatus\tName\tOwner") 
    
            for scan in self.tio.scans.list(): 
                line = '{id},{status},{name},{owner}\n'.format(**scan)
                file.write(line)

        return "T.io Scan Report Generated"
 
    
    def get_scans_id(self):
        
        '''
        Returns a python list with all the scan id's available in Tenable.io
        '''
        
        scan_ids = []

        for scan in self.tio.scans.list(): 
            scan_ids.append(scan['id'])
        return scan_ids