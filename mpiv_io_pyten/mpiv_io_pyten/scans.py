# Groups all methods related to retrieval or modifications of the scans in Tenable.io

from .base_functions import *

class scans:
    
    # Connect to Tenable.io with no parameter mode
        
    def report():
        '''
        Creates a .csv report named tio_scans_report.csv with the deatils of the id, 
        status, name of the scan and owner of a scan
        '''
        tio = connect_io()
        with open('output_files/io_scans_report.csv', 'w') as file:
            
            file.write("Scan ID,Status,Name,Owner\n")
            #print("Scan ID\tStatus\tName\tOwner") 
    
            for scan in tio.scans.list(): 
                line = '{id},{status},{name},{owner}\n'.format(**scan)
                file.write(line)

        return "T.io Scan Report Generated"
 
    
    def get_ids():
        
        '''
        Returns a python list with all the scan id's available in Tenable.io
        '''
        tio = connect_io()
        scan_ids = []

        for scan in tio.scans.list(): 
            scan_ids.append(scan['id'])
        return scan_ids