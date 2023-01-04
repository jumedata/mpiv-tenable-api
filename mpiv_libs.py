# By: MPIV Partners - v1.0

#### NOTES ################################
# The user should store API keys in a file named API_Keys.txt. 
# that file should contain only two lines:
# 1st line Access Key
# 2nd line Secret Key
#
#################IMPROVEMENTS#####################
# How T.io connection can be tested?
#


from tenable.io import TenableIO

def connect_IO():
    '''This function connects to Tenable.io, user should store API keys in a file
    named API_Keys.txt. That file should contain only two lines: 1st line AK, second: SK'''
    with open("API_Keys.txt") as file:
        api_keys = [line.rstrip() for line in file]
        access_key = api_keys[0]
        secret_key = api_keys[1]
    tio = TenableIO(access_key, secret_key)
    return tio
    
def show_scans():
    tio = connect_IO()
    scans_id = []
    for scan in tio.scans.list(): 
        print('{id}\t{status}\t {name} '.format(**scan))
        scans_id.append(scan['id'])
    return scans_id

def report(*args, filename):
    all_scans = show_scans()
    tio = connect_IO()
    
    if len(args) == 0:
        with open(filename+'.csv', 'ab') as reportobj:
            for i in all_scans:
                tio.scans.export(i,('severity', 'neq', 'Info'), fobj=reportobj, format='csv')
                print("Done with scan id:"+str(i))
    
        print("All vulnerabilities report completed!")
        
    else:
        for i in args:
            
            if i in all_scans:
                with open(filename+'.csv', 'ab') as reportobj:
                    tio.scans.export(i,('severity', 'neq', 'Info'), fobj=reportobj, format='csv')
                    print("Done with scan id:"+str(i))
            else:
                print("The scan id: "+str(i)+" does not exist, skipping to next scan id!")
                continue
                
        print(".csv Report Completed!")
    return None        
    

