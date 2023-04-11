# Groups all methods related to retrieval of the vulnerabilities found in Tenable.io

from base_functions import *
from scans import *

class vulnerabilities:

    # Connect to Tenable.io with no parameter mode
    tio = connect_io()

    def vuln_report(self, *args, filename):
        '''
        Creates a vulnerabilities csv report. The filename is a string that should be
        provided always without specifying the format.
        
        If used without arguments, will generate a vulnerabilities report of all the
        available scans in Tenable.io.
        
        If scans id's passed as parameters, the report will only contain data of the
        specified id's
    '''
        
        # This line connects to T.io and gets the scan id's using get_scan_ids
        io_scans = scans()
        scan_ids = io_scans.get_scans_id()
      
        
        if len(args) == 0:


            with open(filename+'.csv', 'ab') as reportobj:
                for id in scan_ids:

                    try:
                        self.tio.scans.export(id,('severity', 'neq', 'Info'), fobj=reportobj, format='csv')
                        print("Done with scan id:"+str(id))

                    except Exception:
                        print("Could not work with Scan:"+str(id))
                        continue
                    

            return "All vulnerabilities report completed!"
            
        else:
            for id in args:
                
                if id in scan_ids:
                    with open(filename+'.csv', 'ab') as reportobj:

                        try:
                            self.tio.scans.export(id,('severity', 'neq', 'Info'), fobj=reportobj, format='csv')
                            print("Done with scan id:"+str(id))
                        except Exception:
                            print("Could not work with Scan:"+str(id))
                            continue
                else:
                    print("The scan id: "+str(id)+" does not exist, skipping to next scan id!")
                    continue
                    
            return "Selected scans report completed!"

