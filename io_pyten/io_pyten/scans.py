# Groups all methods related to retrieval or modifications of the scans in Tenable.io

from .connections import *

class scans:
        
    @staticmethod
    def report():

        tio = connect_io()
        '''
        Creates a .csv report named tio_scans_report.csv with the deatils of the id, 
        status, name of the scan and owner of a scan
        '''
        
        with open('output_files/io_scans_report.csv', 'w') as file:
            
            file.write("Scan ID,Status,Name,Owner\n")
            #print("Scan ID\tStatus\tName\tOwner") 
    
            for scan in tio.scans.list(): 
                line = '{id},{status},{name},{owner}\n'.format(**scan)
                file.write(line)

        return "T.io Scan Report Generated"
 
    @staticmethod
    def get_ids():

        tio = connect_io()
        
        '''
        Returns a python list with all the scan id's available in Tenable.io
        '''
        
        scan_ids = []

        for scan in tio.scans.list(): 
            scan_ids.append(scan['id'])
        return scan_ids